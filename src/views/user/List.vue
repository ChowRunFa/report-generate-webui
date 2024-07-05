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
    <el-input  placeholder="填入您所研究的关键词（可选，默认为空）" v-model="keywords"></el-input>
  </el-form-item>

  <el-form-item label="语言">
    <el-select  placeholder="请选择输出语言(默认中文)" v-model="language">
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
  <div class="demo-pagination-block" >
    <!--    <div v-for="(content) in (12)" class="report-output"  v-html="content">-->
    <!-- 打印按钮 -->
   <el-button type="primary" v-if="paginatedContent[0]" @click="printPDF"><el-icon><Download /></el-icon></el-button>
    <div v-for="content in paginatedContent" class="report-output" v-html="content" id="report-html">

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
import { UploadFilled } from '@element-plus/icons-vue'
import { ElButton, ElMessage } from 'element-plus'
import { computed, ref } from 'vue'
import { paper_report } from '@/apis/report/paper'

const images = ref<string[]>([]);
const uploadRef = ref(null)
const fileList = ref([])
const htmlContent = ref([]); // 存储后端返回的htmlContent列表
// const htmlContent = ref(
// ['<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>\n<img src="/src/assets/mermaid_imgs/diagram1.png" width="500" alt="">', '<div class="markdown-body"><h2>Paper:1</h2>\n<ol>\n<li>标题: AutoKG: Efficient Automated Knowledge Graph (自动知识图谱:高效自动化知识图谱)</li>\n<li>Title: AutoKG: Efficient Automated Knowledge Graph</li>\n<li>Authors: Bohan Chen and Andrea L. Bertozzi</li>\n<li>Affiliation: Department of Mathematics, University of California, Los Angeles (加州大学洛杉矶分校数学系)</li>\n<li>Keywords: Large Language Models, Knowledge Graph, Graph Learning, Retrieval-augmented Generation</li>\n</ol>\n<h2>Summary:</h2>\n<ul>\n<li>(1): 本文的研究背景是传统方法在将大型语言模型（LLMs）与知识库链接时往往无法捕捉复杂的关系动态。</li>\n<li>(2): 过去的方法包括语义相似性搜索，存在问题是难以捕捉复杂的关系动态。本文的方法是有充分动机的，提出了一种轻量高效的自动化知识图谱构建方法。</li>\n<li>(3): 本文提出的研究方法是通过使用LLM提取关键词，然后通过图拉普拉斯学习评估每对关键词之间的关系权重。使用向量相似性和基于图的关联的混合搜索方案来丰富LLM响应。</li>\n<li>(4): 本文的方法在任务上取得了更全面和相互关联的知识检索机制，从而增强了LLMs在生成更具洞察力和相关性输出方面的能力。</li>\n</ul>\n<h2>Methods:</h2>\n<ul>\n<li>\n<p>(1): 使用大型语言模型（LLMs）提取关键词。</p>\n</li>\n<li>\n<p>(2): 通过图拉普拉斯学习评估每对关键词之间的关系权重。</p>\n</li>\n<li>\n<p>(3): 利用向量相似性和基于图的关联的混合搜索方案来丰富LLMs响应。</p>\n</li>\n<li>\n<p>(4): 通过构建更全面和相互关联的知识检索机制增强LLMs的生成能力。</p>\n</li>\n</ul>\n<h2>Conclusion:</h2>\n<ul>\n<li>\n<p>(1): 本研究的意义在于提出了一种轻量高效的自动化知识图谱构建方法，弥补了传统方法在捕捉复杂关系动态方面的不足。</p>\n</li>\n<li>\n<p>(2): 创新点: 提出了基于大型语言模型（LLMs）的关键词提取和图拉普拉斯学习的方法，增强了知识检索机制；表现: 在任务上取得更全面和相互关联的知识检索机制；工作量: 通过轻量高效的自动化方法减少了工作量。</p>\n</li>\n</ul></div>\n<img src="/src/assets/mermaid_imgs/diagram2.png" width="500" alt="">']); // 静态的HTML内容数组

const filePath = ref('')
const keywords = ref('')
const language = ref('')


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
      formData.append(   'keywords',keywords.value)
      formData.append(   'language',language.value)
      paper_reporting(formData)
  }
};

// 定义方法来获取图片路径
const getDiagramImagePath = (pageIndex: number) => {
  return `/src/assets/mermaid_imgs/diagram${pageIndex + 1}.png`;
};

const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}

 const printPDF = () => {
  // 定义打印样式
  let printStyle = `
    <style>
      @media print {
        #report-html {
          position: static !important;
        }
        .el-button {
          display: none !important;
        }
      }

.section {
  margin-top: 30px;
  margin-bottom: 30px;
}
p{
            margin:1em 0;
            padding:0 0 0 2em;
            text-indent:-1.5em;
            font:normal normal 16px/1.6em SimSun-ExtB;
            color:#000;
        }

.section-title {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.section-subtitle {
    text-align: center;
  font-size: 25px;
  font-weight: bold;
  font-family: SimSun-ExtB,serif;
}

.section-content {
  padding: 20px;
}

.subsection {
  margin-top: 20px;
  margin-bottom: 20px;
}

.subsection-title {
  font-size: 24px;
  font-weight: bold;
    font-family: SimSun-ExtB,serif;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin-top: 30px;
  margin-bottom: 30px;
}

.centered-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
}
.detail-info{
  font-size: 15px;
    font-family: STXihei,sans-serif;
}
.centered-list li {
  text-align: center;
  padding: 5px;
}


.teacher-info {
  border-collapse: collapse;
}
.teacher-info th, .teacher-info td {
  border: 1px solid black;
  padding: 8px;
}
.teacher-info th {
  background-color: #f2f2f2;
}
    </style>
  `;

  // 获取<el-container>的HTML内容
  let containerHtml = document.getElementById('report-html').innerHTML;

  // 创建一个新的窗口，打印HTML内容
let printWindow = window.open('www.xxx.com', '_blank');
  printWindow.document.write(printStyle + containerHtml);
  printWindow.print();
  printWindow.close();
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
.common-layout {
  background-image: radial-gradient(circle at center, #baf39d, #a8d8d8, #e5dfc8);
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
