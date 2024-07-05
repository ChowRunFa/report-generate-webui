<template>

<div style="display: flex; justify-content: center;">
  <img :src="requireSrc1" style="max-width: 50%;" />
</div>

</template>

<script setup lang="ts">
import { ref } from 'vue';

import requireSrc1 from '@/assets/kg_imgs/download.png'; // 替换为你自己的图片绝对路径
requireSrc1: requireSrc1

</script>