<template>
  <div class="app-container dashboard-container">
    <div id="dashboard-header" class="basic">
      <div class="dashboard-title">嘉轩监控大屏</div>
    </div>
    <div class="dashboard-main">
      <div class="overview-container basic">
        <div class="overview-title">在线统计</div>
        <div class="overview-content">
          <div class="label-with-data">
            <span>产品数量:</span>
            <span>7</span>
          </div>
          <div class="label-with-data">
            <span>设备数量:</span>
            <span>9</span>
          </div>
        </div>
        <div id="device-online-statistics" ref="deviceOnlineChart" style="height: 300px; width: 200px;"></div>
      </div>
      <div class="basic">
        <amap>
          <amap-marker :position="[119.969113,31.817912]"/>
        </amap>
      </div>
      <div id="overview-2" class="basic">
        <div class="overview-title">健康统计</div>
        <div class="overview-content">
          <div class="label-with-data">
            <span>设备数量:</span>
            <span>1000</span>
          </div>
          <div class="label-with-data">
            <span>报警数量:</span>
            <span>53</span>
          </div>
        </div>
        <div id="device-health-statistics" ref="deviceHealthChart" style="height: 300px; width: 200px;"></div>
      </div>
      <div id="warning-info-container" class="basic">
        <div class="overview-title">事件公告</div>
        <div id="device-event-notice">
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
          <div class="event-record">
            <div class="event-timestamp">2023-10-17 10:38:58</div>
            <div class="event-content">
              <div class="event-subject">JX000001</div>
              <div class="event-detail">轴承不对中</div>
            </div>
          </div>
        </div>
      </div>
      <div id="history-data-container" class="basic">
        <div id="history-data-charts" ref="chartContainer" />
      </div>
      <div class="basic"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import Amap from '@amap/amap-vue/lib/amap'
import AmapMarker from '@amap/amap-vue/lib/marker'

export default {
  name: 'MG_Dashboard',
  components: {
    Amap,
    AmapMarker
  },
  data() {
    return {
      map: null
    }
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      var myChart = echarts.init(this.$refs.chartContainer)
      myChart.setOption({
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      })
      var healthChart = echarts.init(this.$refs.deviceHealthChart)
      healthChart.setOption({
        title: {
          text: '设备健康状态统计表',
          left: 'center',
          textStyle: {
            color: 'white',
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          top: '50',
          left: 'center'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 53, name: '报警' },
              { value: 876, name: '健康' },
              { value: 71, name: '预警' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
      var onlineChart = echarts.init(this.$refs.deviceOnlineChart)
      onlineChart.setOption({
        title: {
          text: '设备在线情况统计表',
          left: 'center',
          textStyle: {
            color: 'white',
          }
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          top: '50',
          left: 'center'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 124, name: '离线' },
              { value: 876, name: '在线' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  background-color: #050505;
  height: calc(100vh - 84px);
  box-sizing: border-box;
  padding: 10px;
  display: flex;
  flex-direction: column;
  row-gap: 10px;
}

.basic {
  background-color: #0B174A;
  color: white;
  border: 1px gray solid;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#dashboard-header {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 60px;
}

.dashboard-title {
  line-height: 38px;
  font-size: 28px;
}

.dashboard-main {
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  grid-template-rows: 500px 1fr;
  row-gap: 10px;
  column-gap: 10px;
}

.overview-container {
  display: flex;
  flex-direction: column;
  background-color: #0B174A;
  width: 300px;
  padding: 10px 10px;
}

.overview-title {
  font-size: 24px;
  color: white;
}

.overview-content {
  display: flex;
  width: 100%;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  column-gap: 10px;
  margin: 10px 0px;
}

.label-with-data {
  font-size: 20px;
  color: white;
  width: 45%;
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #448EF7;
}

#map-container {
  width: 100%;
  height: 100%;
}

.event-record {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
}

.event-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#history-data-charts {
  width: 100%;
  height: 100%;
}
</style>

