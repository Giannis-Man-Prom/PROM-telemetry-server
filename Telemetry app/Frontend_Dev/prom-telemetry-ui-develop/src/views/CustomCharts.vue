<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 grid-rows-3 gap-x-8 gap-y-4 h-screen">
      <CustomLine
          :labels="'air_m_supp'"
          :items="air_m_supp"
          :title="'air_m_supp'"
      />
      <CustomLine
          :labels="'air_p_state'"
          :items="air_p_state"
          :title="'air_p_state'"
          :update_ms="300"
      />
      <CustomGauge
          :labels="'accu_over_60v_dclink'"
          :items="accu_over_60v_dclink"
          :title="'accu_over_60v_dclink'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import SideBar from '../components/SideBar.vue';
import BarChartComponent from '@/components/CustomBarChart.vue';

import CustomLine from "@/components/CustomLine.vue";
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
    socket.on('telemetry_data', (telemetry_data) => {
      //Here we are updating the object every time we get a new message from the socket,
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

      if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
        this.air_m_supp = this.telemetry_data_obj.accu_air_m_supp;
      }
      //console.log(this.air_m_supp.value[0]);
      //console.log(this.telemetry_data_obj.accu_air_p_state);
      if (this.telemetry_data_obj.accu_air_p_state !== undefined) {
        this.air_p_state = this.telemetry_data_obj.accu_air_p_state;
      }
      //console.log(this.air_p_state);
      if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
        this.accu_over_60v_dclink = this.telemetry_data_obj.accu_over_60v_dclink;
      }
      //console.log(this.accu_over_60v_dclink);
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      air_m_supp: Number,
      air_p_state: Number,
      accu_over_60v_dclink: 0
    }
  }
})

</script>
