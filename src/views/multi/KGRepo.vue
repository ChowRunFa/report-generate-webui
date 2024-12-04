<template>
  <el-container>
    <el-header>
      <h1 style="text-align: center;">📌LLMs-KG智能报告自动生成📝</h1>
    </el-header>

    <el-main>
      <el-form :model="formData" label-width="120px">
        <el-form-item label="主题">
          <el-input v-model="formData.main_topic" placeholder="请输入主题"></el-input>
        </el-form-item>
        <el-form-item label="图谱名称">
          <el-input v-model="formData.kg_name" placeholder="请输入图谱名称"></el-input>
        </el-form-item>
        <el-form-item label="用户查询">
          <el-input
            type="textarea"
            v-model="formData.usr_query"
            placeholder="请输入用户查询"
            rows="4"
          ></el-input>
        </el-form-item>
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
              >
                <el-icon><upload-filled /></el-icon>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
              </el-upload>
              <div class="button-group">
                <el-button type="primary" @click="submitUpload">确认上传</el-button>
                <el-button @click="clearFiles">清空</el-button>
              </div>
            </el-card>
               </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">生成 LLMs-KG Report</el-button>
        </el-form-item>
      </el-form>

      <div >
        <el-divider></el-divider>
        <h2>图谱报告</h2>
        <el-card>
            <el-skeleton v-if="!responseData" :rows="5" animated />
          <div v-html="responseData.kg_report"></div>
        </el-card>
        <el-divider></el-divider>

        <h2>关键词</h2>
                    <el-skeleton v-if="!responseData" :rows="1" animated />
        <el-tag
          v-for="(keyword, index) in responseData.keywords"
          :key="index"
          type="success"
          style="margin: 5px"
        >
          {{ keyword }}
        </el-tag>

        <el-divider></el-divider>
        <h2>知识图谱</h2>    <el-button type="primary" @click="refreshKG">刷新KG</el-button>
<!--  <img v-if="imageSrc" :src="loadImage(imageSrc)" alt="" style="width: 60%; height: 70%;">-->
              <el-skeleton-item v-if="!responseData" variant="image" style="width: 240px; height: 240px" />

              <div v-if="responseData">
<!--        <img   src="~@/assets/kg_imgs/related_work_ref_KG.png" alt="" style="width: 60%; height: 70%;">-->
            <!-- 显示的图片，保持路径不变，只刷新内容 -->
<!--          <img :src="kgImageUrl" alt="Knowledge Graph" style="width: 60%; height: 70%;" />-->

            <img id="kgImage" src="~@/assets/kg_imgs/related_work_ref_KG.png" alt="Knowledge Graph" style="width: 60%; height: 70%;" />
                      </div>
      </div>
    </el-main>

  </el-container>
</template>

<script setup>
import { reactive, ref, computed, watch } from 'vue'
import { ElMessage,ElLoading } from 'element-plus';
// 引入封装的请求方法
import { auto_kg,update_kg } from '@/apis/report/paper';
import { UploadFilled } from '@element-plus/icons-vue'

const formData = reactive({
  main_topic: 'knowledge graph, automatic generation',
  kg_name: 'related_work_ref_KG',
  usr_query:
    'Please write a survey about the main topic provided by user in both English and 中文. more than 500 words',
});
const fileList = ref([]);
const uploadRef = ref(null);
const filePath = ref('');
const responseData = ref('');

const submitForm = async () => {
  // 启用加载动画
  const loadingInstance = ElLoading.service({
    lock: true,
    text: '正在生成，请稍候...',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)',
  });

  try {
    const form = new FormData();
    form.append('main_topic', formData.main_topic);
    form.append('kg_name', formData.kg_name);
    form.append('usr_query', formData.usr_query);

    // 设置超时时间，单位为毫秒（例如：30000 毫秒等于 30 秒）
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error('请求超时，请稍后重试'));
      }, 60000);
    });

    // 使用 Promise.race 来实现超时控制
    const requestPromise = auto_kg(form);
    const { data } = await Promise.race([requestPromise, timeoutPromise]);

    if (data.code === 200) {
      responseData.value = data.data;
      console.log(responseData.value)
      ElMessage.success(data.msg);
    } else {
      ElMessage.error('生成失败，请重试');
    }
  } catch (error) {
    console.error(error);
    ElMessage.error(error.message || '请求出错，请检查网络连接');
  } finally {
    // 停止加载动画
    loadingInstance.close();
  }
};

watch(
  () => responseData.value,
  (newValue) => {
    console.log('Data updated:', newValue); // 检查数据是否成功更新
  }
);

// 定义刷新KG的方法
// 定义刷新KG的方法
const refreshKG = () => {
  update_kg().then(() => {
    // 强制图片重新加载
    const imgElement = document.getElementById('kgImage');
    imgElement.src = imgElement.src.split('?')[0] + '?t=' + new Date().getTime(); // 添加时间戳避免缓存
  });
};

// const imageSrc = computed(() =>
//   responseData.value ? `@/assets/kg_imgs/${responseData.value.kg_fig_path}` : ''
// );

const handleSuccess = (response, file, fileList) => {
  filePath.value = response.file_path;
  ElMessage.success('上传成功！');
};

const handleError = (err, file, fileList) => {
  ElMessage.error('上传失败：' + err.message);
};

const submitUpload = () => {
  if (uploadRef.value) {
    uploadRef.value.submit();
  }
};

const clearFiles = () => {
  fileList.value = [];
};




</script>

<style scoped>
  /* 样式保持不变 */
</style>

<style scoped>
h1 {
  color: #303133;
  font-size: 24px;
  margin: 0;

}

h2 {
  color: #409eff;
  margin-top: 20px;
}

.el-header,
.el-footer {
  //background-color: #f5f7fa;
  line-height: 60px;
}

.el-main {
    //background-color: white;
  padding: 20px;
}

.el-card {
  margin-bottom: 20px;
}

.el-image {
  margin-top: 20px;
}
</style>
