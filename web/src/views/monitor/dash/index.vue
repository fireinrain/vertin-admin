<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NModal } from 'naive-ui'
import * as echarts from 'echarts'
import { useMessage } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import api from '@/api'

defineOptions({ name: '历史图表' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const showModal = ref(false)
const chartData = ref([])
const chartInstance = ref(null)
const selectedRowId = ref(null)
const message = useMessage()

onMounted(() => {
  $table.value?.handleSearch()
})

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
                selectedRowId.value = row.id
                fetchChartData(row.sn)
                showModal.value = true
              },
            },
            {
              default: () => '查看图表',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/monitor/dash/detail']]
        ),
      ]
    },
  },
]

const fetchChartData = async (sn) => {
  try {
    const response = await api.getMonitorHisDetail({ sn: sn })
    chartData.value = response.data
    setTimeout(() => {
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }
      const chartDom = document.getElementById('his_chart')
      chartInstance.value = echarts.init(chartDom)
      const option = {
        xAxis: {
          type: 'category',
          data: chartData.value.map((item) => item.time),
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: chartData.value.map((item) => item.value),
            type: 'line',
          },
        ],
      }
      chartInstance.value.setOption(option)
    }, 0)
  } catch (error) {
    message.error('获取图表数据失败')
  }
}

const handleCloseModal = () => {
  showModal.value = false
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
}
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="数据图表">
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getMonitorSetsList"
    />
  </CommonPage>

  <!-- 模态框 -->
  <NModal v-model:show="showModal" title="历史数据图表" size="large" @close="handleCloseModal">
    <div id="his_chart" style="width: 95%; height: 600px"></div>
  </NModal>
</template>

<style scoped>
#his_chart {
  background: white;
}
</style>
