<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-3 gap-x-1 gap-y-4 h-screen">
      <CustomLine
        :items="[accu_total_voltage_vs]"
        :datasetLabels="['total_voltage_vs']"
        :title="'voltage_vs'"
      />
      <CustomLine
        :items="[accu_current]"
        :datasetLabels="['current']"
        :title="'current'"
      />
      <CustomLine
        :items="[accu_power]"
        :datasetLabels="['power']"
        :title="'power'"
      />
      <CustomLine
        :items="[accu_avg_cell_temp]"
        :datasetLabels="['avg_cell_temp']"
        :title="'avg_cell_temp'"
      />
      <div class="flex items-start justify-center rounded bg-gray-50 dark:bg-gray-800 pt-16">
      <VueSpeedometer
      :value="accu_soc"
      :minValue="0"
      :maxValue="100"
      :segments="5"
      :needleHeightRatio="0.7"
      :needleTransitionDuration="4000"
      needleTransition="easeElastic"
      needleColor="steelblue"
      :segmentColors='["green", "limegreen", "yellow", "firebrick"]'
      :customSegmentStops="[0, 15, 25, 50, 100]"
      :maxSegmentLabels="5"
      currentValueText="SoC: ${value}"
      :ringWidth="47"
      textColor="#d8dee9"
      />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';

import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import VueSpeedometer from 'vue-speedometer';
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'AccuView',
  components: {
    CustomLine,
    CustomGauge,
    VueSpeedometer,
  },
  setup() {
  },
  created() {
    socket.on('telemetry_data', (telemetry_data) => {
      //Here we are updating the object every time we get a new message from the socket,
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.accu_total_voltage_vs = this.telemetry_data_obj.accu_total_voltage_vs;
      }
      if (this.telemetry_data_obj.accu_accu_current !== undefined) {
        this.accu_current = this.telemetry_data_obj.accu_accu_current;
      }
      if (this.telemetry_data_obj.accu_avg_cell_temp !== undefined) {
        this.accu_avg_cell_temp = this.telemetry_data_obj.accu_avg_cell_temp;
      }
      if (this.telemetry_data_obj.accu_power !== undefined) {
        this.accu_power = this.telemetry_data_obj.accu_power;
      }
      if (this.telemetry_data_obj.accu_soc !== undefined) {
        this.accu_soc = this.telemetry_data_obj.accu_soc;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,
      
      accu_total_voltage_vs: 0,
      accu_current:0,
      accu_avg_cell_temp: 0,
      accu_power:0,
      accu_soc:0
    }
  }
})

</script>
