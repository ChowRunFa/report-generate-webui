<template>
  <div class="about bg-gradient-to-r from-blue-50 to-blue-100 min-h-screen flex items-center justify-center p-6">
    <div class="container w-full h-full max-w-5xl bg-white p-10 rounded-3xl shadow-2xl transform transition duration-300 hover:scale-105 flex flex-col justify-between">
      <h1 >📜 文本质量评估 🔎</h1>

      <!-- Candidate Text Section -->
      <div class="flex-1 mb-6 overflow-auto">
        <label for="candidateText" class="block text-2xl font-semibold mb-2 text-gray-700">待评估文本:</label>
        <textarea
          id="candidateText"
          v-model="candidateText"
          rows="6"
          class="w-full p-4 border-2 border-blue-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-shadow duration-300 ease-in-out"
          placeholder="请输入待评估文本..."></textarea>
      </div>

      <!-- Reference Text Section -->
      <div class="flex-1 mb-6 overflow-auto">
        <label for="referenceText" class="block text-2xl font-semibold mb-2 text-gray-700">参考文本:</label>
        <textarea
          id="referenceText"
          v-model="referenceText"
          rows="6"
          class="w-full p-4 border-2 border-blue-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-shadow duration-300 ease-in-out"
          placeholder="请输入参考文本..."></textarea>
      </div>

      <!-- Submit Button -->
      <div class="text-center mb-8">
        <button
          :disabled="isLoading"
          @click="submitTexts"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-2xl transition duration-300 transform hover:scale-110">
          {{ isLoading ? '评估中...' : '📝 评估' }}
        </button>
      </div>

    <el-skeleton
      v-if="!scores"
      :rows="6"
      animated
      style="margin-top: 60px;" /> <!-- 在这里设置外边距 -->

      <!-- Scores Display -->
      <div v-if="scores" class="results bg-white p-4 rounded-lg shadow-md border-t-4 border-blue-400 transition-all duration-300 ease-in-out mt-4 ">
  <h2 class="text-2xl font-semibold text-blue-700 mb-2 text-center">📊 评分结果 📊</h2>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-2 ">
    <!-- BLEU-4 Score -->
    <div class="score-card bg-blue-50 p-3 rounded-md flex items-center space-x-2 shadow-sm hover:shadow-md transition-shadow duration-300">
      <div class="score-icon bg-blue-600 text-white rounded-full p-2 text-sm">
        📘
      </div>
      <div>
        <p class="text-lg font-bold text-gray-800">BLEU-4 分数</p>
        <p class="text-xl text-blue-700 font-semibold">{{ scores['BLEU-4'] }}</p>
      </div>
    </div>

    <!-- ROUGE-1 Score -->
    <div class="score-card bg-red-50 p-3 rounded-md flex items-center space-x-2 shadow-sm hover:shadow-md transition-shadow duration-300">
      <div class="score-icon bg-red-600 text-white rounded-full p-2 text-sm">
        📕
      </div>
      <div>
        <p class="text-lg font-bold text-gray-800">ROUGE-1 分数</p>
        <p class="text-xl text-red-700 font-semibold">{{ scores['ROUGE-1'] }}</p>
      </div>
    </div>

    <!-- ROUGE-2 Score -->
    <div class="score-card bg-yellow-50 p-3 rounded-md flex items-center space-x-2 shadow-sm hover:shadow-md transition-shadow duration-300">
      <div class="score-icon bg-yellow-600 text-white rounded-full p-2 text-sm">
        📗
      </div>
      <div>
        <p class="text-lg font-bold text-gray-800">ROUGE-2 分数</p>
        <p class="text-xl text-yellow-700 font-semibold">{{ scores['ROUGE-2'] }}</p>
      </div>
    </div>

    <!-- ROUGE-L Score -->
    <div class="score-card bg-green-50 p-3 rounded-md flex items-center space-x-2 shadow-sm hover:shadow-md transition-shadow duration-300">
      <div class="score-icon bg-green-600 text-white rounded-full p-2 text-sm">
        📙
      </div>
      <div>
        <p class="text-lg font-bold text-gray-800">ROUGE-L 分数</p>
        <p class="text-xl text-green-700 font-semibold">{{ scores['ROUGE-L'] }}</p>
      </div>
    </div>
  </div>
</div>
</div>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { text_evaluate } from '@/apis/report/paper';

const candidateText = ref('');
const referenceText = ref('');
const scores = ref(null);
const isLoading = ref(false);
const error = ref('');

// 创建一个表单数据对象
const formData = ref({
  candidateText: '',
  referenceText: ''
});

// 更新表单数据对象的函数
const updateFormData = () => {
  formData.value.candidateText = candidateText.value;
  formData.value.referenceText = referenceText.value;
};

const submitTexts = async () => {
  // 更新表单数据
  updateFormData();

  // 检查输入是否为空
  if (!formData.value.candidateText.trim() || !formData.value.referenceText.trim()) {
    error.value = '待评估文本和参考文本不能为空';
    return;
  }

  try {
    isLoading.value = true;
    error.value = null;
    // 发送请求
    const response = await text_evaluate(formData.value);
    const res_data = await response.data.data;
    console.log(res_data)
    scores.value = res_data;
  } catch (error) {
    console.error('Error during text evaluation:', error);
    error.value = '评估过程中发生错误';
  } finally {
    isLoading.value = false;
  }
};


</script>
<style scoped>
h1 {
  //color: #303133;
  font-size: 24px;
  margin: 0;
  padding: 20px 0;
  text-align: center;
}

.about {
  height: 100vh; /* Ensures full-page height */
  display: flex;
  justify-content: center;
  align-items: center;
  //background: linear-gradient(135deg, #e0f7fa, #e1f5fe);
}

.container {
  height: 90%; /* Makes container take up 90% of the page height */
  width: 100%; /* Ensure full width inside its container */
  max-width: 80%; /* Limiting max width for better visual */
  overflow: hidden; /* Prevents overflowing content */
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  padding: 40px;
  //background: white;
  display: flex;
  flex-direction: column;
}

textarea {
  width: 100%;
  padding: 15px;
  //border: 1px solid #d1d5db;
  border-radius: 10px;
  resize: none;
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: border 0.3s ease, box-shadow 0.3s ease;
}
textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
}
button {
  background-color: #3b82f6;
  padding: 12px 24px;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}
button:hover {
  background-color: #2563eb;
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
}
.results {
  background: #fff;
  padding: 20px;
  border-radius: 15px;
  border-top: 4px solid #3b82f6;
  margin-top: 20px;
  flex-shrink: 0; /* Prevents the results section from shrinking */
  overflow-y:scroll;
  max-height: 40%; /* 例如，设置最大高度为 500px */
}
.score-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.score-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.score-icon {
  font-size: 24px;
  padding: 20px;
  background-color: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
