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
      <LiveThermometer
          :temperature="temperature"
          :title="'whatever'"
      />
      <div class="flex items-start justify-center min-h-1/2 rounded bg-gray-50 dark:bg-gray-800 pt-16">
        <VueSpeedometer
        :value="333"
        :minValue="0"
        :maxValue="1000"
        :segments="5"
        :needleHeightRatio="0.7"
        :needleTransitionDuration="4000"
        needleTransition="easeElastic"
        needleColor="steelblue"
        :segmentColors='["firebrick", "tomato", "gold", "limegreen"]'
        :customSegmentStops="[0, 500, 750, 900, 1000]"
        :maxSegmentLabels="5"
        currentValueText="Speedometer"
        :ringWidth="47"
        textColor="#d8dee9"
      />
      </div>
      <HorizontalBar
        :value="test"
        :title="'whatever'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import SideBar from '../components/SideBar.vue';
import BarChartComponent from '@/components/CustomBarChart.vue';

import CustomLine from "@/components/CustomLine.vue";
import CustomBarChart from "@/components/CustomBarChart.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import LiveThermometer from "../components/Thermometer.vue";
import HorizontalBar from "../components/HorizontalBar.vue";
import VueSpeedometer from 'vue-speedometer';
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
    CustomGauge,
    LiveThermometer,
    VueSpeedometer,
    HorizontalBar,
  },
  setup() {
    const labels = reactive<string[]>([]);

    return {
      labels,
    };
  },
  mounted() {
    // Simulate data for every chart
    setInterval(() => {
      // Simulate values for line charts
      this.air_m_supp = Math.random() * 20 - 10; // Random between -10 and 10
      this.air_p_state = Math.random() * 20 - 10;

      // Simulate values for the gauge chart
      this.accu_over_60v_dclink = Math.random() * 20 - 10;

      // Simulate temperature for the thermometer chart
      this.temperature = Math.random() * 100;

      // Simulate values for scatter chart
      this.valueX = Math.random() * 20 - 10; // Random between -10 and 10
      this.valueY = Math.random() * 20 - 10;

      this.test = Math.random() * 100;
    }, 1000); // Update every 1 second
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
      if (this.telemetry_data_obj.accu_air_p_state !== undefined) {
        this.air_p_state = this.telemetry_data_obj.accu_air_p_state;
      }
      if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
        this.accu_over_60v_dclink = this.telemetry_data_obj.accu_over_60v_dclink;
      }
      if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
        this.temperature = this.telemetry_data_obj.accu_over_60v_dclink;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      air_m_supp: 0,
      air_p_state: 0,
      accu_over_60v_dclink: 0,
      temperature: 0,
      test: 0,
      valueX: 0,
      valueY: 0
    }
  }
})

</script>
