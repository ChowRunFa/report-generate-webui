 <template>
  <el-container class="h-screen">
    <!-- 顶部导航 -->
    <el-header height="60px" class="header">
      <h1 class="title">Instagraph 图谱构建器</h1>
    </el-header>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <!-- 错误信息提示 -->
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        closable
        @close="closeErrorMessage"
        class="mb-4"
      ></el-alert>

      <!-- 输入表单 -->
      <el-card class="input-card">
        <el-form :model="form" label-position="top">
          <el-form-item label="构建图谱源文本" prop="userInput">
            <el-input
              type="textarea"
              v-model="form.userInput"
              placeholder="请输入文本或URL"
              :disabled="isLoading"
              :rows="6"
              autosize
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="handleFormSubmit"
              :loading="isLoading"
              :disabled="isLoading"
            >
              提交
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 加载动画 -->
      <el-progress
        v-if="isLoading"
        type="line"
        :indeterminate="true"
        :stroke-width="2"
        class="mb-4"
      ></el-progress>

      <!-- 主体内容 -->
      <div class="content-row" style="display: flex; gap: 20px;">
        <!-- 图表区域 -->
        <div style="flex: 2; height: 600px;">
        <div ref="cyRef" class="graph-container"></div>
        </div>

        <!-- 历史记录 -->
        <div style="flex: 1;">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>历史记录</span>
                                <el-text class="mx-1" type="danger">需配置图数据库/暂不可用</el-text>
                <el-button
                  type="text"
                  icon="el-icon-refresh"
                  @click="fetchGraphHistory"
                ></el-button>
              </div>
            </template>
            <p v-if="historyError">获取图谱历史失败: {{ historyError }}</p>
            <el-scrollbar v-else class="history-scroll">
              <el-collapse accordion>
                <el-collapse-item
                  v-for="(item, k) in graphHistory"
                  :key="k"
                  :title="`记录 ${k + 1}`"
                >
                  <el-card
                    @click.native="handleGraphItemClick(k)"
                    class="history-item"
                    shadow="hover"
                  >
                    <p>
                      <strong>From:</strong> {{ item.from_node.label }} (Type:
                      {{ item.from_node.type }})
                    </p>
                    <p>
                      <strong>Relationship:</strong> {{ item.relationship.type }}
                      (Direction: {{ item.relationship.direction }})
                    </p>
                    <p>
                      <strong>To:</strong> {{ item.to_node.label }} (Type:
                      {{ item.to_node.type }})
                    </p>
                  </el-card>
                </el-collapse-item>
              </el-collapse>
            </el-scrollbar>
          </el-card>
        </div>
      </div>
    </el-main>
  </el-container>
</template>
  <script setup>

  import { ref, onMounted, nextTick } from 'vue';
  import {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElMessage,
    ElAlert,
    ElProgress,
    ElRow,
    ElCol,
    ElCard,
    ElScrollbar,
    ElCollapse,
    ElCollapseItem,
  } from 'element-plus';
  import cytoscape from 'cytoscape';
  import { get_graph_history, get_response_data, get_graph_data } from '@/apis/report/paper';

  const isLoading = ref(false);
  const cyRef = ref(null);
  const form = ref({
    userInput: '',
  });
  const errorMessage = ref('');

  const graphHistory = ref([]);
  const historyError = ref('');

  /** 计算节点宽度 */
  const calcNodeWidth = (label) => {
    if (!label) {
      return '50px';
    }
    return Math.max(50, label.length * 8) + 'px';
  };

  /** 显示错误信息 */
  const showError = (message) => {
    errorMessage.value = message;
  };

  /** 关闭错误信息 */
  const closeErrorMessage = () => {
    errorMessage.value = '';
  };

  /** 数据验证和预处理函数 */
  const preprocessGraphData = (elements) => {
    const nodeIds = new Set(elements.nodes.map((node) => node.data.id));

    elements.edges.forEach((edge) => {
      const { source, target } = edge.data;

      if (!nodeIds.has(source)) {
        console.error(`边的源节点 ${source} 不存在。`);
        showError(`边的源节点 ${source} 不存在。`);
      }
      if (!nodeIds.has(target)) {
        console.error(`边的目标节点 ${target} 不存在。`);
        showError(`边的目标节点 ${target} 不存在。`);
      }

      // 如果是自循环边，添加 self-loop 类
      if (source === target) {
        if (!edge.classes) {
          edge.classes = 'self-loop';
        } else {
          edge.classes += ' self-loop';
        }
      }
    });
  };

  /** 获取文本颜色 */
  function getTextColor(bgColor = '#000000') {
    const [r, g, b] = [0, 2, 4].map((start) =>
      parseInt(bgColor.replace('#', '').substr(start, 2), 16)
    );
    const brightness = r * 0.299 + g * 0.587 + b * 0.114;
    return brightness < 128 ? '#ffffff' : '#000000';
  }

  /** 创建图表 */
  async function createGraph(data) {
      await nextTick(); // 确保 DOM 已更新
      console.log('cyRef:', cyRef.value);
      console.log('Container dimensions:', cyRef.value.offsetWidth, cyRef.value.offsetHeight);
      const elements = [
        ...data.elements.nodes,
        ...data.elements.edges,
      ];
    // preprocessGraphData(data.elements);
      const cy = cytoscape({
      container: cyRef.value,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(color)',
            label: 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            shape: 'rectangle',
            height: '50px',
            width: (ele) => calcNodeWidth(ele.data('label')),
            color: (ele) => getTextColor(ele.data('color')),
            'font-size': '12px',
          },
        },
        {
          selector: 'edge',
          style: {
            width: 3,
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            label: 'data(label)',
            'curve-style': 'bezier',
            'line-dash-pattern': [4, 4],
            'text-background-color': '#ffffff',
            'text-background-opacity': 1,
            'text-background-shape': 'rectangle',
            'font-size': '10px',
          },
        },
        // 自循环边样式
        {
          selector: 'edge.self-loop',
          style: {
            'curve-style': 'bezier',
            'loop-direction': '0deg',
            'loop-sweep': '20deg',
            'control-point-step-size': 40,
          },
        },
      ],
      layout: {
        name: 'cose',
        fit: true,
        padding: 30,
        avoidOverlap: true,
        nodeOverlap: 10,
        componentSpacing: 40,
        nodeRepulsion: 10000,
      },
      ready: function() {
        this.fit();
        this.center();
      },
    });
  }

  /** 渲染图表 */
  const renderGraph = async () => {
    try {
      const response = await get_graph_data();
      if (response.status === 200) {
        const graphData = response.data;
        if (!graphData || Object.keys(graphData).length === 0) {
          console.error('图谱数据为空');
          showError('图谱数据为空');
          return;
        } else {
          await createGraph(graphData);
        }
      } else {
        showError(response.data.error || '获取图谱数据失败');
      }
    } catch (error) {
      console.error('获取图谱数据出错:', error);
      showError('获取图谱数据失败：' + error.message);
    }
  };

  /** 处理表单提交 */
  async function handleFormSubmit() {
    isLoading.value = true;
    const payload = { user_input: form.value.userInput };

    try {
      const response = await get_response_data(payload);
      if (response.status === 200) {
        await renderGraph();
        ElMessage.success('图谱生成成功');
      } else {
        showError(response.data.error || '请求错误');
      }
    } catch (error) {
      console.error('请求出错:', error);
      showError('请求错误：' + error.message);
    }
    isLoading.value = false;
  }

  /** 获取图表历史记录 */
  async function fetchGraphHistory() {
    try {
      const response = await get_graph_history();
      if (response.status === 200) {
        const graph_response = response.data;
        if (graph_response.graph_history && graph_response.graph_history.length > 0) {
          graphHistory.value = graph_response.graph_history;
        } else {
          historyError.value = '没有图谱历史记录';
        }
      } else {
        showError(response.data.error || '获取图谱历史失败');
      }
    } catch (error) {
      console.error('获取图谱历史出错:', error);
      historyError.value = error.message;
    }
  }

  /** 处理历史记录项点击事件 */
  function handleGraphItemClick(key) {
    const itemData = graphHistory.value[key];
    const transformedData = transformDataToGraphFormat(itemData);
    createGraph(transformedData);
  }

  /** 转换数据格式以适应 Cytoscape */
  function transformDataToGraphFormat(itemData) {
    // 检查自循环边并添加 self-loop 类
    const isSelfLoop = itemData.from_node.id === itemData.to_node.id;
    const edgeData = {
      id: `edge-${itemData.relationship.id || new Date().getTime()}`,
      color: itemData.relationship.color,
      label: itemData.relationship.type,
      source: itemData.from_node.id,
      target: itemData.to_node.id,
    };
    if (isSelfLoop) {
      edgeData.classes = 'self-loop';
    }

    return {
      elements: {
        edges: [
          {
            data: edgeData,
          },
        ],
        nodes: [
          {
            data: {
              id: itemData.from_node.id,
              label: itemData.from_node.label,
              type: itemData.from_node.type,
              color: itemData.from_node.color,
            },
          },
          {
            data: {
              id: itemData.to_node.id,
              label: itemData.to_node.label,
              type: itemData.to_node.type,
              color: itemData.to_node.color,
            },
          },
        ],
      },
    };
  }

  onMounted(() => {
    fetchGraphHistory();
  });
  </script>

  <style scoped>
  .header {
    background-color: #409eff;
    color: #fff;
    display: flex;
    align-items: center;
    padding-left: 20px;
  }

  .title {
    font-size: 24px;
    font-weight: bold;
  }

  .main-content {
    padding: 20px;
  }

  .input-card {
    margin-bottom: 20px;
  }

  .content-row {
    margin-top: 20px;
  }

  .graph-card {
    height: 600px;
  }

  .graph-container {
    width: 100%;
    height: 100%;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .history-scroll {
    max-height: 600px;
  }

  .history-item {
    margin-bottom: 10px;
    cursor: pointer;
  }

  .history-item:hover {
    background-color: #f5f7fa;
  }

  .el-col {
    height: 100%;
  }

  .el-row {
    height: 100%;
  }


  .loading {
    background: linear-gradient(90deg, transparent, #007bff, transparent);
    background-size: 200% 100%;
    animation: loading-animation 2s linear infinite;
  }

  @keyframes loading-animation {
    from {
      background-position: 200% 0;
    }
    to {
      background-position: -200% 0;
    }
  }
  </style>
