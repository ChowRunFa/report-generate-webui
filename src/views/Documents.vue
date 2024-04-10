<template>
  <el-table
    :data="tableData"
    style="width: 100%"
    :row-class-name="tableRowClassName"
  >
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="title" label="Title" width="400" />
    <el-table-column prop="abstract" label="Abstract" />
  </el-table>
</template>

<script lang="ts" setup>
interface User {
  date: string
  title: string
  abstract: string
}

const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: User
  rowIndex: number
}) => {
  if (rowIndex === 1) {
    return 'warning-row'
  } else if (rowIndex === 3) {
    return 'success-row'
  }
  return ''
}

const tableData: User[] = [
  {
    date: '2023-05-03',
    title: 'Automatic Generation of Test Cases based on Bug Reports',
    abstract: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2023-11-02',
    title: 'Few-Shot Data-to-Text Generation via Unified Representation and Multi-Source Learning',
    abstract: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2022-012-04',
    title: 'Retrieval Augmented Chest X-Ray Report Generation using OpenAI GPT models',
    abstract: 'No. 189, Grove St, Los Angeles',
  },
  {
    date: '2024-01-01',
    title: 'You Can Generate It Again Data-to-text Generation with Verification and Correction Prompting',
    abstract: 'No. 189, Grove St, Los Angeles',
  },
]
</script>

<style>
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
