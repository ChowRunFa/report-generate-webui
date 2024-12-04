<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { generate_framework } from '@/apis/report/paper'; // 引入后端API

// 用户输入的主题、领域和关键词
const topic = ref('人工智能的未来'); // 默认主题
const field = ref('科技趋势'); // 默认领域
const keywords = ref('人工智能, 伦理问题, 产业影响'); // 默认关键词，逗号分隔
const maxRetries = ref(3); // 用户可以自定义重试次数
const isLoading = ref(false); // 加载状态

// 保存生成的报告框架
const generatedFramework = ref<null | Record<string, any>>(null);

// 提交数据生成报告框架
const submitFrameworkData = async () => {
  if (!topic.value.trim() || !field.value.trim() || !keywords.value.trim()) {
    ElMessage.error('主题、领域和关键词不能为空');
    return;
  }

  isLoading.value = true;

  try {
    const response = await generate_framework({
      topic: topic.value,
      field: field.value,
      keywords: keywords.value.split(','), // 逗号分隔关键词
      max_retries: maxRetries.value,
    });

    generatedFramework.value = response.data.framework_preview; // 保存生成的框架
    ElMessage.success(response.message || '报告框架生成成功');
  } catch (error) {
    console.error('Error generating framework:', error);
    ElMessage.error('报告框架生成失败，请检查后端服务');
  } finally {
    isLoading.value = false;
  }
};
</script>


<template>
  <div class="container">
    <!-- 页面标题 -->
    <h1 class="page-title">📋 生成报告框架</h1>
    <p class="description">
      输入主题、领域和关键词，点击生成按钮，获取一个自动化的报告框架。
    </p>

    <!-- 输入表单 -->
    <el-form label-width="100px" class="input-form">
      <el-form-item label="主题">
        <el-input
          v-model="topic"
          placeholder="请输入报告的主题"
        ></el-input>
      </el-form-item>

      <el-form-item label="领域">
        <el-input
          v-model="field"
          placeholder="请输入报告的领域"
        ></el-input>
      </el-form-item>

      <el-form-item label="关键词">
        <el-input
          v-model="keywords"
          placeholder="请输入关键词，用逗号分隔"
        ></el-input>
      </el-form-item>

      <el-form-item label="最大重试次数">
        <el-input-number
          v-model="maxRetries"
          :min="1"
          :max="10"
          placeholder="设置最大重试次数"
        ></el-input-number>
      </el-form-item>

      <el-form-item class="action-buttons">
        <el-button
          type="primary"
          :loading="isLoading"
          @click="submitFrameworkData"
        >
          生成报告框架
        </el-button>
        <el-button
          type="warning"
          @click="() => { topic.value = ''; field.value = ''; keywords.value = ''; }"
        >
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <!-- 生成的框架展示 -->
    <el-card class="generated-framework-card" v-if="generatedFramework">
      <h2 class="section-title">生成的报告框架</h2>
      <el-table
        :data="Object.entries(generatedFramework)"
        border
        style="width: 100%"
      >
        <el-table-column prop="0" label="字段"></el-table-column>
        <el-table-column prop="1" label="内容"></el-table-column>
      </el-table>
    </el-card>

    <p v-else-if="!isLoading" class="no-data">暂未生成任何报告框架</p>
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

.generated-framework-card {
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
