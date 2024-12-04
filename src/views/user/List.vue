<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <h1>📃智能报告生成‍🚀</h1>
      </el-header>

      <el-main>
        <el-row :gutter="20">
          <!-- 上传和参数设置 -->
          <el-col :span="8">

            <el-card>
              <h2>上传文件</h2>

              <el-upload
                ref="uploadRef"
                class="upload-demo"
                drag
                action="http://localhost:5000/upload"
                multiple
                :file-list="fileList"
                :on-success="handleSuccess"
                :on-error="handleError"
                :auto-upload="false"
              >
                <el-icon><upload-filled /></el-icon>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
              </el-upload>
              <div class="button-group">
                <el-button type="primary" @click="submitUpload">确认上传</el-button>

                <el-button @click="clearFiles">清空</el-button>
              </div>
            </el-card>

                        <el-card>
              <h2>知识库文件</h2>
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
              <el-table-column prop="title" label="文件" />
<!--              <el-table-column prop="date" label="时间" />-->
              <el-table-column label="操作" >
                <template #default="scope">
                  <el-button
                    type="primary"
                    size="mini"
                    @click="selectFileGenerate(scope.row)"
                  >
                    选择
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
            </el-card>

            <el-card style="margin-top: 20px;">
              <h2>参数设置</h2>
              <el-form label-width="80px">
                <el-form-item label="关键词">
                  <el-input
                    placeholder="输入自定义关键词（可选）"
                    v-model="keywords"
                  ></el-input>
                </el-form-item>
                <el-form-item label="提示词">
                  <el-input
                    placeholder="输入自定义提示词（可选）"
                    v-model="prompts"
                  ></el-input>
                </el-form-item>
                <el-form-item label="思维链">
                  <el-input
                    placeholder="输入自定义思维链（可选）"
                    v-model="cot"
                  ></el-input>
                </el-form-item>

                <el-form-item label="语言">
                  <el-select
                    placeholder="请选择语言"
                    v-model="language"
                  >
                    <el-option label="简体中文" value="zh"></el-option>
                    <el-option label="English" value="en"></el-option>
                    <el-option label="日本語" value="jp"></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item>
                  <div class="button-container">
                    <el-button
                      type="success"
                      @click="generateReport"
                      :disabled="!filePath"
                    >
                      生成报告
                    </el-button>

                    <PromptSelector />
                  </div>
                </el-form-item>
              </el-form>
            </el-card>


            <el-card>
             <div style="margin: 10px">
    <div style="width: 100%; display: flex; flex-direction: row">
      <div style="margin-right: 4px">
        <el-upload
          ref="uploadRef"
          multiple
          :auto-upload="false"
          :show-file-list="false"
          v-model:file-list="uploadFileList"
          :on-change="uploadFileChange"
        >
          <template #trigger>
            <el-button size="small" @click="openUploadFile($event, null)"
              >上传文件</el-button
            >
          </template>
        </el-upload>
      </div>
      <div style="margin-right: 4px">
        <el-button size="small" @click="openInsertFile($event, null)">
          添加文件
        </el-button>
      </div>
      <div style="margin-right: 4px">
        <el-button size="small" @click="openInsertFolder($event, null)">
          添加文件夹
        </el-button>
      </div>
    </div>
  </div>
  <el-tree
    style="max-width: 600px"
    empty-text="没有文件，快去上传吧!"
    :allow-drop="allowDrop"
    :allow-drag="allowDrag"
    :data="dataSource"
    draggable
    default-expand-all
    node-key="id"
    highlight-current
    @node-drag-start="handleDragStart"
    @node-drag-enter="handleDragEnter"
    @node-drag-leave="handleDragLeave"
    @node-drag-over="handleDragOver"
    @node-drag-end="handleDragEnd"
    @node-drop="handleDrop"
  >
    <template #default="scope">
      <div style="width: 100%; display: flex; justify-content: space-between">
        <div style="display: flex; justify-content: left">
          <div
            style="
              display: flex;
              flex-direction: column;
              justify-content: center;
            "
            v-if="scope.node.data.type === 'folder'"
          >
            <!-- 文件夹展示 -->
            <el-icon><Folder /></el-icon>
          </div>
          <div v-else>
            <!-- 文件展示 -->
            <el-icon><Document /></el-icon>
          </div>
          <div style="margin-left: 3px">{{ scope.node.label }}</div>
        </div>
        <div style="margin-right: 20px">
          <el-popover placement="right" trigger="hover">
            <template #reference>
              <el-icon><Tools /></el-icon>
            </template>
            <div class="but-list" style="display: flex; flex-direction: column">
              <div v-if="scope.node.data.type === 'folder'">
                <el-upload
                  ref="uploadRef"
                  multiple
                  :auto-upload="false"
                  :show-file-list="false"
                  v-model:file-list="uploadFileList"
                  :on-change="uploadFileChange"
                >
                  <template #trigger>
                    <el-button
                      style="width: 124px"
                      @click="openUploadFile($event, scope.node)"
                      >上传文件</el-button
                    >
                  </template>
                </el-upload>
              </div>

              <div v-if="scope.node.data.type === 'folder'" style="width: 100%">
                <el-button
                  style="width: 100%"
                  @click="openInsertFile($event, scope.node)"
                >
                  添加文件
                </el-button>
              </div>
              <div v-if="scope.node.data.type === 'folder'" style="width: 100%">
                <el-button
                  style="width: 100%"
                  @click="openInsertFolder($event, scope.node)"
                  >添加文件夹</el-button
                >
              </div>
              <div style="width: 100%">
                <el-button
                  style="width: 100%"
                  @click="openUpdate($event, scope.node)"
                >
                  修改
                </el-button>
              </div>
              <div style="width: 100%">
                <el-button
                  style="width: 100%"
                  @click="openDelete($event, scope.node)"
                  >删除</el-button
                >
              </div>
            </div>
          </el-popover>
        </div>
      </div>
    </template>
  </el-tree>

  <!-- 新增和修改文件 文件夹名称使用 -->
  <el-dialog
    v-model="fileDialogVisible"
    :title="dialogTitle"
    width="500"
    :before-close="handleClose"
    draggable
    class="rounded-dialog"
  >
    当前文件路径: {{ dialogPath }}
    <div style="display: flex; justify-content: center; margin-top: 10px">
      <el-input v-model="dialogData" placeholder="Please input" />
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="cancel">取消</el-button>
        <el-button type="primary" @click="confirm"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog
    v-model="deleteDialogVisible"
    title="删除"
    width="500"
    draggable
    class="rounded-dialog"
  >
    你确定要删除该文件吗？
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="cancel">取消</el-button>
        <el-button type="primary" @click="deleteFileOrFolder"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
</el-card>



          </el-col>



          <!-- 报告显示 -->
          <el-col :span="16">
            <el-card>
              <div class="report-container">
                            <el-skeleton v-if="!paginatedContent.length" :rows="16" animated />
                <el-button
                  type="primary"
                  v-if="paginatedContent.length"
                  @click="printPDF"
                  icon="Download"
                  style="float: right; margin-bottom: 10px;"
                >
                  导出 PDF
                </el-button>

                <div
                  v-for="content in paginatedContent"
                  :key="content"
                  class="report-output"
                  v-html="content"
                  id="report-html"
                ></div>

                <el-pagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="[1, 5, 10]"
                  :page-size="1"
                  layout="prev, pager, next"
                  :total="totalItems"
                  @current-change="handleCurrentChange"
                />
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>

</template>

<script setup lang="ts">

import { VueMermaidRender } from 'vue-mermaid-render'
import { UploadFilled } from '@element-plus/icons-vue';
import { ref, computed,onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { paper_report,document_list } from '@/apis/report/paper';
import type Node from "element-plus/es/components/tree/src/model/node";
import type { DragEvents } from "element-plus/es/components/tree/src/model/useDragNode";
import type {
  AllowDropType,
  NodeDropType,
} from "element-plus/es/components/tree/src/tree.type";
import PromptSelector from '@/components/PromptSelector.vue';


const uploadRef = ref(null);
const fileList = ref([]);
const htmlContent = ref([]);
const filePath = ref('');
const keywords = ref('');
const prompts = ref('');
const cot = ref('');
const language = ref('zh');

const currentPage = ref(1);
const pageSize = ref(1);

const totalItems = computed(() => htmlContent.value.length);

const paginatedContent = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  return htmlContent.value.slice(startIndex, endIndex);
});

const handleSuccess = (response, file, fileList) => {
  filePath.value = response.file_path;
  ElMessage.success('上传成功！');
};

const handleError = (err, file, fileList) => {
  ElMessage.error('上传失败：' + err.message);
};

const submitUpload = () => {
  if (uploadRef.value) {
    uploadRef.value.submit();
  }
};

const clearFiles = () => {
  fileList.value = [];
};

const paper_reporting = (form) => {
  paper_report(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg);
      htmlContent.value = res.data.data.report_html;
      filePath.value = '';
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

const generateReport = () => {
  if (filePath.value) {
    const formData = new FormData();
    formData.append('file_path', filePath.value);
    formData.append('keywords', keywords.value);
    formData.append('prompts', prompts.value);
    formData.append('cot', cot.value);
    formData.append('language', language.value);
    paper_reporting(formData);
  }
};




const handleCurrentChange = (val) => {
  currentPage.value = val;
};

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

  // 打印功能
  const printContent = document.getElementById('report-html').innerHTML;
  const printWindow = window.open('', '_blank');
  printWindow.document.write(printStyle + printContent);
  printWindow.document.close();
  printWindow.print();
};




const handleDragStart = (node: Node, ev: DragEvents) => {
  console.log("drag start", node);
};
const handleDragEnter = (
  draggingNode: Node,
  dropNode: Node,
  ev: DragEvents
) => {
  console.log("tree drag enter:", dropNode.label);
};
const handleDragLeave = (
  draggingNode: Node,
  dropNode: Node,
  ev: DragEvents
) => {
  console.log("tree drag leave:", dropNode.label);
};

const handleDragOver = (draggingNode: Node, dropNode: Node, ev: DragEvents) => {
  console.log("tree drag over:", dropNode.label);
};

const handleDragEnd = (
  draggingNode: Node,
  dropNode: Node,
  dropType: NodeDropType,
  ev: DragEvents
) => {
  console.log(
    "tree drag end:",
    draggingNode.data.label,
    dropNode && dropNode.label,
    dropType
  );
};
const handleDrop = (
  draggingNode: Node,
  dropNode: Node,
  dropType: NodeDropType,
  ev: DragEvents
) => {
  console.log("tree drop:", dropNode.label, dropType);
};
const allowDrop = (draggingNode: Node, dropNode: Node, type: AllowDropType) => {
  return dropNode.data.type === "folder";
};
const allowDrag = (draggingNode: Node) => {
  console.log("allowDrag");
  return !draggingNode.data.label.includes("Level three 3-1-1");
};

const dataSource = ref([
  {
    label: "Level one 1",
    type: "folder",
    path: "/Level one 1",
    children: [
      {
        label: "Level two 1-1",
        type: "folder",
        path: "/Level one 1/Level two 1-1",
        children: [
          {
            type: "file",
            path: "/Level one 1/Level three 1-1-1/Level three 1-1-1",
            label: "Level three 1-1-1",
          },
        ],
      },
    ],
  },
]);

const fileDialogVisible = ref(false);
const dialogTitle = ref(""); // 新增文件|文件夹,修改
const dialogData = ref("");
const dialogPath = ref("/");
const deleteDialogVisible = ref(false);
const fileOrFolderNode = ref();

const handleClose = (done: () => void) => {
  cancel();
  done();
};

/**
 * 取消
 */
const cancel = () => {
  fileDialogVisible.value = false;
};

/**
 * 确定
 */
const confirm = () => {
  console.log("confirm: ", fileOrFolderNode);
  if (dialogTitle.value === "新增文件" || dialogTitle.value === "新建文件夹") {
    let data = {
      label: dialogData.value,
      type: "",
      children: [],
      path: "/" + dialogData.value,
    };
    if (fileOrFolderNode.value) {
      data.path = fileOrFolderNode.value.data.path + "/" + dialogData.value;
    }
    if (dialogTitle.value === "新增文件") {
      data.type = "file";
    } else {
      data.type = "folder";
    }
    append(fileOrFolderNode.value, data);
  } else {
    // 修改处理
    let parent = null;
    let data = {
      label: dialogData.value,
      type: fileOrFolderNode.value.data.type,
      children: fileOrFolderNode.value.data.children,
      path: "/" + dialogData.value,
    };
    if (fileOrFolderNode.value.parent.level != 0) {
      parent = fileOrFolderNode.value.parent;
      data.path = parent.data.path + "/" + data.label;
    }
    updateTreeNode(parent, fileOrFolderNode.value.data, data);
  }
  fileDialogVisible.value = false;
};

const openInsertFile = (even, node) => {
  if (node) {
    dialogPath.value = node.data.path + "/";
  } else {
    dialogPath.value = "/";
  }
  dialogTitle.value = "新增文件";
  dialogData.value = "";
  fileOrFolderNode.value = node;
  fileDialogVisible.value = true;
};

/**
 * 开始修改
 * @param even
 * @param node
 */
const openUpdate = (even, node) => {
  if (node) {
    dialogPath.value = node.data.path;
  } else {
    dialogPath.value = "/";
  }
  fileDialogVisible.value = true;
  fileOrFolderNode.value = node;
  dialogData.value = fileOrFolderNode.value.data.label;
  dialogTitle.value = "修改";
};

const openInsertFolder = (even, node) => {
  if (node) {
    dialogPath.value = node.data.path;
  } else {
    dialogPath.value = "/";
  }
  dialogData.value = "";
  fileOrFolderNode.value = node;
  dialogTitle.value = "新建文件夹";
  fileDialogVisible.value = true;
};

const openDelete = (even, node) => {
  fileOrFolderNode.value = node;
  deleteDialogVisible.value = true;
};

const deleteFileOrFolder = (even) => {
  // 删除该文件
  remove(fileOrFolderNode.value, fileOrFolderNode.value.data);
  deleteDialogVisible.value = false;
};

/**
 * 添加
 * @param node 父节点
 * @param data 要添加的数据
 */
const append = (node, data) => {
  if (isNameDuplicate(node, null, data)) {
    ElMessage.error("文件名重复");
    return;
  }
  const newChild = data;
  if (node) {
    if (!node.data.children) {
      node.data.children = [];
    }
    node.data.children.push(newChild);
  } else {
    dataSource.value.push(newChild);
  }
};

/**
 * 删除
 * @param node 节点
 * @param data 数据
 */
const remove = (node: Node, data) => {
  console.log("all data:", dataSource.value);
  const parent = node.parent;
  const children = parent.data.children || parent.data;
  const index = children.findIndex((d) => d.path === data.path);
  children.splice(index, 1);
  dataSource.value = [...dataSource.value];
};

const updateTreeNode = (parentNode, oldData, newData) => {
  console.log(
    "parentNode:",
    parentNode,
    "oldData:",
    oldData,
    "newData:",
    newData
  );
  if (isNameDuplicate(parentNode, oldData, newData)) {
    ElMessage.error("文件名重复");
    return;
  }
  let index: number;
  if (parentNode && parentNode.data) {
    // 查找 newData.path 在 parentNode.data.children 中的索引
    index = parentNode.data.children.findIndex(
      (child) => child.path === oldData.path
    );
    // 如果找到索引，则更新该位置的数据
    if (index !== -1) {
      parentNode.data.children[index] = newData;
    } else {
      console.error(
        "找不到, index:",
        index,
        "parentNode.data",
        parentNode.data,
        "newData",
        newData
      );
    }
  } else {
    index = dataSource.value.findIndex((item) => item.path === oldData.path);
    // 如果找到索引，则更新该位置的数据
    if (index !== -1) {
      dataSource.value[index] = newData;
    } else {
      console.error(
        "找不到, index:",
        index,
        "parentNode.data",
        parentNode.data,
        "newData",
        newData
      );
    }
  }

  console.log(dataSource.value);
};

/**
 * 判断名称是否有相同的
 */
const isNameDuplicate = (parentNode, oldData, newData) => {
  console.log(
    "parentNode:",
    parentNode,
    "oldData:",
    oldData,
    "newData: ",
    newData
  );
  if (oldData && oldData.label === newData.label) return false;
  if (parentNode) {
    for (let i = 0; i < parentNode.data.children.length; i++) {
      const child = parentNode.data.children[i];
      if (child.label === newData.label) {
        return true;
      }
    }
  } else {
    for (let i = 0; i < dataSource.value.length; i++) {
      const child = dataSource.value[i];
      if (child.label === newData.label) {
        return true;
      }
    }
  }

  return false;
};

/**
 * 文件上传操作
 */
const uploadFileList = ref([]);

const openUploadFile = (even, node) => {
  if (node) {
    dialogPath.value = node.data.path;
  } else {
    dialogPath.value = "/";
  }
  fileOrFolderNode.value = node;
};

const uploadFileChange = (uploadFile, uploadFiles) => {
  let data = {
    label: uploadFile.name,
    type: "file",
    path: "/" + uploadFile.name,
    uid: uploadFile.uid,
  };
  if (fileOrFolderNode.value) {
    data.path = fileOrFolderNode.value.data.path + "/" + uploadFile.name;
  }
  append(fileOrFolderNode.value, data);
};
function flattenTree(trees) {
  const result = [];

  function traverse(node) {
    // 添加当前节点到结果数组
    result.push({
      label: node.label,
      type: node.type,
      path: node.path,
    });

    // 如果节点有children，则递归遍历它们
    if (Array.isArray(node.children)) {
      node.children.forEach(traverse);
    }
  }

  // 遍历输入的树数组
  trees.forEach((tree) => {
    traverse(tree); // 从每个树的根节点开始遍历
  });

  // 返回结果数组
  return result;
}

console.log("dataSource.value:", dataSource.value);
console.log("result:", flattenTree(dataSource.value));



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
const pageSizeDoc = ref(3); // 每页条数
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
const selectFileGenerate = (row: Document) => {
  console.log('Preview button clicked:', row.title);
  const filePath = `./uploads/docs/${row.title}`;
  if (row.title.endsWith('.pdf')) {
    const formData = new FormData();
    formData.append('file_path', filePath);
    formData.append('keywords', keywords.value);
    formData.append('language', language.value);
    paper_reporting(formData);
    console.log('selectFileGenerate set to:', formData.get('file_path'));
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
.common-layout {
  //background-color: #f5f7fa;
}

h1 {
  //color: #303133;
  font-size: 24px;
  margin: 0;
  padding: 20px 0;
  text-align: center;
}

h2 {
  font-size: 18px;
  margin-bottom: 20px;
}

.upload-demo {
  width: 100%;
  margin-bottom: 20px;
}

.el-upload__text {
  margin-top: 10px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.report-container {
  position: relative;
  min-height: 400px;
}

.report-output {
  margin-bottom: 20px;
}

#report-html {
  padding: 20px;
  background-color: #fff;
  border-radius: 6px;
}

.el-footer {
  background-color: #f5f7fa;
  line-height: 60px;
}

.el-pagination {
  text-align: center;
  margin-top: 20px;
}

.rounded-dialog {
  border-radius: 10px;
}

.button-container {
  display: flex;
  justify-content: space-between; /* 子元素间距自动分配 */
  width: 100%; /* 父容器宽度为 100% */
}

.but-list > div {
  margin: 2px;
}
</style>
