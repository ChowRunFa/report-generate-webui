<template >
    <div class="common-layout" style="background-color: rgb(219, 217, 244);">
    <el-container>

      <el-aside width="500px" >

        <div class="parameter-area" style="background-color: rgb(209,216,245);"> <!-- 左边参数区 -->
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
                    </el-card>
          <br>
          <el-card>
            <h1 style=" text-align: center;">参数说明</h1>
            <div class="demo-collapse">
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
          </el-card>
    </div>
      </el-aside>
      <el-container>

        <el-header>
          <h1 style=" text-align: center; font-size: 15px">综述报告生成</h1>

        </el-header>

        <el-main>
          <el-card>
            <div class="main-content">
              {{ related_work_content }}
           </div>
          </el-card>
       <div class="user-input">

          <el-card >
   <!-- 下方用户输入区 -->
        <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="base_abstract">
          <el-input v-model="form.base_abstract" placeholder="请输入base_abstract" @input="forceUpdate">></el-input>
        </el-form-item>
        <el-form-item label="base_paper_url">
          <el-input v-model="form.base_paper_url" placeholder="请输入base_paper_url" @input="forceUpdate"></el-input>
        </el-form-item>
        <el-form-item label="keyword">
          <el-input v-model="form.keyword" placeholder="请输入keyword" @input="forceUpdate"></el-input>
        </el-form-item>
        <el-form-item label="cite_format">
          <el-input v-model="form.cite_format" placeholder="请输入cite_format" @input="forceUpdate"></el-input>
        </el-form-item>
        <div class="button-container">
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">清空</el-button>
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
import { RefreshRight } from '@element-plus/icons-vue'
import {  related_work } from '@/apis/report/paper'
import { ElMessage } from 'element-plus'

const related_work_content = ref('')
const activeName = ref('1')
// 表单数据
const form = ref({
  base_abstract: '',
  base_paper_url: '',
  keyword: '',
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


function related_working(form){
  related_work(form).then(res => {
    if (res.data.code === 200) {
          ElMessage({
      message: res.data.msg,
      type: 'success',
    })
       // Assuming the server responds with text/html content
     related_work_content.value = res.data.data.related_work; // 更新htmlContent列表数据
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
</script>

<style scoped>
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