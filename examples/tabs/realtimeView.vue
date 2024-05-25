<template>
  <div>
    <el-row>
      <el-col :span="10" id="motor-feature-data">
        <div id="motor-simple-intro">
          <div class="data-catetory-label">基础信息:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">时间:</span>
                <span
                  style="font-size: 15px;line-height: 20px;">{{ motorAnalysisResult.reportTime }}</span>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">温度:</span>
                <span>{{motorAnalysisResult.temperature}}</span>
                <span class="row-unit">℃</span>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">转速:</span>
                <span>{{ motorAnalysisResult.rpm }}</span>
                <div class="row-unit">rpm</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div id="speed-data-container">
          <div class="data-catetory-label">速度数据:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span class="feature-value">{{ motorAnalysisResult.xFeatures.velocity }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.velocity }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.velocity }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">位移数据:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.displacement }}</span>
                <div class="row-unit">μm</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.displacement }}</span>
                <div class="row-unit">μm</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.displacement }}</span>
                <div class="row-unit">μm</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">三轴加速度数据:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.acceleration }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.acceleration }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.acceleration }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">三轴速度峰值:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.velocityPeak }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.velocityPeak }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.velocityPeak }}</span>
                <div class="row-unit">mm/s</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">三轴加速度峰值:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.accelerationPeak }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.accelerationPeak }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.accelerationPeak }}</span>
                <div class="row-unit">m/s²</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">三轴速度峭度:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.velocityKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.velocityKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.velocityKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="feature-category-data">
          <div class="data-catetory-label">三轴加速度峭度:</div>
          <el-row>
            <el-col :span="8">
              <div class="row-layout">
                <span class="row-label">X轴:</span>
                <span>{{ motorAnalysisResult.xFeatures.accelerationKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Y轴:</span>
                <span>{{ motorAnalysisResult.yFeatures.accelerationKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">Z轴:</span>
                <span>{{ motorAnalysisResult.zFeatures.accelerationKurtosis }}</span>
                <div class="row-unit"></div>
              </div>
            </el-col>
          </el-row>
        </div>

      </el-col>

      <el-col :span="13" :offset="1">
        <div class="motor-charts-container">
          <div class="motor-chart" ref="speedEnergyChart">
          </div>
          <div class="motor-chart" ref="speedChart">
          </div>
          <div class="motor-chart" ref="zRotateChart">
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getMotorFeatDataBySn} from '@/api/device/deviceData' 
export default {
  name: 'RealtimeView',
  props: ['info'],
  data() {
    console.log(this.info)
    return {
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
        reportTime: undefined,
      },
      deviceInfo: this.info
    }
  },
  mounted() {
    this.getMotorRtMonitor()
    console.log(this.deviceInfo)
  },
  methods: {
    parseFeatData(res) {
      let data = res.content
      let valueList = this.parseIntStrToValue(data)
      let analysisInTime = {
        xFeatures: {},
        yFeatures: {},
        zFeatures: {},
        temperature: undefined,
        rpm: undefined,
        reportTime: undefined
      }

      analysisInTime.reportTime = res.reportTime  //转换为ms
      let items = ['xFeatures', 'yFeatures', 'zFeatures']
      for (const [index, key] of items.entries()) {
        analysisInTime[key]['velocity'] = valueList[index]
        analysisInTime[key]['displacement'] = valueList[3 + index]
        analysisInTime[key]['acceleration'] = valueList[6 + index]
        analysisInTime[key]['velocityPeak'] = valueList[9 + index]
        analysisInTime[key]['accelerationPeak'] = valueList[12 + index]
        analysisInTime[key]['velocityKurtosis'] = valueList[15 + index]
        analysisInTime[key]['accelerationKurtosis'] = valueList[18 + index]
        analysisInTime[key]['velocitySpectrum'] = valueList.slice(21 + index * 8, 21 + index * 8 + 8)
        analysisInTime[key]['accelerationSpectrum'] = valueList.slice(45 + index * 8, 45 + index * 8 + 8)
      }
      analysisInTime['zFeatures']['rotateVelocitySpectrum'] = valueList.slice(68, 76)
      analysisInTime.temperature = valueList[77]
      analysisInTime.rpm = valueList[78] * 6
      return analysisInTime
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
    getMotorRtMonitor() {
      getMotorFeatDataBySn(this.deviceInfo.sn).then(res => {
        let data = res.content
        let valueList = this.parseIntStrToValue(data)
        let analysisInTime = {
          xFeatures: {},
          yFeatures: {},
          zFeatures: {},
          temperature: undefined,
          rpm: undefined,
          reportTime: undefined
        }

        analysisInTime.reportTime = this.parseTime(res.reportTime)
        let items = ['xFeatures', 'yFeatures', 'zFeatures']
        for (const [index, key] of items.entries()) {
          analysisInTime[key]['velocity'] = valueList[index]
          analysisInTime[key]['displacement'] = valueList[3 + index]
          analysisInTime[key]['acceleration'] = valueList[6 + index]
          analysisInTime[key]['velocityPeak'] = valueList[9 + index]
          analysisInTime[key]['accelerationPeak'] = valueList[12 + index]
          analysisInTime[key]['velocityKurtosis'] = valueList[15 + index]
          analysisInTime[key]['accelerationKurtosis'] = valueList[18 + index]
          analysisInTime[key]['velocitySpectrum'] = valueList.slice(21 + index * 8, 21 + index * 8 + 8)
          analysisInTime[key]['accelerationSpectrum'] = valueList.slice(45 + index * 8, 45 + index * 8 + 8)
        }
        analysisInTime['zFeatures']['rotateVelocitySpectrum'] = valueList.slice(68, 76)
        analysisInTime.temperature = valueList[77]
        analysisInTime.rpm = valueList[78] * 6
        this.motorAnalysisResult = analysisInTime
        this.initCharts()
      })
    },
    // dialog显示后,对图表进行渲染
    initCharts() {
      var chartSpeedEnergy = echarts.init(this.$refs['speedEnergyChart'])
      chartSpeedEnergy.setOption({
        title: {
          text: '三轴速度谱 (单位: J/HZ)',
          textStyle: {
            fontWeight: 'normal'
          },
          left: 'center'
        },
        legend: {
          data: ['X轴', 'Y轴', 'Z轴'],
          left: 50
        },
        xAxis: {
          name: '频带',
          data: [0.5, 1, 1.5, 2, 3, 4, 5, 6]
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b0}倍频: {c0} J/HZ'
        },
        series: [
          {
            name: 'X轴',
            type: 'bar',
            data: this.motorAnalysisResult.xFeatures.velocitySpectrum
          },
          {
            name: 'Y轴',
            type: 'bar',
            data: this.motorAnalysisResult.yFeatures.velocitySpectrum
          },
          {
            name: 'Z轴',
            type: 'bar',
            data: this.motorAnalysisResult.zFeatures.velocitySpectrum
          }
        ]
      })
      var chartSpeed = echarts.init(this.$refs['speedChart'])
      chartSpeed.setOption({
        title: {
          text: '三轴加速度谱 (单位: J/HZ)',
          textStyle: {
            fontWeight: 'normal'
          },
          left: 'center'
        },
        legend: {
          data: ['X轴', 'Y轴', 'Z轴'],
          left: 50
        },
        xAxis: {
          name: '频带',
          data: [0.5, 1, 1.5, 2, 3, 4, 5, 6]
        },
        yAxis: {},
        tooltip: {
          trigger: 'item',
          formatter: '{b0}倍频: {c0} J/HZ'
        },
        series: [
          {
            name: 'X轴',
            type: 'bar',
            data: this.motorAnalysisResult.xFeatures.accelerationSpectrum
          },
          {
            name: 'Y轴',
            type: 'bar',
            data: this.motorAnalysisResult.yFeatures.accelerationSpectrum
          },
          {
            name: 'Z轴',
            type: 'bar',
            data: this.motorAnalysisResult.zFeatures.accelerationSpectrum
          }
        ]
      })
      var zRotateSpectrumChart = echarts.init(this.$refs['zRotateChart'])
      zRotateSpectrumChart.setOption({
        title: {
          text: 'Z轴转速速度谱 (单位: J/HZ)',
          textStyle: {
            fontWeight: 'normal'
          },
          left: 'center'
        },
        xAxis: {
          name: '频带',
          data: [0.5, 1, 1.5, 2, 3, 4, 5, 6]
        },
        yAxis: {},
        tooltip: {
          trigger: 'item',
          formatter: '{b0}倍频: {c0} J/HZ'
        },
        series: [
          {
            name: 'Z轴',
            type: 'bar',
            data: this.motorAnalysisResult.zFeatures.rotateVelocitySpectrum
          }
        ]
      })
    }
  }
}
</script>

<style>
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