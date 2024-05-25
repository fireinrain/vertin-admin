<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

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
    accelerationKurtosis: 0
  },
  yFeatures: {
    velocity: 0,
    displacement: 0,
    acceleration: 0,
    velocityPeak: 0,
    accelerationPeak: 0,
    velocityKurtosis: 0,
    accelerationKurtosis: 0
  },
  zFeatures: {
    velocity: 0,
    displacement: 0,
    acceleration: 0,
    velocityPeak: 0,
    accelerationPeak: 0,
    velocityKurtosis: 0,
    accelerationKurtosis: 0
  }
});

const motorId = ref('');

const getMotorAnalysisResult = async () => {
  try {
    const response = await axios.get(`api/motor-analysis/${motorId.value}`);
    motorAnalysisResult.value = response.data;
  } catch (error) {
    console.error('Error fetching motor analysis result:', error);
  }
};

onMounted(() => {
  motorId.value = 'YOUR_MOTOR_ID';  // Replace with actual motor ID
  getMotorAnalysisResult();
});
</script>


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
                <span style="font-size: 15px;line-height: 20px;">{{ motorAnalysisResult.reportTime }}</span>
              </div>
            </el-col>
            <el-col :span="7" :offset="1">
              <div class="row-layout">
                <span class="row-label">温度:</span>
                <span>{{ motorAnalysisResult.temperature }}</span>
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
    </el-row>
  </div>
</template>

<style scoped>
.row-layout {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.row-label {
  font-weight: bold;
  margin-right: 5px;
}

.row-unit {
  margin-left: 2px;
}

.data-catetory-label {
  font-weight: bold;
  margin: 10px 0;
}

.feature-category-data {
  margin-top: 20px;
}
</style>
