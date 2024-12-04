<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ElDialog, ElButton, ElTable, ElTableColumn, ElPagination, ElMessage } from 'element-plus';
import { load_json_prompts } from '@/apis/report/paper'; // 引入后端 API

// 控制弹窗显示
const dialogVisible = ref(false);

// 存储从后端获取的数据
const savedData = ref([]);

// 搜索关键字
const searchKeyword = ref('');
const currentPage = ref(1);
const pageSize = ref(3);

// 获取数据的函数
const fetchData = async () => {
  try {
    const response = await load_json_prompts();
    savedData.value = response.data || []; // 假设返回数据是一个数组
  } catch (error) {
    console.error('Error fetching data:', error);
    ElMessage.error('获取数据失败，请检查网络连接');
  }
};

// 页面加载时获取数据
onMounted(() => {
  fetchData();
});

// 复制到剪贴板
const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(
    () => {
      ElMessage.success('复制成功！');
    },
    () => {
      ElMessage.error('复制失败，请重试！');
    }
  );
};

// 显示弹窗
const openDialog = () => {
  dialogVisible.value = true;
};

// 模糊搜索过滤后的数据
const filteredData = computed(() => {
  if (!searchKeyword.value.trim()) {
    return savedData.value;
  }
  const keyword = searchKeyword.value.toLowerCase();
  return savedData.value.filter((item) => {
    return (
      item.prompt.toLowerCase().includes(keyword) ||
      item.chain.toLowerCase().includes(keyword)
    );
  });
});

// 当前页显示的数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredData.value.slice(start, end);
});


const updatepagedData = () => {
  const start = (currentPage.value - 1) * pageSizeDoc.value;
  const end = start + pageSize.value;
  pagedData.value = filteredData.value.slice(start, end);
};


const handlePageChange = (page: number) => {
  currentPage.value = page;
  updatepagedData(); // 更新当前页数据
};
</script>

<template>
  <div>
    <!-- 按钮触发弹窗 -->
    <el-button type="primary" @click="openDialog">自定义提示词</el-button>

    <!-- 弹窗内容 -->
    <el-dialog v-model="dialogVisible" title="选择提示词或思维链">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索提示词或思维链"
          prefix-icon="el-icon-search"
          clearable
        />
      </div>

      <!-- 数据表格 -->
      <el-table :data="paginatedData" border>
        <el-table-column prop="prompt" label="提示词">
          <template #default="scope">
            <div class="cell-content">
              <p>{{ scope.row.prompt }}</p>
              <el-button
                type="text"
                size="small"
                @click="copyToClipboard(scope.row.prompt)"
              >
                复制
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="chain" label="思维链">
          <template #default="scope">
            <div class="cell-content">
              <p>{{ scope.row.chain }}</p>
              <el-button
                type="text"
                size="small"
                @click="copyToClipboard(scope.row.chain)"
              >
                复制
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="filteredData.length"
      layout="prev, pager, next"
      @current-change="handlePageChange"
    />



      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.cell-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cell-content p {
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 80%;
}

.search-bar {
  margin: 20px 0;
}
</style>
