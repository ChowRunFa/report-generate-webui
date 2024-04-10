<template>
  <el-card>
  <div class="upload-container">
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
      <div class="upload-area">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
      </div>
    </el-upload>
    <div class="button-group">
      <el-button type="primary" @click="submitUpload">Confirm Upload</el-button>
      <el-button type="danger" @click="clearFiles">Clear</el-button>
      <el-button type="success" @click="generateReport">Generate</el-button>
    </div>
  </div>
    </el-card>
  <el-card style="margin-bottom: 20px;">
    <div class="report-output" v-html="htmlContent"></div>
  </el-card>
</template>

<script setup lang="ts">
  import { UploadFilled } from '@element-plus/icons-vue'
  import { ElMessage, ElButton } from 'element-plus'
  import { ref } from 'vue'

  const uploadRef = ref(null)
  const fileList = ref([])
  const htmlContent = ref('') // Add this line to store the HTML content

  const handleSuccess = (response, file, fileList) => {
    ElMessage({
      message: 'Upload successful!',
      type: 'success',
    })
  }

  const handleError = (err, file, fileList) => {
    ElMessage({
      message: 'Error during upload: ' + err.message,
      type: 'error',
    })
  }

  const submitUpload = () => {
    if (uploadRef.value) {
      uploadRef.value.submit()
    }
  }

  const clearFiles = () => {
    fileList.value = []
  }

const generateReport = async () => {
  // if (fileList.value.length === 0) {
  //   ElMessage({
  //     message: 'Please upload a file first.',
  //     type: 'warning',
  //   })
  //   return
  // }

  // Create a FormData object to hold the file to be sent
  const formData = new FormData()
  // formData.append('file', fileList.value[0].raw) // Assuming 'file' is the field expected by the backend
  //
  try {
    const response = await fetch('http://localhost:5000/paper_report', {
      method: 'POST',
      body: formData,
    })
  //
    if (response.ok) {
      const html = await response.text() // Assuming the server responds with text/html content
      htmlContent.value = html // Update the htmlContent to render the report
    } else {
      throw new Error('Server responded with status: ' + response.status)
    }
  } catch (error) {
    ElMessage({
      message: 'Error generating report: ' + error.message,
      type: 'error',
    })
  }
}

</script>

<style scoped>
.upload-container {
  text-align: center;
}

.upload-demo {
  display: inline-block;
  margin-right: 10px;
}

.upload-area {
  cursor: pointer;
  padding: 15px 20px;
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  transition: border-color .3s;
}

.upload-area:hover {
  border-color: #409eff;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.el-icon--upload {
  color: #409eff;
  font-size: 20px;
}

  .report-output {
    margin-top: 20px;
  }
</style>
