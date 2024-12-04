<template>
  <div class="framework-report-page">
    <el-card class="report-form-card">
      <el-form :model="form" label-width="120px" class="report-form">
        <!-- 文件上传 -->

        <el-form-item label="文件上传">
                  <el-card>
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            drag
            action="http://localhost:5000/upload"
            multiple
            :file-list="fileList"
            :on-success="handleSuccess"
            :on-error="handleError"
            :auto-upload="false"
            accept=".pdf,.docx"
          >
            <el-icon size="40"><upload-filled /></el-icon>
            <p class="el-upload__text">
              <strong>将文件拖到此处</strong> 或 <em>点击上传</em>
            </p>
            <p class="el-upload__hint">支持 .pdf 和 .docx 格式文件（Supports .pdf and .docx format files）</p>
          </el-upload>
          <div class="button-group">
            <el-button type="primary" icon="UploadFilled" @click="submitUpload">确认上传</el-button>
            <el-button icon="Delete" @click="clearFiles">清空</el-button>
          </div>
          </el-card>
        </el-form-item>

        <!-- 动态章节输入 -->
        <el-form-item label="章节设置">
          <div class="section-header">
            <el-button
              type="primary"
              @click="addFrameworkField"
              :disabled="frameworkEntries.length >= 8"
            >
              添加章节
            </el-button>

            <span class="section-limit" v-if="frameworkEntries.length >= 8">（最多8个章节）</span>
          </div>
          <el-alert
            v-if="frameworkEntries.length < 8"
            type="info"
            title="在此输入您的期望报告框架，数量可添加"
            show-icon
            class="alert-limit"
          ></el-alert>

          <el-alert
            v-if="frameworkEntries.length >= 8"
            type="warning"
            title="最多允许添加 8 个章节"
            show-icon
            class="alert-limit"
          ></el-alert>

          <div
            v-for="(section, index) in frameworkEntries"
            :key="index"
            class="framework-entry"
          >
            <el-card shadow="hover">
              <div class="entry-header">
                <span>章节 {{ index + 1 }}</span>
                <el-button
                  type="text"
                  icon="el-icon-delete"
                  @click="removeFrameworkField(index)"
                  circle
                ></el-button>
              </div>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="章节标识">
                    <el-input
                      v-model="section.sectionKey"
                      placeholder="例如：section1"
                      clearable
                    ></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="章节描述">
                    <el-input
                      v-model="section.descriptionKey"
                      placeholder="例如：desc_of_section1"
                      clearable
                    ></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-card>
          </div>
        </el-form-item>
          <el-form-item label="提示工程">
                                            <PromptSelector />
          </el-form-item>
        <!-- 提交按钮 -->
        <el-form-item>
          <el-button
            type="success"
            icon="el-icon-document"
            @click="submitReport"
            class="submit-button"
          >
            生成报告
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 显示生成的报告 -->
  <div class="framework-report-page">
    <el-card v-if="reportHtml" class="report-output">
      <h3>生成的报告</h3>
      <div v-html="renderedReportHtml" class="markdown-content"></div>
    </el-card>
  </div>
  </div>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue';
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus';
import { framework_report } from '@/apis/report/paper'; // 根据您的项目结构调整路径
import MarkdownIt from 'markdown-it';
import PromptSelector from '@/components/PromptSelector.vue';

interface FrameworkEntry {
  sectionKey: string;
  descriptionKey: string;
}

const fileList = ref([]);
const uploadRef = ref(null);
const reportHtml = ref('');
const form = ref({
  file: '',
  framework: {} as Record<string, string>,
});
const frameworkEntries = ref<FrameworkEntry[]>([
  { sectionKey: '背景与目标', descriptionKey: '本章节描述项目或报告的背景信息，明确需要解决的问题以及目标。' },
  { sectionKey: '方案与方法', descriptionKey: '本章节介绍所采用的解决方案或方法，包括技术手段、工作流程或具体实施方案。' },
  { sectionKey: '实施与结果', descriptionKey: '本章节展示实施过程中的关键步骤和成果，包含数据、分析结果或案例展示。' },
  { sectionKey: '总结与建议', descriptionKey: '本章节总结报告的关键发现，并提出改进建议或未来规划。' },
]);


// 文件上传处理
const handleSuccess = (response: any, file: any) => {
  form.value.file = response.file_path;
  ElMessage.success('文件上传成功！');
};

const handleError = (err: any) => {
  ElMessage.error('上传失败：' + err.message);
};

const submitUpload = () => {
  if (uploadRef.value) {
    uploadRef.value.submit();
  }
};

const clearFiles = () => {
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
  fileList.value = [];
  form.value.file = '';
};

// 动态添加框架字段
const addFrameworkField = () => {
  if (frameworkEntries.value.length < 8) {
    frameworkEntries.value.push({
      sectionKey: '',
      descriptionKey: '',
    });
  }
};

const removeFrameworkField = (index: number) => {
  frameworkEntries.value.splice(index, 1);
};

// 提交报告生成请求
const submitReport = async () => {
  if (!form.value.file) {
    ElMessage.error('请先上传文件');
    return;
  }

  // 构建 framework 对象
  form.value.framework = {};
  frameworkEntries.value.forEach((entry) => {
    if (entry.sectionKey && entry.descriptionKey) {
      form.value.framework[entry.sectionKey] = entry.descriptionKey;
    }
  });

  try {
    const formData = new FormData();
    formData.append('file_path', form.value.file);
    formData.append('framework', JSON.stringify(form.value.framework));

    const response = await framework_report(formData);
    if (response.status === 200) {
      reportHtml.value = response.data.data.report_html;
      ElMessage.success('报告生成成功');
    } else {
      ElMessage.error(response.message || '报告生成失败');
    }
  } catch (error) {
    ElMessage.error('请求失败，请稍后重试');
  }
};

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

const renderedReportHtml = ref('');

watch(reportHtml, (newVal) => {
  renderedReportHtml.value = md.render(newVal);
});

// 初始渲染
renderedReportHtml.value = md.render(reportHtml.value);

</script>

<style scoped>
.framework-report-page {
  padding: 20px;
  background: #f5f7fa;
}

.report-form-card,
.report-output {
  margin-bottom: 20px;
}

.report-form {
  background: #fff;
}

.upload-demo {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  background-color: #fafafa;
  text-align: center;
  padding: 40px 20px;
}

.button-group {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.section-limit {
  margin-left: 10px;
  color: #f56c6c;
}

.alert-limit {
  margin-top: 10px;
}

.framework-entry {
  margin-top: 10px;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.submit-button {
  width: 100%;
}

.report-output {
  padding: 20px;
}

.report-output h3 {
  margin-bottom: 15px;
  color: #333;
}


.report-output {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.markdown-content {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
}

.markdown-content h1, .markdown-content h2, .markdown-content h3 {
  color: #2c3e50;
  margin-top: 20px;
  border-bottom: 2px solid #ebeef5;
  padding-bottom: 5px;
}

.markdown-content p {
  margin: 10px 0;
}

.markdown-content ul {
  padding-left: 20px;
}

.markdown-content li {
  margin: 5px 0;
}

.markdown-content code {
  background-color: #f2f4f5;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}

.markdown-content pre {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-content a {
  color: #409eff;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}
</style>
