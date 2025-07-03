<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      <CustomLine
        :items="[vcu_hall_fr, vcu_hall_fl]"
        :datasetLabels="['vcu_hall_fr', 'vcu_hall_fl']"
        :title="'Hall Sensors'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[right_inv_motor_rpm, left_inv_motor_rpm]"
        :datasetLabels="['right_inv_motor_rpm', 'left_inv_motor_rpm']"
        :title="'Inv RPM'"
        :chartPercent="70"
      />
      
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent} from 'vue';
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";
import CustomLine from "@/components/CustomLine.vue";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'VcuView',
  components: {
    CustomLine
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

      if (this.telemetry_data_obj.vcu_hall_fr !== undefined) {
        this.vcu_hall_fr = this.telemetry_data_obj.vcu_hall_fr;
      }
      if (this.telemetry_data_obj.vcu_hall_fl !== undefined) {
        this.vcu_hall_fl = this.telemetry_data_obj.vcu_hall_fl;
      }
      if (this.telemetry_data_obj.right_inv_motor_rpm !== undefined) {
        this.right_inv_motor_rpm = this.telemetry_data_obj.right_inv_motor_rpm;
      }
      if (this.telemetry_data_obj.left_inv_motor_rpm !== undefined) {
        this.left_inv_motor_rpm = this.telemetry_data_obj.left_inv_motor_rpm;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      vcu_hall_fr: 0,
      vcu_hall_fl: 0,
      right_inv_motor_rpm: 0,
      left_inv_motor_rpm: 0,
    }
  }
})

</script>
