<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NModal } from 'naive-ui'
import { useMessage } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import api from '@/api'
import * as echarts from 'echarts'

defineOptions({ name: '即时图表' })

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
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  const formattedTime = `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`
  return formattedTime
}
const fetchChartData = async (sn) => {
  try {
    const response = await api.getMonitorHisDetail({ sn: sn })
    let latestData = response.data[response.data.length - 1]
    let data = latestData.content
    setTimeout(() => {
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }
      let valueList = parseIntStrToValue(data)
      let analysisInTime = {
        xFeatures: {},
        yFeatures: {},
        zFeatures: {},
        temperature: undefined,
        rpm: undefined,
        reportTime: undefined,
      }

      analysisInTime.reportTime = formatTimestamp(latestData.report_time)
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
      motorAnalysisResult.value = analysisInTime
      initCharts()
    }, 100)
  } catch (error) {
    message.error('获取图表数据失败')
  }
}

const initCharts = () => {
  const chartDom1 = document.getElementById('speedEnergyChart')
  let chartSpeedEnergy = echarts.init(chartDom1)
  chartSpeedEnergy.setOption({
    title: {
      text: '三轴速度谱 (单位: J/HZ)',
      textStyle: {
        fontWeight: 'normal',
      },
      left: 'center',
    },
    legend: {
      data: ['X轴', 'Y轴', 'Z轴'],
      left: 50,
    },
    xAxis: {
      name: '频带',
      data: [0.5, 1, 1.5, 2, 3, 4, 5, 6],
    },
    yAxis: {
      type: 'value',
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b0}倍频: {c0} J/HZ',
    },
    series: [
      {
        name: 'X轴',
        type: 'bar',
        data: motorAnalysisResult.value.xFeatures.velocitySpectrum,
      },
      {
        name: 'Y轴',
        type: 'bar',
        data: motorAnalysisResult.value.yFeatures.velocitySpectrum,
      },
      {
        name: 'Z轴',
        type: 'bar',
        data: motorAnalysisResult.value.zFeatures.velocitySpectrum,
      },
    ],
  })
  const chartDom2 = document.getElementById('speedChart')
  let chartSpeed = echarts.init(chartDom2)
  chartSpeed.setOption({
    title: {
      text: '三轴加速度谱 (单位: J/HZ)',
      textStyle: {
        fontWeight: 'normal',
      },
      left: 'center',
    },
    legend: {
      data: ['X轴', 'Y轴', 'Z轴'],
      left: 50,
    },
    xAxis: {
      name: '频带',
      data: [0.5, 1, 1.5, 2, 3, 4, 5, 6],
    },
    yAxis: {},
    tooltip: {
      trigger: 'item',
      formatter: '{b0}倍频: {c0} J/HZ',
    },
    series: [
      {
        name: 'X轴',
        type: 'bar',
        data: motorAnalysisResult.value.xFeatures.accelerationSpectrum,
      },
      {
        name: 'Y轴',
        type: 'bar',
        data: motorAnalysisResult.value.yFeatures.accelerationSpectrum,
      },
      {
        name: 'Z轴',
        type: 'bar',
        data: motorAnalysisResult.value.zFeatures.accelerationSpectrum,
      },
    ],
  })
  const chartDom3 = document.getElementById('zRotateChart')
  let zRotateSpectrumChart = echarts.init(chartDom3)
  zRotateSpectrumChart.setOption({
    title: {
      text: 'Z轴转速速度谱 (单位: J/HZ)',
      textStyle: {
        fontWeight: 'normal',
      },
      left: 'center',
    },
    xAxis: {
      name: '频带',
      data: [0.5, 1, 1.5, 2, 3, 4, 5, 6],
    },
    yAxis: {},
    tooltip: {
      trigger: 'item',
      formatter: '{b0}倍频: {c0} J/HZ',
    },
    series: [
      {
        name: 'Z轴',
        type: 'bar',
        data: motorAnalysisResult.value.zFeatures.rotateVelocitySpectrum,
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

const motorAnalysisResult = ref({
  reportTime: '',
  temperature: 0,
  rpm: 0,
  xFeatures: {
    velocity: 0,
    displacement: 0,
    acceleration: 0,
    velocityPeak: 0,
    accelerationPeak: 0,
    velocityKurtosis: 0,
    accelerationKurtosis: 0,
  },
  yFeatures: {
    velocity: 0,
    displacement: 0,
    acceleration: 0,
    velocityPeak: 0,
    accelerationPeak: 0,
    velocityKurtosis: 0,
    accelerationKurtosis: 0,
  },
  zFeatures: {
    velocity: 0,
    displacement: 0,
    acceleration: 0,
    velocityPeak: 0,
    accelerationPeak: 0,
    velocityKurtosis: 0,
    accelerationKurtosis: 0,
  },
})

const handleCloseModal = () => {
  showModal.value = false
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
}
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage show-footer title="即时数据图表">
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
    <div id="his_chart" style="width: 90%; height: 700px; background: white">
      <NRow>
        <NCol id="motor-feature-data" :span="10">
          <div id="motor-simple-intro">
            <div class="data-category-label">基础信息:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">时间:</span>
                  <span style="font-size: 15px; line-height: 20px">{{
                    motorAnalysisResult.reportTime
                  }}</span>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">温度:</span>
                  <span>{{ motorAnalysisResult.temperature }}</span>
                  <span class="row-unit">℃</span>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">转速:</span>
                  <span>{{ motorAnalysisResult.rpm }}</span>
                  <div class="row-unit">rpm</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div id="speed-data-container">
            <div class="data-category-label">速度数据:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span class="feature-value">{{ motorAnalysisResult.xFeatures.velocity }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.velocity }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.velocity }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">位移数据:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.displacement }}</span>
                  <div class="row-unit">μm</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.displacement }}</span>
                  <div class="row-unit">μm</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.displacement }}</span>
                  <div class="row-unit">μm</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">三轴加速度数据:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.acceleration }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.acceleration }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.acceleration }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">三轴速度峰值:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.velocityPeak }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.velocityPeak }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.velocityPeak }}</span>
                  <div class="row-unit">mm/s</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">三轴加速度峰值:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.accelerationPeak }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.accelerationPeak }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.accelerationPeak }}</span>
                  <div class="row-unit">m/s²</div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">三轴速度峭度:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.velocityKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.velocityKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.velocityKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
            </NRow>
          </div>

          <div class="feature-category-data">
            <div class="data-category-label">三轴加速度峭度:</div>
            <NRow>
              <NCol :span="8">
                <div class="row-layout">
                  <span class="row-label">X轴:</span>
                  <span>{{ motorAnalysisResult.xFeatures.accelerationKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Y轴:</span>
                  <span>{{ motorAnalysisResult.yFeatures.accelerationKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
              <NCol :span="7" :offset="1">
                <div class="row-layout">
                  <span class="row-label">Z轴:</span>
                  <span>{{ motorAnalysisResult.zFeatures.accelerationKurtosis }}</span>
                  <div class="row-unit"></div>
                </div>
              </NCol>
            </NRow>
          </div>
        </NCol>
        <NCol :span="13" :offset="1">
          <div class="motor-charts-container">
            <div id="speedEnergyChart" class="motor-chart"></div>
            <div id="speedChart" class="motor-chart"></div>
            <div id="zRotateChart" class="motor-chart"></div>
          </div>
        </NCol>
      </NRow>
    </div>
  </NModal>
</template>

<style scoped>
.feature-category-data {
  background-color: #0f216d;
  color: white;
  padding: 0 5px;
  border-radius: 5px;
}
#speed-data-container {
  background-color: #3556ee;
  color: #5ff65f;
  padding: 0 5px;
  border-radius: 5px;
}
#motor-simple-intro {
  background-color: #6981f5;
  color: #5ff65f;
  padding: 0 5px;
  border-radius: 5px;
}

.row-layout {
  height: 50px;
  display: flex;
  flex-direction: row;
  column-gap: 10px;
  align-items: center;
}

.row-layout .row-label {
  width: 50px;
  font-size: 15px;
}

.row-layout .feature-value {
  width: 30px;
  border-bottom: white 1px solid;
  text-align: center;
}

.row-layout .row-unit {
  width: 65px;
}

.data-catetory-label {
  height: 30px;
}

.motor-charts-container {
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
  /* row-gap: 10px; */
}

.motor-charts-container .motor-chart {
  width: 700px;
  height: 300px;
  padding: 5px;
  /* height: 210px; */
  box-sizing: border-box;
}
</style>
