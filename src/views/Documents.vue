<template>
  <div>
    <!-- 搜索框 -->
    <el-input
      v-model="searchQueryDoc"
      placeholder="Search..."
      clearable
      @input="handleSearch"
      style="margin-bottom: 20px; width: 300px;"
    />

    <!-- 表格 -->
    <el-table
      :data="pagedDataDoc"
      style="width: 100%"
      :row-class-name="tableRowClassName"
      :border="true"
    >
      <el-table-column prop="date" label="Date" width="180" />
      <el-table-column prop="title" label="Title" width="300" />
      <el-table-column prop="abstract" label="Abstract" />
      <el-table-column prop="size" label="File Size (MB)" width="120" />
      <el-table-column label="Actions" width="120">
        <template #default="scope">
          <el-button
            type="primary"
            size="mini"
            @click="previewFile(scope.row)"
          >
            Preview
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="currentPageDoc"
      :page-size="pageSizeDoc"
      :total="filteredDataDoc.length"
      layout="prev, pager, next"
      @current-change="handlePageChange"
    />

    <!-- PDF 预览对话框 -->
    <el-dialog
      title="Preview PDF"
      :visible.sync="dialogVisibleDoc"
      width="80%"
    >
      <iframe
        v-if="previewUrlDoc"
        :src="previewUrlDoc"
        style="width: 100%; height: 600px; border: none;"
      ></iframe>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisibleDoc = false">Close</el-button>
      </span>
    </el-dialog>

  </div>
</template>



<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { document_list } from '@/apis/report/paper';

interface Document {
  date: string;
  title: string;
  abstract: string;
  size: number;
}

// 响应式变量
const allDataDoc = ref<Document[]>([]); // 原始数据
const filteredDataDoc = ref<Document[]>([]); // 搜索过滤后的数据
const pagedDataDoc = ref<Document[]>([]); // 当前分页展示的数据
const currentPageDoc = ref(1); // 当前页码
const pageSizeDoc = ref(10); // 每页条数
const searchQueryDoc = ref(''); // 搜索关键字
const dialogVisibleDoc = ref(false); // 控制对话框显示
const previewUrlDoc = ref(''); // 预览文件的 URL

// 获取后端数据
const fetchDocuments = async () => {
  try {
    const { data } = await document_list();
    console.log(data);
    allDataDoc.value = data || [];
    filteredDataDoc.value = allDataDoc.value; // 初始筛选数据等于全部数据
    updatepagedDataDoc(); // 初始化分页数据
  } catch (error) {
    console.error('Failed to fetch documents:', error);
  }
};

// 更新分页数据
const updatepagedDataDoc = () => {
  const start = (currentPageDoc.value - 1) * pageSizeDoc.value;
  const end = start + pageSizeDoc.value;
  pagedDataDoc.value = filteredDataDoc.value.slice(start, end);
};

// 搜索处理
const handleSearch = () => {
  currentPageDoc.value = 1; // 搜索后从第一页开始
  filteredDataDoc.value = allDataDoc.value.filter((doc) =>
    doc.title.toLowerCase().includes(searchQueryDoc.value.toLowerCase())
  );
  updatepagedDataDoc(); // 更新分页数据
};

// 分页变化处理
const handlePageChange = (page: number) => {
  currentPageDoc.value = page;
  updatepagedDataDoc(); // 更新当前页数据
};

// 动态行样式
const tableRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  return rowIndex % 2 === 0 ? 'warning-row' : '';
};

// 点击预览文件
const previewFile = (row: Document) => {
  console.log('Preview button clicked:', row.title);
  const filePath = `./uploads/docs/${row.title}`;
  if (row.title.endsWith('.pdf')) {
    previewUrlDoc.value = filePath;
    dialogVisibleDoc.value = true; // 显示预览对话框
    console.log('Preview URL set to:', previewUrlDoc.value);
  } else {
    alert('Only PDF files can be previewed.');
  }
};


// 初始化加载数据
onMounted(() => {
  fetchDocuments();
});
</script>

<style scoped>
.el-table .warning-row {
  background-color: #fdf6ec !important; /* 偶数行背景色 */
}
</style>
