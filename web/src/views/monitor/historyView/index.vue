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
const padZero = (num) => {
  return num < 10 ? '0' + num : num
}

const initCharts = () => {
  const chartDom1 = document.getElementById('his_chart')
  let chartSpeedEnergy = echarts.init(chartDom1)
  //遍历出数值
  const reportTimeList = computed(() => {
    return motorAnalysisResult.value.map((row) => row.reportTime)
  })
  const rpmList = computed(() => {
    return motorAnalysisResult.value.map((row) => row.rpm)
  })
  const temperatureList = computed(() => {
    return motorAnalysisResult.value.map((row) => row.temperature)
  })
  // 速度数据
  const xFeaturesVelocity = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.velocity)
  })
  const yFeaturesVelocity = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.velocity)
  })
  const zFeaturesVelocity = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.velocity)
  })
  // 位移数据
  const xFeaturesDisplacement = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.displacement)
  })
  const yFeaturesDisplacement = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.displacement)
  })
  const zFeaturesDisplacement = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.displacement)
  })
  // 加速度数据
  const xFeaturesAcceleration = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.acceleration)
  })
  const yFeaturesAcceleration = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.acceleration)
  })
  const zFeaturesAcceleration = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.acceleration)
  })
  // 峰值数据
  const xFeaturesVelocityPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.velocityPeak)
  })
  const yFeaturesVelocityPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.acceleration)
  })
  const zFeaturesVelocityPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.velocityPeak)
  })
  // 加速度峰值数据
  const xFeaturesAccelerationPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.accelerationPeak)
  })
  const yFeaturesAccelerationPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.accelerationPeak)
  })
  const zFeaturesAccelerationPeak = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.accelerationPeak)
  })
  // 速度峭度
  const xFeaturesVelocityKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.velocityKurtosis)
  })
  const yFeaturesVelocityKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.velocityKurtosis)
  })
  const zFeaturesVelocityKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.velocityKurtosis)
  })
  // 加速度峭度
  const xFeaturesAccelerationKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.xFeatures.accelerationKurtosis)
  })
  const yFeaturesAccelerationKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.yFeatures.accelerationKurtosis)
  })
  const zFeaturesAccelerationKurtosis = computed(() => {
    return motorAnalysisResult.value.map((row) => row.zFeatures.accelerationKurtosis)
  })
  //console.log(xFeaturesVelocity.value)
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
      left: 'right',
      top: 'middle',
      orient: 'vertical',
      align: 'left',
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
      type: 'category',
      boundaryGap: false,
      data: reportTimeList.value,
      axisLabel: {
        formatter: function (value) {
          // 将时间戳转换为日期对象
          const dateObj = new Date(value)

          // 格式化日期时间
          const year = dateObj.getFullYear()
          const month = dateObj.getMonth() + 1
          const day = dateObj.getDate()
          const hours = dateObj.getHours()
          const minutes = dateObj.getMinutes()
          const seconds = dateObj.getSeconds()

          // 拼接格式化后的日期时间字符串
          const formattedDate = `${year}-${padZero(month)}-${padZero(day)} ${padZero(
            hours
          )}:${padZero(minutes)}:${padZero(seconds)}`

          return formattedDate
        },
      },
      // 根据数据自动调整 X 轴分隔线
      splitLine: {
        show: true,
      },
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '温度',
        type: 'line',
        stack: 'Total',
        data: temperatureList.value,
      },
      {
        name: '转速',
        type: 'line',
        stack: 'Total',
        data: rpmList.value,
      },
      {
        name: 'X轴速度',
        type: 'line',
        stack: 'Total',
        data: xFeaturesVelocity.value,
      },
      {
        name: 'Y轴速度',
        type: 'line',
        stack: 'Total',
        data: yFeaturesVelocity.value,
      },
      {
        name: 'Z轴速度',
        type: 'line',
        stack: 'Total',
        data: zFeaturesVelocity.value,
      },
      {
        name: 'X轴位移',
        type: 'line',
        stack: 'Total',
        data: xFeaturesDisplacement.value,
      },
      {
        name: 'Y轴位移',
        type: 'line',
        stack: 'Total',
        data: yFeaturesDisplacement.value,
      },
      {
        name: 'Z轴位移',
        type: 'line',
        stack: 'Total',
        data: zFeaturesDisplacement.value,
      },
      {
        name: 'X轴加速度',
        type: 'line',
        stack: 'Total',
        data: xFeaturesAcceleration.value,
      },
      {
        name: 'Y轴加速度',
        type: 'line',
        stack: 'Total',
        data: yFeaturesAcceleration.value,
      },
      {
        name: 'Z轴加速度',
        type: 'line',
        stack: 'Total',
        data: zFeaturesAcceleration.value,
      },
      {
        name: 'X轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: xFeaturesVelocityPeak.value,
      },
      {
        name: 'Y轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: yFeaturesVelocityPeak.value,
      },
      {
        name: 'Z轴速度峰值',
        type: 'line',
        stack: 'Total',
        data: zFeaturesVelocityPeak.value,
      },
      {
        name: 'X轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: xFeaturesAccelerationPeak.value,
      },
      {
        name: 'Y轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: yFeaturesAccelerationPeak.value,
      },
      {
        name: 'Z轴加速度峰值',
        type: 'line',
        stack: 'Total',
        data: zFeaturesAccelerationPeak.value,
      },
      {
        name: 'X轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: xFeaturesVelocityKurtosis.value,
      },
      {
        name: 'Y轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: yFeaturesVelocityKurtosis.value,
      },
      {
        name: 'Z轴速度峭值',
        type: 'line',
        stack: 'Total',
        data: zFeaturesVelocityKurtosis.value,
      },
      {
        name: 'X轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: xFeaturesAccelerationKurtosis.value,
      },
      {
        name: 'Y轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: yFeaturesAccelerationKurtosis.value,
      },
      {
        name: 'Z轴加速度峭值',
        type: 'line',
        stack: 'Total',
        data: zFeaturesAccelerationKurtosis.value,
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

const motorAnalysisResult = ref([])

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
    <div id="his_chart" style="width: 100%; height: 700px; background: white"></div>
  </NModal>
</template>

<style scoped></style>
