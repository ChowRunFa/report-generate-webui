<template>
  <div class="app-container min-h-screen bg-gradient-to-b from-purple-800 via-indigo-700 to-blue-700 flex flex-col items-center p-8 text-white">
    <!-- Title Section -->
    <div class="w-full max-w-5xl bg-white text-blue-900 p-6 rounded-2xl shadow-2xl text-center mb-8 transform hover:scale-105 transition duration-300">
      <h1 class="text-4xl font-bold tracking-widest">🌟 LLMs-KG-Report 🌟</h1>
    </div>

    <!-- Main Content Area occupying full available space -->
    <div class="flex-grow w-full max-w-5xl grid grid-rows-3 gap-6">
      <!-- Input Section occupying one row -->
      <div class="bg-white p-6 rounded-2xl shadow-2xl transform hover:scale-105 transition duration-300 flex flex-col justify-between h-full">
        <label for="prompt" class="block text-xl font-bold text-gray-700 mb-2">输入 Prompt:</label>
        <input
          v-model="prompt"
          id="prompt"
          type="text"
          placeholder="请输入您的Prompt..."
          class="w-full p-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-4 focus:ring-blue-400 text-gray-800 transition duration-300 ease-in-out"
        />
      </div>

      <!-- Buttons Section occupying half of the row -->
      <div class="flex space-x-6 justify-center items-center h-full">
        <button
          @click="generateReport"
          class="bg-gradient-to-r from-green-400 to-green-600 text-white font-semibold py-4 px-12 rounded-full shadow-lg hover:shadow-2xl transition duration-300 transform hover:-translate-y-1 hover:scale-110"
        >
          📝 生成报告
        </button>
        <button
          @click="uploadFile"
          class="bg-gradient-to-r from-yellow-400 to-yellow-600 text-white font-semibold py-4 px-12 rounded-full shadow-lg hover:shadow-2xl transition duration-300 transform hover:-translate-y-1 hover:scale-110"
        >
          📂 上传文件
        </button>
      </div>

      <!-- Text Content Display Section occupying one row -->
      <div class="bg-white p-6 rounded-2xl shadow-2xl transform hover:scale-105 transition duration-300 flex-grow">
        <h2 class="text-2xl font-bold mb-4 text-blue-800 text-center">📝 显示文本内容框</h2>
        <div class="bg-gray-100 p-4 rounded-lg h-full overflow-auto border border-gray-300 shadow-inner">
          {{ textContent }}
        </div>
      </div>

      <!-- Knowledge Graph Display Section occupying one row -->
      <div class="bg-white p-6 rounded-2xl shadow-2xl transform hover:scale-105 transition duration-300 flex-grow">
        <h2 class="text-2xl font-bold mb-4 text-blue-800 text-center">🔍 显示知识图谱</h2>
        <div class="bg-gray-100 p-4 rounded-lg h-full overflow-auto border border-gray-300 shadow-inner flex items-center justify-center">
          <div v-if="knowledgeGraph" v-html="knowledgeGraph" class="text-center text-gray-800"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const prompt = ref('');
const textContent = ref('这里显示生成的文本内容...');
const knowledgeGraph = ref(null);

const generateReport = () => {
  textContent.value = `生成的报告内容基于输入: ${prompt.value}`;
  knowledgeGraph.value = '<p class="text-blue-600 font-semibold">知识图谱展示区域（这里可插入图表或图形）</p>';
};

const uploadFile = () => {
  alert('文件上传功能暂未实现');
};
</script>

<style scoped>
.app-container {
  background: linear-gradient(to bottom, #6b46c1, #7b61ff, #5f9cfa);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2rem;
}

input::placeholder {
  color: #a0aec0;
  opacity: 0.8;
}

button {
  transition: all 0.3s ease;
}

button:hover {
  transform: scale(1.05);
}

.shadow-inner {
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.1);
}
</style>



<!--<template>-->

<!--<div style="display: flex; justify-content: center;">-->
<!--  <img :src="requireSrc1" style="max-width: 50%;" />-->
<!--</div>-->

<!--</template>-->

<!--<script setup lang="ts">-->
<!--import { ref } from 'vue';-->

<!--import requireSrc1 from '@/assets/kg_imgs/download.png'; // 替换为你自己的图片绝对路径-->
<!--requireSrc1: requireSrc1-->

<!--</script>-->