<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-3 gap-x-8 gap-y-4 h-screen">
      <LineChart
          :labels="'max_cell_temp'"
          :items="max_cell_temp"
          :title="'max_cell_temp'"
      />
      <CustomLineChart
          :labels="'wh_consumed'"
          :items="wh_consumed"
          :title="'wh_consumed'"
      />
      <CustomLineChart
          :labels="'accu_max_cell_temp'"
          :items="accu_max_cell_temp"
          :title="'accu_max_cell_temp'"
      />
      <CustomLineChart
          :labels="'motor_temp'"
          :items="motor_temp"
          :title="'motor_temp'"
      />
      <CustomLineChart
          :labels="'motor_rpm'"
          :items="motor_rpm"
          :title="'motor_rpm'"
      />
      <CustomGauge
          :labels="'left_inv_igbt_temp'"
          :items="left_inv_igbt_temp"
          :title="'left_inv_igbt_temp'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import SideBar from '../components/SideBar.vue';
import BarChartComponent from '@/components/CustomBarChart.vue';

import CustomLineChart from "@/components/CustomLineChart.vue";
import CustomBarChart from "@/components/CustomBarChart.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import {io} from "socket.io-client";
import {linechartItems, VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'CustomCharts',
  components: {
    CustomBarChart,
    SideBar,
    BarChartComponent,
    CustomLineChart,
    CustomGauge
  },
  setup() {
    const labels = reactive<string[]>([]);

    return {
      labels,
    };
  },
  created() {
    socket.on('telemetry_data', (telemetry_data) => {
      //Here we are updating the object every time we get a new message from the socket,
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

      if (this.telemetry_data_obj.max_cell_temp !== undefined) {
        this.max_cell_temp.value = [this.telemetry_data_obj.max_cell_temp];
      }
      if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
        this.accu_over_60v_dclink.value = [this.telemetry_data_obj.accu_over_60v_dclink];
      }
      if (this.telemetry_data_obj.accu_max_cell_temp !== undefined) {
        this.accu_max_cell_temp.value = [this.telemetry_data_obj.accu_max_cell_temp];
      }
      if (this.telemetry_data_obj.motor_temp !== undefined) {
        this.motor_temp.value = [this.telemetry_data_obj.motor_temp];
      }
      if (this.telemetry_data_obj.max_cell_temp !== undefined) {
        this.max_cell_temp = [this.telemetry_data_obj.max_cell_temp];
      }
      if (this.telemetry_data_obj.left_inv_igbt_temp !== undefined) {
        this.left_inv_igbt_temp = this.telemetry_data_obj.left_inv_igbt_temp;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      max_cell_temp: {} as linechartItems[],
      wh_consumed: {} as linechartItems[],
      accu_max_cell_temp: {} as linechartItems[],
      motor_temp: {} as linechartItems[],
      motor_rpm: {} as linechartItems[],
      left_inv_igbt_temp: 0
    }
  }
})

</script>
