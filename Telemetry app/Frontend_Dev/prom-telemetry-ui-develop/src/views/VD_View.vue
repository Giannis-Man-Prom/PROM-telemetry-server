<!-- Εδώ έχουμε το VD View που δεν είναι developped και απλά δείχνει άκυρα δεδομένα -->
<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-3 gap-x-8 gap-y-4 h-screen">
      <CustomLine
          :labels="'ax'"
          :items="ax"
          :title="'ax'"
      />
      <CustomLine
          :labels="'ay'"
          :items="ay"
          :title="'ay'"
      />
      <CustomGauge
          :labels="'yaw_rate'"
          :items="yaw_rate"
          :title="'yaw_rate'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import SideBar from '../components/SideBar.vue';
import BarChartComponent from '@/components/CustomBarChart.vue';

import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import {io} from "socket.io-client";
import {api_res, event_connection_res} from "../types/socketIO.types.ts"; //"@" instead of ".."
import {linechartItems, VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'CustomCharts',
  components: {
    CustomLine,
    CustomGauge
  },
  setup() {
    const labels = reactive<string[]>([]);

    return {
      labels,
    };
  },
  created() {
    socket.on('telemetry_data', (telemetry_data : api_res) => {
      //Here we are updating the object every time we get a new message from the socket,
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }
      if (this.telemetry_data_obj.max_cell_temp !== undefined) {
        this.max_cell_temp.value = [this.telemetry_data_obj.max_cell_temp];
      }
      if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
        this.ax = [this.telemetry_data_obj.accu_air_m_supp];
      }
      if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
        this.ax = [this.telemetry_data_obj.accu_air_m_supp];
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      ax: 0,
      ay: 0,
      yaw_rate: 0
    }
  }
})

</script>