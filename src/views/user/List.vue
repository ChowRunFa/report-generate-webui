<template>

    <div class="common-layout " >
    <el-container >
      <el-aside width="1"  >
        <div class="container">
        <el-card >
  <div class="upload-container">
    <el-upload
      ref="uploadRef"
      class="upload-demo upload-vertical"
      drag
      action="http://localhost:5000/upload"
      multiple
      :file-list="fileList"
      :on-success="handleSuccess"
      :on-error="handleError"
      :auto-upload="false"
    >
      <div class="upload-area " >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text " >
          Drop file here or <em>click to upload</em>
        </div>
      </div>
    </el-upload>
    <div class="button-group">
      <el-button type="primary" @click="submitUpload">Confirm Upload</el-button>
      <el-button type="danger" @click="clearFiles">Clear</el-button>
<!--      <el-button type="success" @click="generateReport" >Generate</el-button>-->
    </div>
  </div>
    </el-card>
          </div>
<div class="container">
                 <el-card >

  <el-form-item label="关键词">
    <el-input  placeholder="填入您所研究的关键词（可选，默认为空）"></el-input>
  </el-form-item>

  <el-form-item label="语言">
    <el-select  placeholder="请选择输出语言(默认中文)">
      <el-option label="简体中文" value="zh"></el-option>
      <el-option label="English" value="en"></el-option>
      <el-option label="日本語" value="jp"></el-option>
    </el-select>
  </el-form-item>
<div class="button-group">
                        <!-- 添加Generate按钮 -->
      <el-button type="success" @click="generateReport" :disabled="!filePath" >Generate</el-button>
</div>
                    </el-card>
  </div>
      </el-aside>
      <el-main>
  <el-card  >
    <div class="report-container">
  <div class="demo-pagination-block">
    <div v-for="content in paginatedContent" class="report-output" v-html="content">

    </div>
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :small="small"
      :disabled="disabled"
      :background="background"
      layout="prev, pager, next, jumper"
      :total="totalItems"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
    </div>
</el-card></el-main>
    </el-container>
  </div>



  <!--<img referrerpolicy="no-referrer"  src="https://img-blog.csdnimg.cn/direct/3941ac1cb3894e3b937b21c8f4598cac.png" alt="" style="width: 200px; height: 150px;">-->
<!--<img   src="~@/assets/max_image.png" alt="" style="width: 200px; height: 150px;">-->

</template>

<script setup lang="ts">
import { RefreshRight, UploadFilled } from '@element-plus/icons-vue'
import { ElButton, ElMessage } from 'element-plus'
import { computed, ref } from 'vue'
import { paper_report } from '@/apis/report/paper'

const uploadRef = ref(null)
const fileList = ref([])
const htmlContent = ref([]); // 存储后端返回的htmlContent列表
const filePath = ref('')


const currentPage = ref(1); // 当前页码
const pageSize = ref(1); // 每页显示的数量
const small = ref(true); // 分页组件尺寸
const disabled = ref(false); // 是否禁用分页组件
const background = ref(false); // 分页组件背景


const totalItems = computed(() => htmlContent.value.length); // 总条目数量为htmlContent列表的长度

const paginatedContent = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value; // 当前页的起始索引
  const endIndex = startIndex + pageSize.value; // 当前页的结束索引
  return htmlContent.value.slice(startIndex, endIndex); // 根据当前页码和每页显示数量进行分页
});

const handleSuccess = (response, file, fileList) => {
     // Assuming the server responds with the file_path
  filePath.value = response.file_path; // Store the file_path in the filePath variable
  // console.log('filePath', filePath);
  // console.log('filePath.value', filePath.value);
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


function paper_reporting(form){
  paper_report(form).then(res => {
    if (res.data.code === 200) {
          ElMessage({
      message: res.data.msg,
      type: 'success',
    })
       // Assuming the server responds with text/html content
     htmlContent.value = res.data.data.report_html; // 更新htmlContent列表数据
      // console.log(htmlContent.value)
     filePath.value = ''
       }else {
      alert(res)
      console.log(res)
      // alert(res.data.msg)
    }
  })
}

const generateReport = async () => {
  if (filePath.value) {
      const formData = new FormData()
      formData.append(   'file_path',filePath.value)
      paper_reporting(formData)
  }
};


const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}

</script>

<style scoped>
.upload-container {
padding: 20px;
  text-align: center;
}

.upload-demo {

  display: inline-block;
  //margin-right: 10px;
}

.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;

}
.demo-pagination-block .demonstration {

  margin-bottom: 16px;
}

.upload-area {

  cursor: pointer;
  padding: 30px 200px;
  //border: px dashed #d9d9d9;
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

.common-layout{
   background-color: rgb(199,226,231);
}

.report-container {
      flex: 1;
    height: 750px;
    overflow-y: scroll;
    padding: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}
.container {
  padding: 20px; /* 调整所需的边距值 */
}
</style>
