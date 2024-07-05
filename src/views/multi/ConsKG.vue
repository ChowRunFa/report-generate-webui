<template>

  <img :src="requireSrc1" width="800"/>

</template>




<script setup lang="ts">
import { ref } from 'vue';
import MarkdownIt from 'markdown-it';
const markdown = new MarkdownIt()
import requireSrc1 from '@/assets/kg_imgs/kg1.png'; // 替换为你自己的图片绝对路径
requireSrc1: requireSrc1

</script>

