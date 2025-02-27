<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-2 gap-x-8 gap-y-4 h-screen">
      <CustomLineChart
          :labels="labels"
          :items="LineChartItems"
          :title='max_cell_voltage'
          />
      <CustomLineChart
          :labels="labels"
          :items="LineChartItems"
          :title='max_cell_voltage'
      />
      <CustomLineChart
          :labels="labels"
          :items="LineChartItems"
          :title='max_cell_voltage'
      />
      <CustomLineChart
          :labels="labels"
          :items="LineChartItems"
          :title='max_cell_voltage'
      />

<!--      <CustomLineChart :labels="labels" />-->
<!--      <CustomBarChart :labels="labels" />-->

<!--      <StatusListComponent/>-->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import SideBar from '../components/SideBar.vue';
import LineChartComponent from '@/components/LineChartComponent.vue';
import BarChartComponent from '@/components/CustomBarChart.vue';
import StatusListComponent from '@/components/StatusListComponent.vue';
import CustomLineChart from "@/components/CustomLineChart.vue";
import CustomBarChart from "@/components/CustomBarChart.vue";
import {io} from "socket.io-client";
import {linechartItems, VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'ShowCustomCharts',
  components: {
    CustomBarChart,
    SideBar,
    LineChartComponent,
    BarChartComponent,
    StatusListComponent,
    CustomLineChart
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

      this.LineChartItems = [
        {label1: 'max_cell_voltage', value1: this.telemetry_data_obj.accu_max_cell_voltage},
        {label1: 'min_cell_voltage', value1: this.telemetry_data_obj.accu_min_cell_voltage},
      ]

    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,
      LineChartItems: [] as linechartItems[],
      max_cell_voltage: String
    }
  }
})

</script>
