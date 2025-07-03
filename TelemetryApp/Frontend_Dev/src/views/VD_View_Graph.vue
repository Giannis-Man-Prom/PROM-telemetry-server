<!-- Εδώ έχουμε το VD View που δεν είναι developped και απλά δείχνει άκυρα δεδομένα -->
<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-3 gap-x-8 gap-y-4 h-screen">
      <SPScatterChart
          :point="point"
          :title="'Acceleration Chart'"
          :minx="{ x: -2, y: 2 }"
          :miny="{ x: -2, y: 2 }"
      />
      <CustomLine
          :datasetLabels="['vcu_Accel_z']"
          :items="[vcu_Accel_z]"
          :title="'Z Accel'"
      />
      <CustomLine
          :datasetLabels="['vcu_hall_fr', 'vcu_hall_fl']"
          :items="[vcu_hall_fr, vcu_hall_fl]"
          :title="'Hall sensors'"
      />
      <CustomLine
          :items="[left_inv_motor_rpm,right_inv_motor_rpm]"
          :datasetLabels="['left_inv_motor_rpm', 'right_inv_motor_rpm']"
          :title="'Motor RPM'"
      />
      <CustomLine
          :datasetLabels="['sensors_linear_rr', 'sensors_linear_rl']"
          :items="[sensors_linear_rr, sensors_linear_rl]"
          :title="'Rear Linears'"
      />
      <CustomLine
          :datasetLabels="['sensors_linear_fl', 'sensors_linear_fr']"
          :items="[sensors_linear_fl, sensors_linear_fr]"
          :title="'Front Linears'"
      />
      <CustomLine
          :datasetLabels="['vcu_brake_front', 'vcu_brake_rear']"
          :items="[vcu_brake_front, vcu_brake_rear]"
          :title="'VCU Brakes'"
      />
      <CustomLine
          :datasetLabels="['vcu_apps1', 'vcu_apps2']"
          :items="[vcu_apps1, vcu_apps2]"
          :title="'APPS'"
      />
      <CustomLine
          :datasetLabels="['vcu_SteeringLinear_angle']"
          :items="[vcu_SteeringLinear_angle]"
          :title="'vcu_SteeringLinear_angle'"
      />
      <CustomLine
          :datasetLabels="['vcu_yaw_rate']"
          :items="[vcu_yaw_rate]"
          :title="'vcu_yaw_rate'"
      />
      <CustomLine
          :datasetLabels="['vcu_requested_torque_right', 'vcu_requested_torque_left']"
          :items="[vcu_requested_torque_right, vcu_requested_torque_left]"
          :title="'vcu_requested_torque'"
      />
      <CustomLine
          :datasetLabels="['vcu_Ku']"
          :items="[vcu_Ku]"
          :title="'vcu_Ku'"
      />
      <CustomLine
          :datasetLabels="['vcu_bb']"
          :items="[vcu_bb]"
          :title="'vcu_bb'"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import SPScatterChart from "../components/SPScatter.vue";
import {io} from "socket.io-client";
import {api_res} from "../types/socketIO.types.ts"; //"@" instead of ".."
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'VD_View_Graph',
  components: {
    CustomLine,
    CustomGauge,
    SPScatterChart
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

      if (this.telemetry_data_obj.vcu_Accel_x !== undefined && this.telemetry_data_obj.vcu_Accel_y !== undefined) {
        this.vcu_Accel_x = [];
        this.point = { x: this.telemetry_data_obj.vcu_Accel_x, y: this.telemetry_data_obj.vcu_Accel_y };
      }
      if (this.telemetry_data_obj.vcu_Accel_z !== undefined) {
        this.vcu_Accel_z = this.telemetry_data_obj.vcu_Accel_z;
      }
      if (this.telemetry_data_obj.vcu_hall_fr !== undefined) {
        this.vcu_hall_fr = this.telemetry_data_obj.vcu_hall_fr;
      }
      if (this.telemetry_data_obj.left_inv_motor_rpm !== undefined) {
        this.left_inv_motor_rpm = this.telemetry_data_obj.left_inv_motor_rpm;
      }
      if (this.telemetry_data_obj.right_inv_motor_rpm !== undefined) {
        this.right_inv_motor_rpm = this.telemetry_data_obj.right_inv_motor_rpm;
      }
      if (this.telemetry_data_obj.vcu_hall_fl !== undefined) {
        this.vcu_hall_fl = this.telemetry_data_obj.vcu_hall_fl;
      }
      if (this.telemetry_data_obj.vcu_VelX !== undefined) {
        this.vcu_VelX = this.telemetry_data_obj.vcu_VelX;
      }
      if (this.telemetry_data_obj.vcu_VelY !== undefined) {
        this.vcu_VelY = this.telemetry_data_obj.vcu_VelY;
      }
      if (this.telemetry_data_obj.sensors_linear_rr !== undefined) {
        this.sensors_linear_rr = this.telemetry_data_obj.sensors_linear_rr;
      }
      if (this.telemetry_data_obj.sensors_linear_rl !== undefined) {
        this.sensors_linear_rl = this.telemetry_data_obj.sensors_linear_rl;
      }
      if (this.telemetry_data_obj.sensors_linear_fl !== undefined) {
        this.sensors_linear_fl = this.telemetry_data_obj.sensors_linear_fl;
      }
      if (this.telemetry_data_obj.sensors_linear_fr !== undefined) {
        this.sensors_linear_fr = this.telemetry_data_obj.sensors_linear_fr;
      }
      if (this.telemetry_data_obj.vcu_brake_front !== undefined) {
        this.vcu_brake_front = this.telemetry_data_obj.vcu_brake_front;
      }
      if (this.telemetry_data_obj.vcu_brake_rear !== undefined) {
        this.vcu_brake_rear = this.telemetry_data_obj.vcu_brake_rear;
      }
      if (this.telemetry_data_obj.vcu_apps1 !== undefined) {
        this.vcu_apps1 = this.telemetry_data_obj.vcu_apps1;
      }
      if (this.telemetry_data_obj.vcu_apps2 !== undefined) {
        this.vcu_apps2 = this.telemetry_data_obj.vcu_apps2;
      }
      if (this.telemetry_data_obj.vcu_yaw_rate !== undefined) {
        this.vcu_yaw_rate = this.telemetry_data_obj.vcu_yaw_rate;
      }
      if (this.telemetry_data_obj.vcu_SteeringLinear_angle !== undefined) {
        this.vcu_SteeringLinear_angle = this.telemetry_data_obj.vcu_SteeringLinear_angle;
      }
      if (this.telemetry_data_obj.vcu_requested_torque_right !== undefined) {
        this.vcu_requested_torque_right = this.telemetry_data_obj.vcu_requested_torque_right;
      }
      if (this.telemetry_data_obj.vcu_requested_torque_left !== undefined) {
        this.vcu_requested_torque_left = this.telemetry_data_obj.vcu_requested_torque_left;
      }
      if (this.telemetry_data_obj.vcu_Ku !== undefined) {
        this.vcu_Ku = this.telemetry_data_obj.vcu_Ku;
      }
      if (this.telemetry_data_obj.vcu_bb !== undefined) {
        this.vcu_bb = this.telemetry_data_obj.vcu_bb;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,

      point: { x: 0, y: 0 },
      vcu_Accel_z: 0,
      vcu_hall_fr: 0,
      vcu_hall_fl: 0,
      vcu_requested_torque_right: 0,
      vcu_requested_torque_left: 0,
      vcu_VelX: 0,
      vcu_VelY: 0,
      sensors_linear_rr: 0,
      sensors_linear_rl: 0,
      sensors_linear_fr: 0,
      sensors_linear_fl: 0,
      left_inv_motor_rpm: 0,
      right_inv_motor_rpm: 0,
      vcu_brake_front: 0,
      vcu_brake_rear: 0,
      vcu_apps1:0 ,
      vcu_apps2: 0,
      vcu_SteeringLinear_angle: 0,
      vcu_yaw_rate: 0,
      vcu_Ku: 0,
      vcu_bb: 0
    }
  }
})

</script>