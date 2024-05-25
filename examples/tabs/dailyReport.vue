<template>
  <div class="daily-report">
    <el-row class="row-fixed-layout" :gutter="5">
      <el-col :span="12" style="height: 100%;">
        <div class="panel">
          <div>最大值统计</div>
        </div>
      </el-col>
      <el-col :span="12" style="height: 100%;">
        <div class="panel" ref="healthChart">
          <div>设备健康图</div>
        </div>
      </el-col>
    </el-row>
    <el-row class="row-fixed-layout" :gutter="5">
      <el-col :span="12" style="height: 100%;">
        <div class="panel">
          <div>最小值统计</div>
        </div>
      </el-col>
      <el-col :span="12" style="height: 100%;">
        <div class="panel">
          <div>事件情况</div>
          <div v-for="record in eventRecords" :key="record.time" class="event-records">
            <div class="time">{{ record.time }}</div>
            <div class="category">{{ record.category }}</div>
            <div class="type">{{ record.type }}</div>
            <div class="value">{{ record.value }}</div>
            <div class="unit">{{ record.unit }}</div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>

export default {
  name: 'DailyReport',
  data() {
    return {
      eventRecords: [
        {
          time: '2023-10-23 9:42:32',
          category: 'X轴加速度',
          type: '预警',
          value: 32,
          unit: 'mm/s²'
        },
        {
          time: '2023-10-23 9:42:31',
          category: 'X轴加速度',
          type: '预警',
          value: 32,
          unit: 'mm/s²'
        },
        {
          time: '2023-10-23 9:42:30',
          category: 'X轴加速度',
          type: '预警',
          value: 32,
          unit: 'mm/s²'
        },
        {
          time: '2023-10-23 9:42:34',
          category: 'X轴加速度',
          type: '预警',
          value: 32,
          unit: 'mm/s²'
        }
      ]
    }
  }
}
</script>

<style lang="scss">
.daily-report {
  display: flex;
  flex-direction: column;
  row-gap: 5px;
}

.row-fixed-layout {
  height: calc(50vh - 90px);
}

.event-records {
  display: flex;
  flex-direction: row;
  align-items: center;
  line-height: 22px;
  text-align: center;
  justify-content: space-around;
  .time {
    width: 150px;
  }
}

.panel {
  background-color: rgb(162, 163, 170);
  border: 3px solid rgb(55, 56, 57);
  height: 100%;
  width: 100%;
}
</style>