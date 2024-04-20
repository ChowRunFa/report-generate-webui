<template>
  <el-card>
    <div class="centered-form">
  <el-form :model="form" label-width="auto" style="max-width: 600px">
    <el-form-item label="模型API KEY">
      <el-input v-model="form.api_key" placeholder="请输入您的模型API KEY"/>
    </el-form-item>
    <el-form-item label="模型API BASE">
      <el-input v-model="form.api_base" placeholder="请输入您的模型API BASE"/>
    </el-form-item>
        <el-form-item label="选择模型类型">
      <el-select v-model="form.llm_name" placeholder="请选择一个模型">
        <el-option label="gpt-3.5-turbo" value="gpt-3.5-turbo" />
        <el-option label="gpt-3.5-turbo-0301" value="gpt-3.5-turbo-0301" />
        <el-option label="gpt-3.5-turbo-0613" value="gpt-3.5-turbo-0613" />
        <el-option label="gpt-3.5-turbo-1106" value="gpt-3.5-turbo-1106" />
        <el-option label="gpt-3.5-turbo-16k" value="gpt-3.5-turbo-16k" />
        <el-option label="gpt-3.5-turbo-16k-0613" value="gpt-3.5-turbo-16k-0613" />
        <el-option label="gpt-4" value="gpt-4" />
        <el-option label="gpt-4-0314" value="gpt-4-0314" />
        <el-option label="gpt-4-0613" value="gpt-4-0613" />
        <el-option label="gpt-4-32k" value="gpt-4-32k" />
        <el-option label="gpt-4-32k-0314" value="gpt-4-32k-0314" />
        <el-option label="gpt-4-32k-0613" value="gpt-4-32k-0613" />
        <el-option label="gpt-4-1106-preview" value="gpt-4-1106-preview" />
        <el-option label="gpt-4-vision-preview" value="gpt-4-vision-preview" />
      </el-select>
    </el-form-item>
    <el-form-item label="设为默认配置">
      <el-switch v-model="form.using" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">Submit</el-button>
      <el-button>Cancel</el-button>
    </el-form-item>
  </el-form>
    </div>
    </el-card>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessageBox } from 'element-plus'
import {set_llm} from '@/apis/report/paper'

// do not use same name with ref
const form = reactive({
  llm_name: '',
  api_key: '',
  api_base: '',
  using: 0 // 初始值为0
})

function llm_setting() {
  // 使用api方法获取项目数据
  set_llm(form).then(res => {
    if (res.data.code === 200) {
       ElMessageBox.alert(res.data.msg, '提示', {
            // confirmButtonText: '确定',
            type: 'success'
          })
    } else {
             ElMessageBox.alert(res.data.msg, '提示', {
            // confirmButtonText: '确定',
            type: 'error'
          })
    }
  })
}

const onSubmit = () => {
 llm_setting()
}

</script>

<style>
.centered-form {
  display: flex;
  justify-content: center; /* 水平居中 */
  //height: 100vh; /* 设置容器高度为视口高度 */
}
</style>