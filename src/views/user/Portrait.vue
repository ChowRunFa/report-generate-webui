<template >
    <div class="common-layout" >
<!--            <el-header>-->
        <h1 >📑综合报告生成‍📍</h1>
<!--      </el-header>-->
    <el-container>

      <el-aside width="500px" >

        <div class="parameter-area" > <!-- 左边参数区 -->
           <el-card >
  <el-form-item label="引文数量 ">
    <el-input v-model.number="parameterForm.num_papers" placeholder="请输入num_papers"></el-input>
  </el-form-item>
  <el-form-item label="模型随机性">
    <el-slider v-model="parameterForm.temperature" :min="0" :max="1" :step="0.01"></el-slider>
  </el-form-item>
  <el-form-item label="引文排序">
    <el-select v-model="parameterForm.sort_by" placeholder="请选择sort_by">
      <el-option label="Citation" value="Citation"></el-option>
      <el-option label="Year" value="Year"></el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="模型重排">
    <el-switch v-model="parameterForm.rerank" :active-value="true" :inactive-value="false"></el-switch>
  </el-form-item>
  <el-form-item label="综述字数">
    <el-slider v-model.number="parameterForm.limit_words" :min="0" :max="3000" :step="100"></el-slider>
    <span class="slider-value">{{ parameterForm.limit_words }}</span>
  </el-form-item>
  <el-form-item label="S2搜索api">
    <el-input v-model="parameterForm.s2_api_key" placeholder="请输入s2_api_key"></el-input>
  </el-form-item>

  <div class="button-container">

    <el-button @click="setDefaultValues" type="warning" :icon="RefreshRight" circle />
  </div>
                    </el-card  >
          <br>


    <el-dialog  v-model="dialogVisible"  >
                <h1 style=" text-align: center; font-size: larger" >参数说明</h1>
                <div class="demo-collapse">
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item title="基础摘要" name="1">
            <div>
              请输入基础摘要：这里应该包含论文或文章的核心思想和结论的简短概述。
            </div>
          </el-collapse-item>
          <el-collapse-item title="基础论文网址" name="2">
            <div>
              请输入基础论文网址：这里应该包含论文的在线版本链接，推荐使用arxiv网址链接，方便读者访问。例如：'https://arxiv.org/abs/2402.09760'
            </div>
          </el-collapse-item>
          <el-collapse-item title="关键词" name="3">
            <div>
              请输入关键词：这里应该列出描述论文主题和内容的词汇，有助于检索和识别。例如:LLMs,QA
            </div>
          </el-collapse-item>
          <el-collapse-item title="引用格式" name="4">
            <div>
              请输入引用格式：这里应该说明在撰写论文或报告时，引用他人工作时遵循的特定样式指南。
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>


    </el-dialog>

        </div>


  <div class="upload-container">

            <el-card >
              <h1 style=" text-align: center;  ">本地文件分析</h1>
                <el-text class="mx-1" type="danger">测试功能/暂不可用</el-text>
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
         将文件拖到此处 <em>或点击上传</em>
        </div>
      </div>
    </el-upload>
    <div class="button-group">
      <el-button type="primary" @click="submitUpload">确认上传</el-button>
      <el-button type="danger" @click="clearFiles">清空</el-button>
       <el-button type="success" @click="generateReport" :disabled="!filePath" >生成</el-button>
<!--      <el-button type="success" @click="generateReport" >Generate</el-button>-->
    </div>
                      </el-card >
  </div>
      </el-aside>
      <el-container>

<!--        <el-header>-->
<!--          <h1 style=" text-align: center; font-size: 15px">综述报告生成</h1>-->

<!--        </el-header>-->

        <el-main>
          <el-card>
            <div class="main-content">
                 <el-button type="primary" v-if="related_work_content" @click="printPDF"><el-icon><Download /></el-icon></el-button>
                            <el-skeleton v-if="!related_work_content" :rows="10" animated />
                   <div v-if="related_work_content"><h2>Report:</h2></div>
                  <div v-html="related_work_content" id="related-work-report">

                  </div>
                    <div v-if="reference_content"><h2>References:</h2> </div>
<!--                <div v-html="markdown.render(reference_content)"></div>-->
                <div v-html="reference_content" id="related-work-reference">

                </div>

           </div>
          </el-card>
       <div class="user-input">

          <el-card >
            <h1 style=" text-align: center;  ">基于互联网检索生成</h1>
   <!-- 下方用户输入区 -->
        <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="基础摘要">
          <el-input v-model="form.base_abstract" placeholder="请输入base_abstract" @input="forceUpdate">></el-input>
        </el-form-item>
        <el-form-item label="基础网址">
          <el-input v-model="form.base_paper_url" placeholder="请输入base_paper_url" @input="forceUpdate" ></el-input>
        </el-form-item>
        <el-form-item label="关  键  词">
          <el-input v-model="form.keyword" placeholder="请输入keyword；" @input="forceUpdate"></el-input>
        </el-form-item>
        <el-form-item label="引用格式">
          <el-input v-model="form.cite_format" placeholder="请输入cite_format;" @input="forceUpdate"></el-input>
        </el-form-item>
        <div class="button-container">
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">清空</el-button>
          <el-button type="primary" plain @click="dialogVisible = true" >参数说明</el-button>
        </div>
      </el-form>

        </el-card>
 </div>
        </el-main>

      </el-container>
    </el-container>
  </div>

<!--  <div class="form-container">-->





<!--  </div>-->
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RefreshRight, UploadFilled } from '@element-plus/icons-vue'
import {  related_work } from '@/apis/report/paper'
import { ElButton, ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it';
const markdown = new MarkdownIt()

const related_work_content = ref('')
// const related_work_content = ref('ss')
const reference_content = ref('')
const activeName = ref('1')
// 表单数据
const form = ref({
  base_abstract: '',
  base_paper_url: 'https://arxiv.org/abs/2402.09760',
  keyword: 'LLMs、QA',
  cite_format: '',
});

// 参数数据
const parameterForm = ref({
  num_papers: 5,
  temperature: 0.3,
  sort_by: 'Citation',
  rerank: false,
  limit_words: 300,
  s2_api_key: '',
});

const dialogVisible = ref(false)

function related_working(form){
  related_work(form).then(res => {
    if (res.data.code === 200) {
          ElMessage({
      message: res.data.msg,
      type: 'success',
    })
      console.log(res.data)
       // Assuming the server responds with text/html content
     related_work_content.value = res.data.data.relatedwork; // 更新htmlContent列表数据
     reference_content.value = res.data.data.reference; // 更新htmlContent列表数据
      // console.log(htmlContent.value)
       }else {
      alert(res)
      console.log(res)
      // alert(res.data.msg)
    }
  })
}

// 提交表单
const submitForm = () => {
  // 处理提交逻辑
  const totalForm = ref(Object.assign({}, form.value, parameterForm.value));
  console.log(totalForm)
  related_working(totalForm)
};

// 重置表单
const resetForm = () => {
  form.value = {
    base_abstract: '',
    base_paper_url: '',
    keyword: '',
    cite_format: '',
  };
};

// 一键设置为默认值
const setDefaultValues = () => {
  parameterForm.value = {
    num_papers: 5,
    temperature: 0.3,
    sort_by: 'Citation',
    rerank: false,
    limit_words: 300,
    s2_api_key: '',
  };
};


function forceUpdate(event) {
  this.$forceUpdate();
}

 const printPDF = () => {
  // 定义打印样式
  let printStyle = `
    <style>
      @media print {
        #related-work-report {
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
let containerHtml = document.getElementById('related-work-report').innerHTML;
let containerHtml_ref = document.getElementById('related-work-reference').innerHTML;

  // 创建一个新的窗口，打印HTML内容
let printWindow = window.open('www.xxx.com', '_blank');
  printWindow.document.write(printStyle + containerHtml + containerHtml_ref);
  printWindow.print();
  printWindow.close();
}


</script>

<style scoped>

h1 {
  //color: #303133;
  font-size: 24px;
  margin: 0;
  padding: 20px 0;
  text-align: center;
}

.form-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
    flex: 1;
    height: 400px;
    overflow-y: scroll;
    padding: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

.user-input {
  padding: 20px;

}

.upload-container {
padding: 20px;
  text-align: center;
}

.parameter-area {
  padding: 20px;
  /* 根据实际需求设置样式 */
}

.button-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}



.slider-value {
  margin-left: 5px;
}



</style>