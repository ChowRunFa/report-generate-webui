<template>
  <div class="container">
    <!-- 页面标题 -->
    <h1 class="page-title">🔮LLMs-MindMap🧠</h1>
    <!-- 功能说明 -->
    <p class="description">
      输入多段文本（每段最多500字），点击提交，我们将为您生成对应的思维导图。
    </p>

    <!-- 输入表单 -->
    <el-form :model="form" ref="formRef" class="input-form">
      <!-- 动态添加文本输入框 -->
      <div
        v-for="(input, index) in form.inputTexts"
        :key="index"
        class="text-input-item"
      >
        <el-form-item :label="'输入文本 ' + (index + 1)" label-width="80px">
          <el-input
            type="textarea"
            v-model="form.inputTexts[index]"
            :maxlength="maxLength"
            show-word-limit
            placeholder="请输入文本（最多500字）"
            rows="4"
          ></el-input>
        </el-form-item>
      </div>
      <!-- 添加和删除输入框的按钮 -->
      <el-form-item>
        <el-button type="primary" @click="addInput">添加输入框</el-button>
        <el-button
          type="danger"
          @click="removeInput"
          :disabled="form.inputTexts.length <= 1"
        >
          删除输入框
        </el-button>
      </el-form-item>
      <!-- 提交和重置按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
        <el-divider></el-divider>
    <!-- 渲染 mermaid 图 -->
    <div>

    <el-skeleton-item v-if="!mermaidTextList.length" variant="image"  style="width: 100%; height: 100%;"  />

<!--    <el-skeleton-item v-if="!mermaidTextList.length" variant="image" style="width: 100%; height: 100%;" />-->
    </div>

    <div v-if="mermaidTextList.length" class="diagram-container">
      <h2 class="section-title">生成的思维导图：</h2>
      <div
        v-for="(diagram, index) in mermaidTextList"
        :key="index"
        class="mermaid-diagram"
      >
        <h3 class="diagram-title">思维导图 {{ index + 1 }}</h3>
        <VueMermaidRender :content="diagram" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElMessage,
} from 'element-plus';
import { VueMermaidRender } from 'vue-mermaid-render';
import { get_mermaid } from '@/apis/report/paper';

const form = ref({
  inputTexts: [''],
});

const maxLength = 500;
const mermaidTextList = ref([]);

// 添加新的输入框
const addInput = () => {
  if (form.value.inputTexts.length < 10) {
    // 限制最多添加10个输入框
    form.value.inputTexts.push('');
  } else {
    ElMessage.warning('最多只能添加10个输入框');
  }
};

// 删除最后一个输入框
const removeInput = () => {
  if (form.value.inputTexts.length > 1) {
    form.value.inputTexts.pop();
  }
};

// 重置表单
const resetForm = () => {
  form.value.inputTexts = [''];
  mermaidTextList.value = [];
};

// 提交表单
const submitForm = () => {
  // 收集非空的输入文本，组成 text_list
  const text_list = form.value.inputTexts
    .map((text) => text.trim())
    .filter((text) => text);

  // 检查是否至少有一个有效的输入
  if (text_list.length === 0) {
    ElMessage.warning('请输入至少一段文本');
    return;
  }

  // 显示加载提示
  ElMessage.info('正在生成思维导图，请稍候...');
  console.log(text_list)
  // 发送输入文本列表到后端
  get_mermaid({ text_list })
    .then((response) => {
      if (response.data.code === 200) {
        mermaidTextList.value = response.data.data.mermaid_text_list;
        ElMessage.success(response.data.msg);
      } else {
        // 处理后端返回的错误信息
        ElMessage.error('生成思维导图失败：' + response.data.msg);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      ElMessage.error('请求失败，请检查网络连接');
    });
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  //background-color: #f9f9f9;
  border-radius: 8px;
}

.page-title {
  text-align: center;
  font-size: 32px;
  //color: #333;
  margin-bottom: 10px;
}

.description {
  text-align: center;
  font-size: 16px;
  //color: #666;
  margin-bottom: 30px;
}

.input-form {
  //background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}

.input-form .el-form-item {
  margin-bottom: 20px;
}

.input-form .el-button {
  margin-right: 10px;
}

.text-input-item {
  margin-bottom: 20px;
}

.diagram-container {
  margin-top: 40px;
}

.section-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.diagram-title {
  font-size: 20px;
  color: #666;
  margin-bottom: 10px;
}

.mermaid-diagram {
  margin-bottom: 40px;
  //background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}
</style>
