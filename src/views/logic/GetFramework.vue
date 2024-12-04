<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { load_framework_reports } from '@/apis/report/paper'; // 引入后端API
import { ElMessage } from 'element-plus';

// 已保存的报告框架数据
const savedFrameworks = ref([]); // 存储从后端获取的框架数据
const searchKeyword = ref(''); // 搜索关键字
const currentPage = ref(1); // 当前页
const pageSize = ref(5); // 每页条数

// 弹窗相关数据
const showDetailsDialog = ref(false); // 控制弹窗显示
const selectedFramework = ref(null); // 存储选中的框架详情

// 从后端获取框架数据
const fetchFrameworkReports = async () => {
  try {
    const response = await load_framework_reports();
    savedFrameworks.value = response.data || [];
  } catch (error) {
    console.error('Error fetching framework reports:', error);
    ElMessage.error('获取框架报告失败，请检查后端服务');
  }
};

// 显示详情弹窗
const showFrameworkDetails = (framework) => {
  selectedFramework.value = framework;
  showDetailsDialog.value = true;
};

// 复制到剪贴板的函数
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
    ElMessage.success('复制成功！');
  } catch (error) {
    console.error('复制失败:', error);
    ElMessage.error('复制失败，请重试');
  }
};

// 过滤后的数据，支持搜索
const filteredFrameworks = computed(() => {
  if (!searchKeyword.value.trim()) {
    return savedFrameworks.value;
  }
  const keyword = searchKeyword.value.toLowerCase();
  return savedFrameworks.value.filter((framework) => {
    return (
      framework.file_name.toLowerCase().includes(keyword) ||
      framework.topic.toLowerCase().includes(keyword) ||
      framework.field.toLowerCase().includes(keyword)
    );
  });
});

// 当前分页显示的数据
const paginatedFrameworks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredFrameworks.value.slice(start, end);
});

// 监听搜索关键字变化，重置分页
watch(searchKeyword, () => {
  currentPage.value = 1;
});

// 页面加载时初始化数据
onMounted(() => {
  fetchFrameworkReports();
});
</script>


<template>
  <div class="container">
    <!-- 页面标题 -->
    <h1 class="page-title">📋 报告框架管理</h1>
    <p class="description">
      您可以查看、搜索并分页管理保存的报告框架。
    </p>

    <!-- 搜索框 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文件名、主题或领域"
        prefix-icon="el-icon-search"
        clearable
      ></el-input>
    </div>

    <!-- 已保存框架展示 -->
    <el-card class="saved-data-card" v-if="savedFrameworks.length">
      <h2 class="section-title">已保存框架</h2>
      <el-table :data="paginatedFrameworks" border style="width: 100%">
        <el-table-column prop="file_name" label="文件名" ></el-table-column>
        <el-table-column prop="topic" label="主题" ></el-table-column>
        <el-table-column prop="field" label="领域" ></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button
              size="mini"
              type="primary"
              @click="showFrameworkDetails(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredFrameworks.length"
        layout="prev, pager, next"
      />
    </el-card>

    <p v-else class="no-data">暂无框架记录</p>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="showDetailsDialog"
      title="框架详情"
      width="50%"
      :before-close="() => (showDetailsDialog = false)"
    >
<template v-if="selectedFramework">
  <p>
    <strong>文件名：</strong>
    {{ selectedFramework.file_name }}
    <el-button
      type="text"
      icon="el-icon-document-copy"
      @click="copyToClipboard(selectedFramework.file_name)"
    >
      复制
    </el-button>
  </p>
  <p>
    <strong>主题：</strong>
    {{ selectedFramework.topic }}
    <el-button
      type="text"
      icon="el-icon-document-copy"
      @click="copyToClipboard(selectedFramework.topic)"
    >
      复制
    </el-button>
  </p>
  <p>
    <strong>领域：</strong>
    {{ selectedFramework.field }}
    <el-button
      type="text"
      icon="el-icon-document-copy"
      @click="copyToClipboard(selectedFramework.field)"
    >
      复制
    </el-button>
  </p>
  <p>
    <strong>框架内容：</strong>
    {{ selectedFramework.framework || '暂无描述' }}
    <el-button
      type="text"
      icon="el-icon-document-copy"
      @click="copyToClipboard(selectedFramework.framework || '暂无描述')"
    >
      复制
    </el-button>
  </p>
</template>

      <template v-else>
        <p>暂无详情数据</p>
      </template>

      <template #footer>
        <el-button @click="showDetailsDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.container {
  max-width: 90%;
  margin: 0 auto;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f5f7fa, #e4ebf5);
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  font-size: 32px;
  color: #34495e;
  margin-bottom: 10px;
}

.description {
  text-align: center;
  font-size: 16px;
  color: #7f8c8d;
  margin-bottom: 30px;
}

.search-bar {
  margin: 20px 0;
}

.saved-data-card {
  margin-top: 30px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.no-data {
  text-align: center;
  color: #7f8c8d;
  margin-top: 20px;
}
</style>
