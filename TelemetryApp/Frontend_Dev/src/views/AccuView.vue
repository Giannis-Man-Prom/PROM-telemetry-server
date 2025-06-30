<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      <CustomLine
        :items="[accu_total_voltage_vs]"
        :datasetLabels="['accu_total_voltage_vs']"
         :title="'accu_total_voltage_vs'"
      />
      <CustomGauge
        :items="accu_current"
        :datasetLabels="'accu_current'"
        :title="'accu_current'"
      />
      <CustomLine
        :items="[accu_wh_consumed]"
        :datasetLabels="['accu_wh_consumed']"
        :title="'accu_wh_consumed'"
      />
      <CustomGauge
        :items="accu_power"
        :datasetLabels="'accu_power'"
        :title="'accu_power'"
      />
      
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
      if (this.telemetry_data_obj.accu_wh_consumed !== undefined) {
        this.accu_wh_consumed = this.telemetry_data_obj.accu_wh_consumed;
      }
      if (this.telemetry_data_obj.accu_power !== undefined) {
        this.accu_power = this.telemetry_data_obj.accu_power;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,
      
      accu_total_voltage_vs: 0,
      accu_current:0,
      accu_wh_consumed: 0,
      accu_power:0
    }
  }
})

</script>
