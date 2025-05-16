<!-- Εδώ έχουμε το VD View που δεν είναι developped και απλά δείχνει άκυρα δεδομένα -->
<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      <CustomLine
          :labels="'vcu_Accel_x'"
          :items="vcu_Accel_x"
          :title="'vcu_Accel_x'"
      />
      <CustomLine
          :labels="'vcu_Accel_y'"
          :items="vcu_Accel_y"
          :title="'vcu_Accel_y'"
      />
      <CustomLine
          :labels="'vcu_Accel_z'"
          :items="vcu_Accel_z"
          :title="'vcu_Accel_z'"
      />
      <CustomLine
          :labels="'vcu_hall_fr'"
          :items="vcu_hall_fr"
          :title="'vcu_hall_fr'"
      />
      <CustomLine
          :labels="'vcu_hall_fl'"
          :items="vcu_hall_fl"
          :title="'vcu_hall_fl'"
      />
      <CustomLine
          :labels="'sensors_linear_rr'"
          :items="sensors_linear_rr"
          :title="'sensors_linear_rr'"
      />
      <CustomLine
          :labels="'sensors_linear_rl'"
          :items="sensors_linear_rl"
          :title="'sensors_linear_rl'"
      />
      <CustomLine
          :labels="'vcu_apps1'"
          :items="vcu_apps1"
          :title="'vcu_apps1'"
      />
      <CustomLine
          :labels="'vcu_apps2'"
          :items="vcu_apps2"
          :title="'vcu_apps2'"
      />
      <CustomLine
          :labels="'vcu_SteeringLinear_mm'"
          :items="vcu_SteeringLinear_mm"
          :title="'vcu_SteeringLinear_mm'"
      />
      <CustomLine
          :labels="'vcu_yaw_rate'"
          :items="vcu_yaw_rate"
          :title="'vcu_yaw_rate'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import {io} from "socket.io-client";
import {api_res} from "../types/socketIO.types.ts"; //"@" instead of ".."
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

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

      if (this.telemetry_data_obj.vcu_Accel_x !== undefined) {
        this.vcu_Accel_x = [this.telemetry_data_obj.vcu_Accel_x];
      }
      if (this.telemetry_data_obj.vcu_Accel_y !== undefined) {
        this.vcu_Accel_y = [this.telemetry_data_obj.vcu_Accel_y];
      }
      if (this.telemetry_data_obj.vcu_Accel_z !== undefined) {
        this.vcu_Accel_z = [this.telemetry_data_obj.vcu_Accel_z];
      }
      if (this.telemetry_data_obj.vcu_hall_fr !== undefined) {
        this.vcu_hall_fr = [this.telemetry_data_obj.vcu_hall_fr];
      }
      if (this.telemetry_data_obj.vcu_hall_fl !== undefined) {
        this.vcu_hall_fl = [this.telemetry_data_obj.vcu_hall_fl];
      }
      if (this.telemetry_data_obj.vcu_VelX !== undefined) {
        this.vcu_VelX = [this.telemetry_data_obj.vcu_VelX];
      }
      if (this.telemetry_data_obj.vcu_VelY !== undefined) {
        this.vcu_VelY = [this.telemetry_data_obj.vcu_VelY];
      }
      if (this.telemetry_data_obj.sensors_linear_rr !== undefined) {
        this.sensors_linear_rr = [this.telemetry_data_obj.sensors_linear_rr];
      }
      if (this.telemetry_data_obj.sensors_linear_rl !== undefined) {
        this.sensors_linear_rl = [this.telemetry_data_obj.sensors_linear_rl];
      }
      if (this.telemetry_data_obj.vcu_apps1 !== undefined) {
        this.vcu_apps1 = [this.telemetry_data_obj.vcu_apps1];
      }
      if (this.telemetry_data_obj.vcu_apps2 !== undefined) {
        this.vcu_apps2 = [this.telemetry_data_obj.vcu_apps2];
      }
      if (this.telemetry_data_obj.vcu_yaw_rate !== undefined) {
        this.vcu_yaw_rate = [this.telemetry_data_obj.vcu_yaw_rate];
      }
      
      if (this.telemetry_data_obj.vcu_SteeringLinear_mm !== undefined) {
        this.vcu_SteeringLinear_mm = [this.telemetry_data_obj.vcu_SteeringLinear_mm];
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      vcu_Accel_x: 0,
      vcu_Accel_y: 0,
      vcu_Accel_z: 0,
      vcu_hall_fr: 0,
      vcu_hall_fl: 0,
      vcu_VelX: 0,
      vcu_VelY: 0,
      sensors_linear_rr: 0,
      sensors_linear_rl: 0,
      vcu_apps1:0 ,
      vcu_apps2: 0,
      vcu_SteeringLinear_mm: 0,
      vcu_yaw_rate: 0
    }
  }
})

</script>