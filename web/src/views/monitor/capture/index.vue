<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NSelect, NInputNumber } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'

defineOptions({ name: '数据采集配置' })

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
  name: '监控配置',
  initForm: {
    sn: '',
    api_url: '',
    fetch_interval: '',
    enable: 'true',
  },
  doCreate: api.createMonitorSet,
  doUpdate: api.updateMonitorSet,
  doDelete: api.deleteMonitorSet,
  refresh: () => $table.value?.handleSearch(),
})

// Define options for the "是否开启" select
const enableOptions = [
  { label: '开启', value: 'true' },
  { label: '关闭', value: 'false' },
]

async function handleRefreshMonitorSet() {
  await $dialog.confirm({
    title: '提示',
    type: 'warning',
    content: '此操作会根据后台任务更新，确定继续刷新 监控配置 操作？',
    async confirm() {
      await api.refreshMonitorSet()
      $message.success('刷新完成')
      $table.value?.handleSearch()
    },
  })
}

onMounted(() => {
  $table.value?.handleSearch()
})

const addMonitorSetRules = {
  sn: [
    {
      required: true,
      message: '请输入SN编码',
      trigger: ['input', 'blur'],
    },
  ],
  api_url: [
    {
      required: true,
      message: '请输入采集api地址',
      trigger: ['input', 'blur'],
    },
  ],
  fetch_interval: [
    {
      required: true,
      message: '请输入采集间隔',
      type: 'number',
      trigger: ['input', 'blur'],
    },
  ],
  enable: [
    {
      required: true,
      message: '请选择是否开启',
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
    title: 'SN编码',
    key: 'sn',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '采集地址',
    key: 'api_url',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '采集间隔(S)',
    key: 'fetch_interval',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '开启状态',
    key: 'enable',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return row.enable === 'true' ? '开启' : '关闭'
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
                handleEdit(row)
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/monitor/capture/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ monitorset_id: row.id }, false),
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
                [[vPermission, 'delete/api/v1/monitor/capture/delete']]
              ),
            default: () => h('div', {}, '确定删除该API吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="数据采集">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/monitor/capture/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建数据采集
        </NButton>
        <NButton
          v-permission="'post/api/v1/monitor/capture/refresh'"
          class="float-right mr-15"
          type="warning"
          @click="handleRefreshMonitorSet"
        >
          <TheIcon icon="material-symbols:refresh" :size="18" class="mr-5" />刷新后台任务
        </NButton>
      </div>
    </template>
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getMonitorSets"
    >
      <template #queryBar>
        <QueryBarItem label="SN编码" :label-width="50">
          <NInput
            v-model:value="queryItems.sn"
            clearable
            type="text"
            placeholder="请输入SN编码"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="采集地址" :label-width="60">
          <NInput
            v-model:value="queryItems.api_url"
            clearable
            type="text"
            placeholder="请输入采集地址"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="采集间隔" :label-width="60">
          <NInputNumber
            v-model:value="queryItems.fetch_interval"
            clearable
            type="number"
            placeholder="请输入采集间隔"
            @keypress.enter="$table?.handleSearch()"
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
        :rules="addMonitorSetRules"
      >
        <NFormItem label="SN编码" path="sn">
          <NInput v-model:value="modalForm.sn" clearable placeholder="请输入SN编码" />
        </NFormItem>
        <NFormItem label="采集地址" path="api_url">
          <NInput v-model:value="modalForm.api_url" clearable placeholder="请输入采集地址" />
        </NFormItem>
        <NFormItem label="采集间隔" path="fetch_interval">
          <NInputNumber
            v-model:value="modalForm.fetch_interval"
            clearable
            placeholder="请输入采集间隔"
          />
        </NFormItem>
        <NFormItem label="是否开启" path="enable">
          <NSelect
            v-model:value="modalForm.enable"
            :options="enableOptions"
            clearable
            placeholder="请选择是否开启"
          />
        </NFormItem>
        <NFormItem label="保存提示:">
          <span>修改数据采集数据需要再次点击刷新后台任务触发生效.</span>
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
