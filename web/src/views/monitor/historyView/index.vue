<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives, computed } from 'vue'
import { NButton, NModal } from 'naive-ui'
import { useMessage } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import api from '@/api'
import * as echarts from 'echarts'

defineOptions({ name: '历史图表' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const showModal = ref(false)
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
              default: () => '查看历史图表',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/monitor/dash/detail']]
        ),
      ]
    },
  },
]
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  const formattedTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
  return formattedTime
}
const fetchChartData = async (sn) => {
  try {
    const response = await api.getMonitorHisDetail({ sn: sn })
    let datas = response.data
    setTimeout(() => {
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }
      for (let i = 0; i < datas.length; i++) {
        const obj = datas[i]
        let d = obj.content
        let valueList = parseIntStrToValue(d)
        let analysisInTime = {
          xFeatures: {},
          yFeatures: {},
          zFeatures: {},
          temperature: undefined,
          rpm: undefined,
          reportTime: undefined,
        }

        analysisInTime.reportTime = formatTimestamp(obj.report_time)
        let items = ['xFeatures', 'yFeatures', 'zFeatures']
        for (const [index, key] of items.entries()) {
          analysisInTime[key]['velocity'] = valueList[index]
          analysisInTime[key]['displacement'] = valueList[3 + index]
          analysisInTime[key]['acceleration'] = valueList[6 + index]
          analysisInTime[key]['velocityPeak'] = valueList[9 + index]
          analysisInTime[key]['accelerationPeak'] = valueList[12 + index]
          analysisInTime[key]['velocityKurtosis'] = valueList[15 + index]
          analysisInTime[key]['accelerationKurtosis'] = valueList[18 + index]
          analysisInTime[key]['velocitySpectrum'] = valueList.slice(
            21 + index * 8,
            21 + index * 8 + 8
          )
          analysisInTime[key]['accelerationSpectrum'] = valueList.slice(
            45 + index * 8,
            45 + index * 8 + 8
          )
        }
        analysisInTime['zFeatures']['rotateVelocitySpectrum'] = valueList.slice(68, 76)
        analysisInTime.temperature = valueList[77]
        analysisInTime.rpm = valueList[78] * 6
        motorAnalysisResult.value.push(analysisInTime)
      }

      initCharts()
    }, 100)
  } catch (error) {
    message.error('获取图表数据失败')
  }
}

const initCharts = () => {
  const chartDom1 = document.getElementById('his_chart')
  let chartSpeedEnergy = echarts.init(chartDom1)
  //遍历出数值
  const reportTimeList = computed(() => {
    return motorAnalysisResult.value.map((row) =>
      row.reportTime
    )
  })
  console.log(reportTimeList.value)
  chartSpeedEnergy.setOption({
    title: {
      text: '监控历史图表',
    },
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: [
        '温度',
        '转速',
        'X轴速度',
        'Y轴速度',
        'Z轴速度',
        'X轴位移',
        'Y轴位移',
        'Z轴位移',
        'X轴加速度',
        'Y轴加速度',
        'Z轴加速度',
        'X轴速度峰值',
        'Y轴速度峰值',
        'Z轴速度峰值',
        'X轴加速度峰值',
        'Y轴加速度峰值',
        'Z轴加速度峰值',
        'X轴速度峭值',
        'Y轴速度峭值',
        'Z轴速度峭值',
        'X轴加速度峭值',
        'Y轴加速度峭值',
        'Z轴加速度峭值',
      ],
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    xAxis: {
      type: 'time',
      boundaryGap: false,
      data: ['2024-05-24T12:34:56', '2025-05-24T12:34:56', '2028-05-24T12:34:56'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '温度',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: '转速',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'X轴速度',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'Y轴速度',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'Z轴速度',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'X轴位移',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'Y轴位移',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'Z轴位移',
        type: 'line',
        stack: 'Total',
        data: [120, 132, 139, 140, 141, 230, 235],
      },
      {
        name: 'X轴加速度',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Y轴加速度',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Z轴加速度',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'X轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Y轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Z轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'X轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Y轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Z轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'X轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Y轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Z轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'X轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Y轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
      {
        name: 'Z轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: [111, 121, 143, 143, 143, 143, 143],
      },
    ],
  })
}
const parseIntStrToValue = (str) => {
  let valueList = []
  for (let i = 0; i < str.length; i += 4) {
    let valueStr = '0x' + str[i + 2] + str[i + 3] + str[i] + str[i + 1]
    const value = parseInt(valueStr) / 10
    valueList.push(value)
  }
  return valueList
}

const motorAnalysisResult = ref([
])

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
    <div id="his_chart" style="width: 90%; height: 700px; background: white"></div>
  </NModal>
</template>

<style scoped></style>
