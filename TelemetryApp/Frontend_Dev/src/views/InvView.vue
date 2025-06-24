<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      <CustomLine
          :labels="'vcu_IsdTrqRight'"
          :items="vcu_IsdTrqRight"
          :title="'vcu_IsdTrqRight'"
      />
      <CustomLine
          :labels="'right_inv_trq_actual'"
          :items="right_inv_trq_actual"
          :title="'right_inv_trq_actual'"
      />
      <CustomLine
          :labels="'vcu_IsdTrqLeft'"
          :items="vcu_IsdTrqLeft"
          :title="'vcu_IsdTrqLeft'"
      />
      <CustomLine
          :labels="'left_inv_trq_actual'"
          :items="left_inv_trq_actual"
          :title="'left_inv_trq_actual'"
      />
      <CustomGauge
          :labels="'right_inv_motor_rpm'"
          :items="right_inv_motor_rpm"
          :title="'right_inv_motor_rpm'"
      />
      <CustomGauge
          :labels="'left_inv_motor_rpm'"
          :items="left_inv_motor_rpm"
          :title="'left_inv_motor_rpm'"
      />
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
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

export default defineComponent({
  name: 'InvView',
  components: {
    CustomLine,
    CustomGauge,
    LiveThermometer,
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
