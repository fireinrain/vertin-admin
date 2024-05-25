<template>
  <div class="app-container main">
    <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
      <el-tab-pane label="每日简报" name="dailyReport">
        <daily-report></daily-report>
      </el-tab-pane>
      <el-tab-pane label="实时监测" name="realtimeMonitor">
        <realtime-view :info="deviceInfo"></realtime-view>
      </el-tab-pane>
      <el-tab-pane label="趋势分析" name="threndAnalyse">
        <el-form inline size="mini">
          <el-form-item label="选择时间范围">
            <el-date-picker
              v-model="historyTimeRange"
              type="datetimerange"
              :picker-options="pickerOptions"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              align="right"
              @change="handleTimePick"
              >
            </el-date-picker>
          </el-form-item>

          <el-form-item label="选择轴向：">
            <el-select v-model="historyDataType">
              <el-option
                v-for="item in historyDataOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="选择数据通道：">
            <el-select v-model="historyDataCategory">
              <el-option
                v-for="item in historyDataCategoryOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                >
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-row>
          <el-col :span="10" :offset="1">
            <div class="trendChart" id="trendChartOne" ref="trendChartOne"></div>
          </el-col>
          <el-col :span="10" :offset="2">
            <div class="trendChart" id="trendChartTwo" ref="trendChartTwo"></div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="10" :offset="1">
            <div class="trendChart" ref="trendChartThree"></div>
          </el-col>
          <el-col :span="10" :offset="2">
            <div class="trendChart" ref="trendChartFour"></div>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="故障诊断" name="faultDiagnose">
        
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script>
import { requestMotorWaveData } from '@/api/device/deviceControl'
import { getMotorWaveDataBySn, getMotorWarnDataBySn } from '@/api/device/deviceData' 
import { getHistoryFeatData } from '@/api/jx/statistics'
import { Message, Loading } from 'element-ui'
import * as echarts from 'echarts'

import * as fft from 'jsfft'

import DailyReport from './tabs/dailyReport.vue'
import RealtimeView from './tabs/realtimeView.vue'

export default {
  name: 'DeviceDetail',
  components: {
    DailyReport,
    RealtimeView
  },
  data() {
    return {
      motorChannels: [
        {
          value: 'xSpeed',
          label: 'X轴速度'
        },
        {
          value: 'ySpeed',
          label: 'Y轴速度'
        },
        {
          value: 'zSpeed',
          label: 'Z轴速度'
        }
      ],
      motorAnalyseChannel: undefined,
      motorAnalysisResult: {
        xFeatures: {
          velocity: undefined,
          displacement: undefined,
          acceleration: undefined,
          velocityPeak: undefined,
          accelerationPeak: undefined,
          velocityKurtosis: undefined,
          accelerationKurtosis: undefined,
          velocitySpectrum: [],
          accelerationSpectrum: []
        },
        yFeatures: {
          velocity: undefined,
          displacement: undefined,
          acceleration: undefined,
          velocityPeak: undefined,
          accelerationPeak: undefined,
          velocityKurtosis: undefined,
          accelerationKurtosis: undefined,
          velocitySpectrum: [],
          accelerationSpectrum: []
        },
        zFeatures: {
          velocity: undefined,
          displacement: undefined,
          acceleration: undefined,
          velocityPeak: undefined,
          accelerationPeak: undefined,
          velocityKurtosis: undefined,
          accelerationKurtosis: undefined,
          velocitySpectrum: [],
          accelerationSpectrum: [],
          rotateVelocitySpectrum: []
        },
        temperature: undefined,
        rpm: undefined,
        reportTime: undefined
      },
      motorEventRecords: undefined,
      activeName: 'dailyReport',
      deviceInfo: undefined,
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }]
      },
      historyTimeRange: '',
      historyDataType: 'x',
      historyDataOptions: [
        {
          value: 'x',
          label: 'X轴'
        },
        {
          value: 'y',
          label: 'Y轴'
        },
        {
          value: 'z',
          label: 'Z轴'
        },
        {
          value: 'temperature',
          label: '温度'
        },
        {
          value: 'rpm',
          label: '转速'
        }
      ],
      historyDataCategory: 'speed',
      historyDataCategoryOptions: [
      {
          value: 'speed',
          label: '速度'
        },
        {
          value: 'displacement',
          label: '位移'
        },
        {
          value: 'acceleration',
          label: '加速度'
        },
        {
          value: 'speedPeak',
          label: '速度峰值'
        },
        {
          value: 'accelerationPeak',
          label: '加速度峰值'
        },
        {
          value: 'speedKurtosis',
          label: '速度峭度'
        },
        {
          value: 'accelerationKurtosis',
          label: '加速度峭度'
        }
      ],
      historyFeatData: []
    }
  },
  created() {
    this.deviceInfo = this.$route.query.deviceInfo
    this.onViewMotorEvent()

  },
  methods: {
    handleClick(tab, event) {
      console.log(tab);
      if (tab.name === 'onlineAnalyse') {
        this.onViewWave()
      }
    },
    handleTimePick(data) {
      let start = this.parseTime(data[0])
      let end = this.parseTime(data[1])
      getHistoryFeatData({sn: this.deviceInfo.sn, startTime: start, endTime: end}).then(res => {
          const historyFeatRawList = res.data
          let historyFeatParsedList = []
          for (const historyRecord of historyFeatRawList) {
            let historyParsedRecord = this.parseFeatData(historyRecord)
            historyFeatParsedList.push(historyParsedRecord)
          }
          console.log(historyFeatParsedList)
          this.drawHistoryTrend(historyFeatParsedList)
        })
    },
    drawHistoryTrend(historyFeatList) {
      let temperatureList = []
      let rpmList = []
      for (const historyFeatItem of historyFeatList) {
        temperatureList.push([historyFeatItem.reportTime, historyFeatItem.temperature])
        rpmList.push([historyFeatItem.reportTime, 50])
      }
      let tempTrendChart = echarts.init(this.$refs.trendChartOne)
      let options = {
        title: {
          text: '温度历史趋势图',
          textStyle: {
            fontWeight: 'normal'
          },
          left: 'center'
        },
        xAxis: {
          show: true,
          name: '时间',
          type: 'time',
          boundaryGap: false
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'item',
          // formatter: '{b0}: {c0} ℃'
        },
        series: [
          {
            name: '温度',
            type: 'line',
            data: temperatureList,
            tooltip: {
              formatter: function(params) {
                let value = params.value
                let time = new Date(value[0])
                var year = time.getFullYear();
                var month = time.getMonth() + 1;
                var day = time.getDate();
                var hours = time.getHours();
                var minutes = time.getMinutes();
                var seconds = time.getSeconds();
                if (seconds < 10) {
                  seconds = '0' + seconds
                }
                return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds + "  " + value[1] + '℃'
              }
            }
          }
        ]
      }
      options && tempTrendChart.setOption(options)
      let rpmTrendChart = echarts.init(this.$refs.trendChartTwo)
      rpmTrendChart.setOption({
      title: {
        text: '转速历史趋势图',
        textStyle: {
        fontWeight: 'normal'
        },
        left: 'center'
      },
      xAxis: {
        show: true,
        name: '时间',
        type: 'time',
        boundaryGap: false
        // data: timestampList,
        // minInterval: 1000 * 60 * 1,
        // maxInterval: 1000 * 60 * 5,
        // min: timestampList[0],
        // max: timestampList.slice(-1)[0]
      },
      yAxis: {
        type: 'value'
      },
      tooltip: {
        trigger: 'item',
        // formatter: '{b0}: {c0} ℃'
      },
      series: [
        {
        name: '转速',
        type: 'line',
        data: rpmList,
        tooltip: {
          formatter: function(params) {
          let value = params.value
          let time = new Date(value[0])
          var year = time.getFullYear();
          var month = time.getMonth() + 1;
          var day = time.getDate();
          var hours = time.getHours();
          var minutes = time.getMinutes();
          var seconds = time.getSeconds();
          if (seconds < 10) {
            seconds = '0' + seconds
          }
          return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds + "  " + value[1] + 'rpm'
          }
        }
        }
      ]
      })
    },
    parseIntStrToValue(str) {
      let valueList = []
      for (let i = 0; i < str.length; i+=4) {
        let valueStr = '0x' + str[i+2] + str[i+3] + str[i] + str[i+1]
        const value = parseInt(valueStr) / 10
        valueList.push(value)
      }
      return valueList
    },
    onViewWave() {
      requestMotorWaveData({sn: this.deviceInfo.sn}).then(res => {
        // 设备在线
        if (res.code === 1) {
          let loadingInstance = Loading.service({target: '#motor-wave-container', fullscreen: false})
          setTimeout(() => {
            getMotorWaveDataBySn(this.deviceInfo.sn).then(res => {
              let valueList = this.parseIntStrToValue(res.content)
              let waveData = {
                x: [],
                y: [],
                z: [],
                updateTime: undefined
              }
              for (let i = 0; i < 128; ++i) {
                waveData.x.push(valueList[i * 3])
                waveData.y.push(valueList[i * 3 + 1])
                waveData.z.push(valueList[i * 3 + 2])
              }
              waveData.updateTime = this.parseTime(res.reportTime)
              this.motorSpeedWave = waveData
              this.drawWaveChart()
              const complexedData = new fft.ComplexArray(128).map((value, i, n) => {
                // value.real = 2 * Math.sin(4 * Math.PI / n * i) + Math.cos(2 * Math.PI / n * i) + 5;
                value.real = waveData.z[i];
              })
              
              const frequencies = complexedData.FFT();
              let frequenciesList = []
              frequencies.forEach((item, i) => {
                if (i >= 0 && i < 64) {
                  frequenciesList.push(Math.sqrt(item.real * item.real + item.imag * item.imag))
                }
              })
              var frequencyChart = echarts.init(this.$refs['motorFrequencyChart'])
              let xAxisList = []
              for (let i = 0; i < 64; ++i) {
                xAxisList.push(i)
              }
              frequencyChart.setOption({
                title: {
                  text: '频谱',
                  textStyle: {
                    fontWeight: 'normal'
                  },
                  subtext: this.motorSpeedWave.updateTime,
                  left: 'center'
                },
                legend: {
                  data: ['X轴'],
                  left: 120,
                  top: 50
                },
                grid: {
                  top: 100
                },
                xAxis: {
                  data: xAxisList
                },
                yAxis: {},
                tooltip: {
                  trigger: 'item'
                },
                series: [
                  {
                    name: 'X轴',
                    type: 'scatter',
                    data: frequenciesList
                  }
                ]
            })
            loadingInstance.close()
          })
          }, 5000);
        } else {
          this.$message({
            message: '设备离线',
            type: 'error'
          })
        }
        
      })
    },
    drawWaveChart() {
      if (this.motorSpeedWaveChart != undefined) {
        this.motorSpeedWaveChart.dispose()
      }
      this.motorSpeedWaveChart = echarts.init(this.$refs['motorWaveChart'])
      let xAxisList = []
      for (let i = 0; i < 128; ++i) {
        xAxisList.push(i)
      }
      this.motorSpeedWaveChart.setOption({
        title: {
          text: '三轴速度波形',
          textStyle: {
            fontWeight: 'normal'
          },
          subtext: this.motorSpeedWave.updateTime,
          left: 'center'
        },
        legend: {
          data: ['X轴', 'Y轴', 'Z轴'],
          left: 120,
          top: 50
        },
        grid: {
          top: 100
        },
        xAxis: {
          data: xAxisList
        },
        yAxis: {},
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            name: 'X轴',
            type: 'line',
            data: this.motorSpeedWave.x
          },
          {
            name: 'Y轴',
            type: 'line',
            data: this.motorSpeedWave.y
          },
          {
            name: 'Z轴',
            type: 'line',
            data: this.motorSpeedWave.z
          }
        ]
      })
    },
    // 查看设备事件
    onViewMotorEvent() {
      const eventMap = {
        T: {
          name: '温度',
          level: undefined,
          value: undefined,
          unit: ['℃']
        },
        X: {
          name: 'X轴',
          type: ['加速度', '速度', '位移', '诊断'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        Y: {
          name: 'Y轴',
          type: ['加速度', '速度', '位移', '诊断'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        Z: {
          name: 'Z轴',
          type: ['加速度', '速度', '位移', '诊断'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        E: {
          name: '解除警报'
        },
        warningType: ['加速度预警', '加速度报警', '速度预警', '速度报警', '位移预警', '位移报警', '故障诊断'],
        diagnosis: ['严重故障', '振动能量超标', '不平衡', '耦合不对中', '机械松动', '润滑不良', '轴松动', '电气故障', '齿轮不对中', '齿轮啮合', '齿轮磨损', '叶片故障']
      }
      getMotorWarnDataBySn(this.deviceInfo.sn).then(res => {
        const frame = res.content
        let itemList = frame.split(',')
        let eventSumary = []
        for (let item of itemList) {
          let report = {
            name: undefined,
            level: undefined,
            value: undefined,
            unit: undefined,
            dignosis: []
          }
          const cate = item[0]
          if (cate === 'T') {
            report.level = item[1] - '0'
            report.name = eventMap[cate].name + eventMap.warningType[item[1] - '0']
            report.unit = eventMap[cate].unit[0]
            report.value = parseInt(item.split('-')[1])
          } else if (cate === 'E') {
            report.name = eventMap[cate].name
          } else {
            report.level = item[1] - '0'
            report.name = eventMap[cate].name + eventMap.warningType[item[1] - '0']
            report.unit = eventMap[cate].unit[item[1] - '0']
            if (item[1] - '0' === 6) {
              let valueStr = item.split('-')[1]
              let newValueStr = '0x' + valueStr[2] + valueStr[3] + valueStr[0] + valueStr[1]
              let data = parseInt(newValueStr)
              console.log(data)
              for (let i = 0; i < 12; ++i) {
                if ((data >>> i) & 0x01) {
                  report.dignosis.push(eventMap.diagnosis[i])
                }
              }
            }
          }
          eventSumary.push(report)
        }
        this.motorEventRecords = eventSumary
        console.log(eventSumary)
      })
      
    },
  }
}
</script>

<style>
.main {
  /* background-color: black; */
  height: calc(100vh - 84px);
}

#motor-feature-data {
  display: flex;
  flex-direction: column;
  row-gap: 5px;
}

#motor-simple-intro {
  display: flex;
  flex-direction: column;
  row-gap: 10px;
  background-color: #0B174A;
  color: white;
  padding: 0 5px;
  border-radius: 5px;
}

#speed-data-container {
  background-color: #0f216d;
  color: white;
  padding: 0 5px;
  border-radius: 5px;
}

.trendChart {
  height: calc(50vh - 100px);
}

.feature-category-data {
  background-color: #0f216d;
  color: white;
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

.motor-charts-container .motor-chart{
  width: 700px;
  height: 300px;
  padding: 5px;
  /* height: 210px; */
  box-sizing: border-box;
}
</style>