<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { save_prompt, load_prompts } from '@/apis/report/paper'; // 引入后端 API
import { ElMessage, ElPagination } from 'element-plus'
import { watch } from 'vue';



// 用户输入的 Prompt 和思维链
const userPrompt = ref('');
const thoughtChain = ref('');
const savedData = ref([]); // 存储从后端获取的 Prompt 和思维链记录

// 搜索关键字
const searchKeyword = ref('');
const currentPage = ref(1);
const pageSize = ref(3);

// 提交数据到后端保存为文件
const submitData = async () => {
  if (!userPrompt.value.trim() || !thoughtChain.value.trim()) {
    ElMessage.error('Prompt 和思维链不能为空');
    return;
  }

  try {
    const response = await save_prompt({
      prompt: userPrompt.value,
      chain: thoughtChain.value,
    });

    ElMessage.success(response.message || '数据保存成功');
    userPrompt.value = '';
    thoughtChain.value = '';
    await fetchSavedData(); // 提交成功后重新获取已保存数据
  } catch (error) {
    console.error('Error submitting data:', error);
    ElMessage.error('保存失败，请检查后端服务');
  }
};

// 获取后端保存的 Prompt 和思维链
const fetchSavedData = async () => {
  try {
    const response = await load_prompts();
    savedData.value = response.data || [];
  } catch (error) {
    console.error('Error fetching saved data:', error);
    ElMessage.error('获取保存数据失败');
  }
};

// 模糊搜索过滤后的数据
const filteredData = computed(() => {
  if (!searchKeyword.value.trim()) {
    return savedData.value;
  }
  return savedData.value.filter((item) => {
    const keyword = searchKeyword.value.toLowerCase();
    return (
      item.file_name.toLowerCase().includes(keyword) ||
      item.content.toLowerCase().includes(keyword)
    );
  });
});

const updatepagedData = () => {
  const start = (currentPage.value - 1) * pageSizeDoc.value;
  const end = start + pageSize.value;
  pagedData.value = filteredData.value.slice(start, end);
};


// 当前页显示的数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredData.value.slice(start, end);
});

const handlePageChange = (page: number) => {
  currentPage.value = page;
  updatepagedData(); // 更新当前页数据
};

// 当搜索关键字发生变化时重置分页
watch(searchKeyword, () => {
  currentPage.value = 1;
});


// 页面加载时获取保存的数据
onMounted(() => {
  fetchSavedData();
});
</script>

<template>
  <div class="container">
    <!-- 页面标题 -->
    <h1 class="page-title">🎯 提示词与思维链自定义</h1>
    <p class="description">
      输入您的 Prompt 和思维链，点击提交以保存到文件。您可以查看、搜索并分页管理保存的记录。
    </p>

    <!-- 输入表单 -->
    <el-form label-width="100px" class="input-form">
      <el-form-item label="提示词">
        <el-input
          type="textarea"
          v-model="userPrompt"
          placeholder="请输入自定义 提示词"
          rows="4"
        ></el-input>
      </el-form-item>

      <el-form-item label="思维链">
        <el-input
          type="textarea"
          v-model="thoughtChain"
          placeholder="请输入思维链描述"
          rows="4"
        ></el-input>
      </el-form-item>

      <el-form-item class="action-buttons">
        <el-button type="success"  @click="submitData">
          提交并保存
        </el-button>
        <el-button
          type="warning"
          @click="() => { userPrompt.value = ''; thoughtChain.value = ''; }"
        >
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文件名或内容"
        prefix-icon="el-icon-search"
        clearable
      ></el-input>
    </div>

    <!-- 已保存记录展示 -->
    <el-card class="saved-data-card" v-if="savedData.length">
      <h2 class="section-title">已保存记录</h2>
      <el-table :data="paginatedData" border style="width: 100%">
        <el-table-column prop="file_name" label="文件名"></el-table-column>
        <el-table-column prop="date" label="保存日期"></el-table-column>
        <el-table-column prop="content" label="内容"></el-table-column>
      </el-table>

      <!-- 分页 -->
    <el-pagination
      v-model:current-page="currentPage"
      :page-size="pageSize"
      :total="filteredData.length"
      layout="prev, pager, next"
      @current-change="handlePageChange"
    />

    </el-card>

    <p v-else class="no-data">暂无历史记录</p>
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

.input-form {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-buttons {
  text-align: center;
}

.action-buttons .el-button {
  margin: 0 10px;
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
