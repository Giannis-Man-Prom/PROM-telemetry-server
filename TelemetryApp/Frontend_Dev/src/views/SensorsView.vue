<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      <CustomGauge
          :labels="'vcu_VelX'"
          :items="vcu_VelX"
          :title="'vcu_VelX'"
      />
      <CustomGauge
          :labels="'vcu_VelY'"
          :items="vcu_VelY"
          :title="'vcu_VelY'"
      />
      <CustomGauge
          :labels="'vcu_Accel_x'"
          :items="vcu_Accel_x"
          :title="'vcu_Accel_x'"
      />
      <CustomGauge
          :labels="'vcu_Accel_y'"
          :items="vcu_Accel_y"
          :title="'vcu_Accel_y'"
      />
      <CustomGauge
          :labels="'vcu_Accel_z'"
          :items="vcu_Accel_z"
          :title="'vcu_Accel_z'"
      />
      <CustomGauge
          :labels="'vcu_brake_front'"
          :items="vcu_brake_front"
          :title="'vcu_brake_front'"
      />
      <CustomGauge
          :labels="'vcu_brake_rear'"
          :items="vcu_brake_rear"
          :title="'vcu_brake_rear'"
      />      
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import CustomGauge from "@/components/GaugeChart.vue";
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'SensorsView',
  components: {
    CustomGauge
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

      if (this.telemetry_data_obj.vcu_VelX !== undefined) {
        this.vcu_VelX = this.telemetry_data_obj.vcu_VelX;
      }
      if (this.telemetry_data_obj.vcu_VelY !== undefined) {
        this.vcu_VelY = this.telemetry_data_obj.vcu_VelY;
      }
      if (this.telemetry_data_obj.vcu_Accel_x !== undefined) {
        this.vcu_Accel_x = this.telemetry_data_obj.vcu_Accel_x;
      }
      if (this.telemetry_data_obj.vcu_Accel_y !== undefined) {
        this.vcu_Accel_y = this.telemetry_data_obj.vcu_Accel_y;
      }
      if (this.telemetry_data_obj.vcu_Accel_z !== undefined) {
        this.vcu_Accel_z = this.telemetry_data_obj.vcu_Accel_z;
      }
      if (this.telemetry_data_obj.vcu_brake_front !== undefined) {
        this.vcu_brake_front = this.telemetry_data_obj.vcu_brake_front;
      }
      if (this.telemetry_data_obj.vcu_brake_rear !== undefined) {
        this.vcu_brake_rear = this.telemetry_data_obj.vcu_brake_rear;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      vcu_VelX: 0,
      vcu_VelY: 0,
      vcu_VelZ: 0,
      vcu_Accel_x: 0,
      vcu_Accel_y: 0,
      vcu_Accel_z: 0,
      vcu_brake_front: 0,
      vcu_brake_rear: 0,
    }
  }
})

</script>
