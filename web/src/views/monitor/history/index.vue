<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NDatePicker } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'

defineOptions({ name: '历史数据' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '监控记录',
  initForm: {},
  doCreate: api.createMonitor,
  doUpdate: api.updateMonitor,
  doDelete: api.deleteMonitor,
  refresh: () => $table.value?.handleSearch(),
})
const handleEditWithDataConversion = (rowData) => {
  // Perform date string to date object conversion here
  const convertedData = {
    ...rowData,
    report_time: new Date(rowData.report_time).getTime(), // Convert reportTime to date object
    start_time: new Date(rowData.start_time).getTime(), // Convert startTime to date object
    end_time: new Date(rowData.end_time).getTime(), // Convert endTime to date object
  }

  // Pass the converted data to handleEdit function
  handleEdit(convertedData)
}

onMounted(() => {
  $table.value?.handleSearch()
})

const addHistoryRules = {
  sn: [
    {
      required: true,
      message: '请输入SN编号',
      trigger: ['input', 'blur'],
    },
  ],
  content: [
    {
      required: true,
      message: '请输入监控数据',
      trigger: ['input', 'blur'],
    },
  ],
  report_time: [
    {
      required: true,
      type: 'date',
      message: '请选择上报时间',
      trigger: ['change', 'blur'],
    },
  ],
  start_time: [
    {
      required: true,
      type: 'date',
      message: '请选择起始时间',
      trigger: ['change', 'blur'],
    },
  ],
  end_time: [
    {
      required: true,
      type: 'date',
      message: '请选择结束时间',
      trigger: ['change', 'blur'],
    },
  ],
}

const columns = [
  {
    title: 'ID编号',
    key: 'id',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'SN编号',
    key: 'sn',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '上报数据',
    key: 'content',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '上报时间',
    key: 'report_time',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return new Date(row.report_time).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
    },
  },
  {
    title: '起始时间',
    key: 'start_time',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return row.start_time
        ? new Date(row.start_time).toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          })
        : 'N/A'
    },
  },
  {
    title: '结束时间',
    key: 'end_time',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return row.end_time
        ? new Date(row.end_time).toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          })
        : 'N/A'
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEditWithDataConversion(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/monitor/v1/api/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ monitor_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/monitor/delete']]
              ),
            default: () => h('div', {}, '确定删除该历史记录吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="监控历史列表">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/monitor/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建历史记录
        </NButton>
      </div>
    </template>
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getMonitors"
    >
      <template #queryBar>
        <QueryBarItem label="SN编号" :label-width="50">
          <NInput
            v-model:value="queryItems.sn"
            clearable
            type="text"
            placeholder="请输入SN编号"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="起始时间" :label-width="60">
          <NDatePicker
            v-model:value="queryItems.start_time"
            clearable
            type="datetime"
            placeholder="请输入起始时间"
            @update:value="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="结束时间" :label-width="60">
          <NDatePicker
            v-model:value="queryItems.end_time"
            clearable
            type="datetime"
            placeholder="请输入结束时间"
            @update:value="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="addHistoryRules"
      >
        <NFormItem label="SN编号" path="sn">
          <NInput v-model:value="modalForm.sn" clearable placeholder="请输入SN编号" />
        </NFormItem>
        <NFormItem label="上报数据" path="content">
          <NInput v-model:value="modalForm.content" clearable placeholder="请输入上报数据" />
        </NFormItem>
        <NFormItem label="上报时间" path="report_time">
          <NDatePicker
            v-model:value="modalForm.report_time"
            type="datetime"
            clearable
            placeholder="请输入上报时间"
            @update:value="modalFormRef.value?.validateField('report_time')"
          />
        </NFormItem>
        <NFormItem label="起始时间" path="start_time">
          <NDatePicker
            v-model:value="modalForm.start_time"
            type="datetime"
            clearable
            placeholder="请输入起始时间"
            @update:value="modalFormRef.value?.validateField('start_time')"
          />
        </NFormItem>
        <NFormItem label="结束时间" path="end_time">
          <NDatePicker
            v-model:value="modalForm.end_time"
            type="datetime"
            clearable
            placeholder="请输入结束时间"
            @update:value="modalFormRef.value?.validateField('end_time')"
          />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
