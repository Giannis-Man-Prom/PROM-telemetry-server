<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-4 gap-x-8 gap-y-4 h-screen">
      <CustomLine
        :items="[vcu_IsdTrqRight]"
        :datasetLabels="['vcu_IsdTrqRight']"
        :title="'vcu_IsdTrqRight'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[right_inv_trq_actual]"
        :datasetLabels="['right_inv_trq_actual']"
        :title="'right_inv_trq_actual'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[vcu_IsdTrqLeft]"
        :datasetLabels="['vcu_IsdTrqLeft']"
        :title="'vcu_IsdTrqLeft'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[left_inv_trq_actual]"
        :datasetLabels="['left_inv_trq_actual']"
        :title="'left_inv_trq_actual'"
        :chartPercent="70"
      />
      <div class="flex items-start justify-center rounded bg-gray-50 dark:bg-gray-800 pt-16">
        <VueSpeedometer
        :value="right_inv_motor_rpm"
        :minValue="0"
        :maxValue="30000"
        :segments="5"
        :needleHeightRatio="0.7"
        :needleTransitionDuration="4000"
        needleTransition="easeElastic"
        needleColor="steelblue"
        :segmentColors='["limegreen", "gold", "tomato"]'
        :customSegmentStops="[0, 20000, 25000, 30000]"
        :maxSegmentLabels="5"
        currentValueText="right_inv_motor_rpm ${value}"
        :ringWidth="47"
        textColor="#d8dee9"
      />
      </div>
      <div class="flex items-start justify-center rounded bg-gray-50 dark:bg-gray-800 pt-16">
        <VueSpeedometer
        :value="left_inv_motor_rpm"
        :minValue="0"
        :maxValue="30000"
        :segments="4"
        :needleHeightRatio="0.7"
        :needleTransitionDuration="4000"
        needleTransition="easeElastic"
        needleColor="steelblue"
        :segmentColors='["limegreen", "gold", "tomato"]'
        :customSegmentStops="[0, 20000, 25000, 30000]"
        :maxSegmentLabels="5"
        currentValueText="left_inv_motor_rpm: ${value}"
        :ringWidth="47"
        textColor="#d8dee9"
      />
      </div>
      <LiveThermometer
        :temperature="right_inv_motor_temp"
        :title="'right_inv_motor_temp'"
      />
      <LiveThermometer
        :temperature="left_inv_motor_temp"
        :title="'left_inv_motor_temp'"
      />
      <LiveThermometer
        :temperature="right_inv_igbt_temp"
        :title="'right_inv_igbt_temp'"
      />
      <LiveThermometer
        :temperature="left_inv_igbt_temp"
        :title="'left_inv_igbt_temp'"
      />
      
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import LiveThermometer from "../components/Thermometer.vue";
import VueSpeedometer from 'vue-speedometer';
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

export default defineComponent({
  name: 'InvView',
  components: {
    CustomLine,
    CustomGauge,
    LiveThermometer,
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

      if (this.telemetry_data_obj.vcu_IsdTrqRight !== undefined) {
        this.vcu_IsdTrqRight = this.telemetry_data_obj.vcu_IsdTrqRight;
      }
      if (this.telemetry_data_obj.right_inv_trq_actual !== undefined) {
        this.right_inv_trq_actual = this.telemetry_data_obj.right_inv_trq_actual;
      }
      if (this.telemetry_data_obj.vcu_IsdTrqLeft !== undefined) {
        this.vcu_IsdTrqLeft = this.telemetry_data_obj.vcu_IsdTrqLeft;
      }
      if (this.telemetry_data_obj.left_inv_trq_actual !== undefined) {
        this.left_inv_trq_actual = this.telemetry_data_obj.left_inv_trq_actual;
      }
      if (this.telemetry_data_obj.right_inv_motor_rpm !== undefined) {
        this.right_inv_motor_rpm = this.telemetry_data_obj.right_inv_motor_rpm;
      }
      if (this.telemetry_data_obj.left_inv_motor_rpm !== undefined) {
        this.left_inv_motor_rpm = this.telemetry_data_obj.left_inv_motor_rpm;
      }
      if (this.telemetry_data_obj.right_inv_motor_temp !== undefined) {
        this.right_inv_motor_temp = this.telemetry_data_obj.right_inv_motor_temp;
      }
      if (this.telemetry_data_obj.left_inv_motor_temp !== undefined) {
        this.left_inv_motor_temp = this.telemetry_data_obj.left_inv_motor_temp;
      }
      if (this.telemetry_data_obj.right_inv_igbt_temp !== undefined) {
        this.right_inv_igbt_temp = this.telemetry_data_obj.right_inv_igbt_temp;
      }
      if (this.telemetry_data_obj.left_inv_igbt_temp !== undefined) {
        this.left_inv_igbt_temp = this.telemetry_data_obj.left_inv_igbt_temp;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      vcu_IsdTrqRight: 0,
      right_inv_trq_actual: 0,

      vcu_IsdTrqLeft: 0,
      left_inv_trq_actual: 0,

      right_inv_motor_rpm: 0,
      left_inv_motor_rpm: 0,

      right_inv_motor_temp: 0,
      left_inv_motor_temp: 0,

      right_inv_igbt_temp: 0,
      left_inv_igbt_temp: 0,

    }
  }
})

</script>
