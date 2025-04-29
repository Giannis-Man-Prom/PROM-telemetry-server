<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-3 gap-x-8 gap-y-4 h-screen">
      <CustomLineChart
          :labels="accu_total_voltage_vs"
          :items="accu_total_voltage_vs"
          :title="'accu_total_voltage_vs'"
      />
      <CustomLineChart
          :labels="accu_power"
          :items="accu_power"
          :title="'accu_power'"
      />
      <CustomLineChart
          :labels="accu_max_cell_temp"
          :items="accu_max_cell_temp"
          :title="'accu_max_cell_temp'"
      />
      <CustomLineChart
          :labels="motor_temp"
          :items="motor_temp"
          :title="'motor_temp'"
      />
      <CustomLineChart
          :labels="motor_rpm"
          :items="motor_rpm"
          :title="'motor_rpm'"
      />
      <CustomGauge
          :labels="motor_actual_torque"
          :items="motor_actual_torque"
          :title="'motor_actual_torque'"
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
      const dataObj = typeof telemetry_data.data === 'string'
          ? JSON.parse(telemetry_data.data)
          : telemetry_data.data;

      this.telemetry_data_obj = dataObj;

      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.accu_total_voltage_vs.value = [this.telemetry_data_obj.accu_total_voltage_vs];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.accu_power.value = [this.telemetry_data_obj.accu_power];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.accu_max_cell_temp.value = [this.telemetry_data_obj.accu_max_cell_temp];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.motor_temp.value = [this.telemetry_data_obj.motor_temp];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.motor_rpm.value = [this.telemetry_data_obj.motor_rpm];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.motor_actual_torque.value = [this.telemetry_data_obj.motor_actual_torque];
      }

      this.LineChartItems = [
        {label1: 'max_cell_voltage', value1: this.telemetry_data_obj.accu_max_cell_voltage},
        {label1: 'min_cell_voltage', value1: this.telemetry_data_obj.accu_min_cell_voltage},
      ]

    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      accu_total_voltage_vs: {} as linechartItems[],
      accu_power: {} as linechartItems[],
      accu_max_cell_temp: {} as linechartItems[],
      motor_temp: {} as linechartItems[],
      motor_rpm: {} as linechartItems[],
      motor_actual_torque: {} as linechartItems[]
    }
  }
})

</script>
