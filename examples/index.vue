<template>
  <div class="app-container">
    <el-dialog title="产品信息录入表单" :visible.sync="showDeviceInfoForm" width="600px">
      <el-form :model="formDeviceInfo" label-width="120px">
        <el-form-item label="产品序列号" class="device-info-form-item">
          <el-input v-model="formDeviceInfo.sn" placeholder="请输入产品序列号" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="产品型号" class="device-info-form-item">
          <el-cascader
            v-model="formDeviceInfo.pid"
            :options="devTypeOpts"
            style="width: 300px;"
            placeholder="请选择"
            @change="onDeviceTypeChange"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onAddDevice(formDeviceInfo)">确认</el-button>
          <el-button @click="showDeviceInfoForm=false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-form :inline="true" :model="deviceSearchOpts"  size="small" v-show="showSearch">
      <el-form-item label="用户名">
        <el-input v-model="deviceSearchOpts.account" clearable type="primary" placeholder="请输入" />
      </el-form-item>
      <el-form-item label="设备ID">
        <el-input v-model="deviceSearchOpts.sn" clearable type="primary" placeholder="请输入" />
      </el-form-item>
      <!-- <el-form-item label="设备状态">
        <el-input v-model="deviceSearchOpts.connectionstatus" type="primary" placeholder="请输入" />
      </el-form-item> -->
      <el-form-item>
        <el-button type="primary" @click="onSearchDevice(deviceSearchOpts)">搜索</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" size="small" plain icon="el-icon-plus" @click="onRecordDevice">产品录入</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="primary" size="small" plain icon="el-icon-refresh"  @click="refreshDeviceList">刷新列表</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="refreshDeviceList"></right-toolbar>
    </el-row>

    <div id="device-list-container">
      <el-table
        :data="deviceInfoList"
        style="margin: auto;"
      >
        <el-table-column
          label="设备ID"
          align="center"
          width="100"
        >
          <template slot-scope="scope">
            <el-link type="primary" @click="onViewDetail(scope.row)">{{scope.row.sn}}</el-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="pid"
          label="产品型号"
          align="center"
        />
        <el-table-column
          prop="company"
          label="所属公司"
          align="center"
        />
        <el-table-column
          label="授权状态"
          align="center"
          width="200"
        >
          <template slot-scope="scope">
            <div class="status-tags">
              <el-switch
                v-model="scope.row.authorized"
                :active-value=1
                :inactive-value=0
                @change="onChangeAuthorized(scope.row)">
              </el-switch>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="runningstatus"
          label="状态"
          align="center"
          width="200"
        >
          <template slot-scope="scope">
            <div class="status-tags">
              <el-tag type="primary">{{ scope.row.online === 'yes' ? '在线' : '离线' }}</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="updateTime"
          label="最后更新时间"
        />
      </el-table>
      <!-- <pagination
        v-show="deviceListNums>0"
        :total="deviceListNums"
        :page.sync="pageNums"
        :pageSizes="pageSizes"
        :limit.sync="pageSize"
        @pagination="getPageDeviceList"
      /> -->
    </div>

    <el-dialog
      title="报警事件"
      :visible.sync="showMotorEvent"
      width="500px"
      >
      <div class="event-report"><span>事件上报时间:</span><span class="report-time">2023-10-11 17:41:32</span></div>
      <div v-for="event in motorEventRecords" :key="event.name" class="event-records" :class="event.level === 0 ? 'event-warning' : 'event-error'">
        <div class="event-notice">
          <i v-if="event.level === 0" class="el-icon-warning"></i>
          <i v-else class="el-icon-error"></i>
          <span class="event-name">{{event.name}}</span>
        </div>
        <div class="event-detail">
          <span class="event-notice-value">{{event.value}}</span>
          <span class="event-notice-unit">{{event.unit}}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { createDevice, getDeviceBaseInfo, countDeviceListByConditions, changeDeviceAuthStatus } from '@/api/device/deviceBase'
import { getDeviceStatusBySns } from '@/api/device/deviceStatus'
import { Message} from 'element-ui'

export default {
  name: 'MGINFO',
  data() {
    return {
      authorMode: [
        {
          value: 0,
          label: '未授权'
        },
        {
          value: 1,
          label: '已授权'
        }
      ],
      useMode: [
        {
          value: 0,
          label: '停用'
        },
        {
          value: 1,
          label: '启用'
        }
      ],
      formDeviceInfo: {
        sn: '',
        pid: ''
      },
      showSearch: true,
      showParamConfig: false,
      isWaitForResponse: false,
      showDeviceDetail: false,
      showMotorWave: false,
      showMotorEvent: false,
      formLabelWidth: '100px',
      deviceInfoList: [],
      selectedDeviceSn: '',
      deviceSearchOpts: {
        pidList: [],
        sn: '',
        username: '',
        company: ''
      },
      deviceTypeInputProps: {
        multiple: true
      },
      curModifyDeviceSn: null,
      showDeviceInfoForm: false,
      devTypeOpts: [
        {
          value: 'sort',
          label: '分选机',
          children: [{
            value: 'FVS-JET103',
            label: '高速视选机'
          }, {
            value: 'FVS-TRUSS-JC',
            label: '桁架视选机'
          }]
        }, {
          value: 'MG',
          label: '电机卫士'
        }
      ],
      motorSpeedWave: {},
      motorSpeedWaveChart: undefined,
      motorEventRecords: undefined,
      deviceListNums: 3,
      pageNums: 1,
      pageSize: 2,
      pageSizes: [5, 10, 20]
    }
  },
  mounted: function() {
    this.refreshDeviceList()
  },
  methods: {
    parseIntStrToValue(str) {
      let valueList = []
      for (let i = 0; i < str.length; i+=4) {
        let valueStr = '0x' + str[i+2] + str[i+3] + str[i] + str[i+1]
        const value = parseInt(valueStr) / 10
        valueList.push(value)
      }
      return valueList
    },
    // 查看设备数据事件
    onViewDetail(deviceInfo) {
      this.$router.push({path: '/project/details', query: {deviceInfo: deviceInfo}})
    },
    // 授权按钮点击事件
    onChangeAuthorized(row) {
      this.$confirm('确认修改授权?', '提示').then(() => {
        changeDeviceAuthStatus({
          sn: row.sn,
          authorized: row.authorized
        }).then(res => {
          if (res.code === 200) {
            Message({
              message: '操作成功',
              type: 'success',
              duration: 1.5 * 1000
            })
          }
          this.refreshDeviceList()
        })
      }).catch(() => {
        row.authorized = 1 - row.authorized
      })
    },
    // 确认添加设备事件
    onAddDevice: function(deviceInfo) {
      console.log(deviceInfo)
      createDevice({
        sn: deviceInfo.sn,
        pid: deviceInfo.pid
      }).then((res) => {
        if (res.code === 0) {
          Message({
            message: res.resMsg,
            type: 'error',
            duration: 5 * 1000
          })
        } else {
          Message({
            message: '录入设备成功',
            type: 'success',
            duration: 5 * 1000
          })
          this.showDeviceInfoForm = false
        }
      })
    },
    // 选择产品时事件触发
    onDeviceTypeChange: function(value) {
      this.formDeviceInfo.pid = value[1]
    },
    // 录入设备按钮事件
    onRecordDevice: function() {
      this.showDeviceInfoForm = true
    },
    // 刷新设备列表
    refreshDeviceList: function() {
      countDeviceListByConditions(this.deviceSearchOpts).then(res => {
        this.deviceListNums = res.obj
      })
      let deviceSns = ''
      getDeviceBaseInfo({username: 'admin', company: '嘉轩'}).then(baseInfoList => {
        if (baseInfoList.length === 0) {
          return
        }
        baseInfoList.forEach(item => {
          deviceSns += item.sn
          deviceSns += ','
        })
        deviceSns = deviceSns.substring(0, deviceSns.length - 1)
        getDeviceStatusBySns({sns: deviceSns}).then(statusList => {
          console.log(statusList)
          for (const [index, item] of statusList.entries()) {
            for (const key in item) {
              if (!baseInfoList[index].hasOwnProperty(key)) {
                baseInfoList[index][key] = item[key]
              }
            }
          }
          this.deviceInfoList = baseInfoList
        })
      })
    },
    // 搜索设备
    onSearchDevice: function() {
      this.refreshDeviceList()
    },
    // 查看设备事件
    onViewMotorEvent(deviceInfo) {
      const eventMap = {
        T: {
          name: '温度',
          level: undefined,
          value: undefined,
          unit: ['℃']
        },
        X: {
          name: 'X轴',
          type: ['加速度', '速度', '位移'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        Y: {
          name: 'Y轴',
          type: ['加速度', '速度', '位移'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        Z: {
          name: 'Z轴',
          type: ['加速度', '速度', '位移'],
          level: undefined,
          value: undefined,
          unit: ['m/s²', 'mm/s', 'μm']
        },
        warningType: ['预警', '报警']
      }
      const frame = 'T0-32,X01-32,Z11-21'
      this.showMotorEvent = true
      let itemList = frame.split(',')
      let eventSumary = []
      for (let item of itemList) {
        let report = {
          name: undefined,
          level: undefined,
          value: undefined,
          unit: undefined
        }
        const cate = item[0]
        let data = parseInt(item.split('-')[1])
        if (cate === 'T') {
          report.level = item[1] - '0'
          report.name = eventMap[cate].name + eventMap.warningType[report.level]
          report.unit = eventMap[cate].unit[0]
        } else {
          report.level = item[2] - '0'
          report.name = eventMap[cate].name + eventMap[cate].type[item[1] - '0'] + eventMap.warningType[report.level]
          report.unit = eventMap[cate].unit[item[1] - '0']
        }
        report.value = data
        eventSumary.push(report)
      }
      this.motorEventRecords = eventSumary
      console.log(eventSumary)
    },
    // 更新设备参数
    onUpdateData: function(row) {
      console.log(row)
      // getDeviceRealtimeData({ account: 'hjz' }).then(res => {
      //   console.log(res)
      //   const content = res.content
      //   const data = JSON.parse(content)
      //   console.log(data)
      // })
    }
  }
}
</script>

<style scoped>

.device-info-form-item {
  margin: 20px 0;
}

/* .device-manage-tools {
  margin-left: 20px;
  margin-bottom: 20px;
} */

#device-list-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  row-gap: 20px;
}

.device-list-pagination {
  align-self: flex-end;
  margin-right: 20px;
}

.param-config-form .el-input {
  width: 160px;
}

.config-form-category {
  font-size: 20px;
  color: black;
  padding-left: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
}

.status-tags {
  display: flex;
  flex-direction: row;
  column-gap: 5px;
  justify-content: center;
}

.motor-simple-intro {
  display: flex;
  flex-direction: column;
  row-gap: 10px;
}

.row-layout {
  display: flex;
  flex-direction: row;
  column-gap: 10px;
  align-items: center;
}

.row-layout .row-label {
  width: 70px;
  font-size: 15px;
}

.row-layout .row-unit {
  width: 65px;
}

.motor-charts-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  /* row-gap: 10px; */
}

.motor-charts-container .motor-chart{
  width: 100%;
  height: 210px;
}

.data-catetory-label {
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  color: black;
}

.event-report {
  font-size: 18px;
  margin-bottom: 10px;
}

.event-report .report-time {
  margin-left: 10px;
}

.event-records {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: 18px;
  padding: 5px 0px;
}

.event-warning {
  color: orange;
  /* border-bottom: rgb(228, 185, 104) 1px solid; */
}

.event-error {
  color: rgb(241, 58, 58);
  /* border-bottom: rgb(236, 93, 90) 1px solid; */
}

.event-notice .event-name{
  margin-left: 5px;
}

.event-detail .event-notice-unit {
  margin-left: 5px;
  width:30px;
}

</style>
