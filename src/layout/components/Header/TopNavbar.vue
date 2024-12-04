<template>
  <div class="top-navbar">
    <div class="navbar-content">
      <button class="navbar-btn">
        <i class="fa fa-cogs"></i> 系统名称
      </button>
      <div class="navbar-links">
        <button class="navbar-btn">
          <i class="fa fa-home"></i> 首页
        </button>
        <button class="navbar-btn">
          <i class="fa fa-database"></i> 数据收集
        </button>
        <button class="navbar-btn">
          <i class="fa fa-bar-chart"></i> 数据分析
        </button>
        <button class="navbar-btn">
          <i class="fa fa-file-text"></i> 智能生成报告
        </button>
        <button class="navbar-btn">
          <i class="fa fa-commenting"></i> 大模型问答系统
        </button>
        <button class="navbar-btn">
          <i class="fa fa-share-alt-square"></i> 知识图谱
        </button>
      </div>
      <button class="navbar-btn navbar-admin">
        <i class="fa fa-user-o"></i> Admin
      </button>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.top-navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #343a40;
  color: white;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  padding: 0 20px;
}

.navbar-btn {
  background: none;
  color: white;
  border: none;
  margin: 0 10px;
  padding: 5px 15px;
  font-size: 16px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease;
}

.navbar-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.navbar-links {
  display: flex;
  align-items: center;
}

.navbar-admin {
  margin-left: auto;
}

.navbar-btn i {
  margin-right: 8px;
  font-size: 18px;
}
</style>
