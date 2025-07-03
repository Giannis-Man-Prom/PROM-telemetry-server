<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-4 gap-x-1 gap-y-4 h-screen">
      <div class="flex justify-center items-center col-span-2">
      <ColoredDots
        title="Left"
        :bool_values="leftInvLimiters"
        gap="5px"
        :value1="left_inv_Imax"
        :value2="left_inv_actual_inverter_status"
        />
    </div>
    <div class="flex justify-center items-center col-span-2">
      <ColoredDots
      title="Right"
      :bool_values="rightInvLimiters"
      gap="5px"
      :value1="right_inv_Imax"
      :value2="right_inv_actual_inverter_status"/>
    </div>
      <CustomLine
        :items="[vcu_IsdTrqLeft]"
        :datasetLabels="['IsdTrqLeft']"
        :title="'IsdTrqLeft'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[left_inv_trq_actual]"
        :datasetLabels="['left_inv_trq_actual']"
        :title="'left_inv_trq_actual'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[vcu_IsdTrqRight]"
        :datasetLabels="['IsdTrqRight']"
        :title="'IsdTrqRight'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[right_inv_trq_actual]"
        :datasetLabels="['right_inv_trq_actual']"
        :title="'right_inv_trq_actual'"
        :chartPercent="70"
      />
      <div class="flex items-start justify-center rounded bg-gray-50 dark:bg-gray-800 pt-16">
        <VueSpeedometer
        :value="left_inv_motor_rpm"
        :minValue="0"
        :maxValue="20000"
        :segments="4"
        :needleHeightRatio="0.7"
        :needleTransitionDuration="4000"
        needleTransition="easeElastic"
        needleColor="steelblue"
        :segmentColors='["limegreen", "gold", "tomato"]'
        :customSegmentStops="[0, 11000, 18000, 20000]"
        :maxSegmentLabels="5"
        currentValueText="left_inv_motor_rpm: ${value}"
        :ringWidth="47"
        textColor="#d8dee9"
      />
      </div>
      <div class="flex items-start justify-center rounded bg-gray-50 dark:bg-gray-800 pt-16">
        <VueSpeedometer
        :value="right_inv_motor_rpm"
        :minValue="0"
        :maxValue="20000"
        :segments="5"
        :needleHeightRatio="0.7"
        :needleTransitionDuration="4000"
        needleTransition="easeElastic"
        needleColor="steelblue"
        :segmentColors='["limegreen", "gold", "tomato"]'
        :customSegmentStops="[0, 11000, 18000, 20000]"
        :maxSegmentLabels="5"
        currentValueText="right_inv_motor_rpm ${value}"
        :ringWidth="47"
        textColor="#d8dee9"
      />
      </div>
      <CustomLine
        :items="[left_inv_motor_temp, left_inv_igbt_temp]"
        :datasetLabels="['left_inv_motor_temp', 'left_inv_igbt_temp']"
        :title="'Left Inverter Temps'"
        :chartPercent="70"
      />
      <CustomLine
        :items="[right_inv_motor_temp, right_inv_igbt_temp]"
        :datasetLabels="['right_inv_motor_temp', 'right_inv_igbt_temp']"
        :title="'Right Inverter Temps'"
        :chartPercent="70"
      />      
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import CustomLine from "@/components/CustomLine.vue";
import CustomGauge from "@/components/GaugeChart.vue";
import LiveThermometer from "../components/Thermometer.vue";
import ColoredDots from "../components/Dots.vue";
import VueSpeedometer from 'vue-speedometer';
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

export default defineComponent({
  name: 'InvView',
  components: {
    ColoredDots,
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

      if (this.telemetry_data_obj.left_inv_Imax !== undefined) {
        this.left_inv_Imax = this.telemetry_data_obj.left_inv_Imax;
      }
      if (this.telemetry_data_obj.left_inv_actual_inverter_status !== undefined) {
        this.left_inv_actual_inverter_status = this.telemetry_data_obj.left_inv_actual_inverter_status;
      }
      if (this.telemetry_data_obj.right_inv_Imax !== undefined) {
        this.right_inv_Imax = this.telemetry_data_obj.right_inv_Imax;
      }
      if (this.telemetry_data_obj.right_inv_actual_inverter_status !== undefined) {
        this.right_inv_actual_inverter_status = this.telemetry_data_obj.right_inv_actual_inverter_status;
      }
      if (this.telemetry_data_obj.right_inv_lim_speed_limiter !== undefined) {
        this.right_inv_lim_speed_limiter = this.telemetry_data_obj.right_inv_lim_speed_limiter;
      }
      if (this.telemetry_data_obj.right_inv_lim_power_limiter !== undefined) {
        this.right_inv_lim_power_limiter = this.telemetry_data_obj.right_inv_lim_power_limiter;
      }
      if (this.telemetry_data_obj.right_inv_lim_stall_limiter !== undefined) {
        this.right_inv_lim_stall_limiter = this.telemetry_data_obj.right_inv_lim_stall_limiter;
      }
      if (this.telemetry_data_obj.right_inv_lim_l2t_limiter !== undefined) {
        this.right_inv_lim_l2t_limiter = this.telemetry_data_obj.right_inv_lim_l2t_limiter;
      }
      if (this.telemetry_data_obj.right_inv_lim_motor_temp !== undefined) {
        this.right_inv_lim_motor_temp = this.telemetry_data_obj.right_inv_lim_motor_temp;
      }
      if (this.telemetry_data_obj.right_inv_lim_igbt_temp !== undefined) {
        this.right_inv_lim_igbt_temp = this.telemetry_data_obj.right_inv_lim_igbt_temp;
      }
      if (this.telemetry_data_obj.left_inv_lim_speed_limiter !== undefined) {
        this.left_inv_lim_speed_limiter = this.telemetry_data_obj.left_inv_lim_speed_limiter;
      }
      if (this.telemetry_data_obj.left_inv_lim_power_limiter !== undefined) {
        this.left_inv_lim_power_limiter = this.telemetry_data_obj.left_inv_lim_power_limiter;
      }
      if (this.telemetry_data_obj.left_inv_lim_stall_limiter !== undefined) {
        this.left_inv_lim_stall_limiter = this.telemetry_data_obj.left_inv_lim_stall_limiter;
      }
      if (this.telemetry_data_obj.left_inv_lim_l2t_limiter !== undefined) {
        this.left_inv_lim_l2t_limiter = this.telemetry_data_obj.left_inv_lim_l2t_limiter;
      }
      if (this.telemetry_data_obj.left_inv_lim_motor_temp !== undefined) {
        this.left_inv_lim_motor_temp = this.telemetry_data_obj.left_inv_lim_motor_temp;
      }
      if (this.telemetry_data_obj.left_inv_lim_igbt_temp !== undefined) {
        this.left_inv_lim_igbt_temp = this.telemetry_data_obj.left_inv_lim_igbt_temp;
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

      left_inv_Imax: 0,
      left_inv_actual_inverter_status: -1,
      right_inv_Imax: 0,
      right_inv_actual_inverter_status: -1,
      
      right_inv_lim_speed_limiter: 0,
      right_inv_lim_power_limiter: 0,
      right_inv_lim_stall_limiter: 0,
      right_inv_lim_l2t_limiter: 0,
      right_inv_lim_motor_temp: 0,
      right_inv_lim_igbt_temp: 0,

      left_inv_lim_speed_limiter: 0,
      left_inv_lim_power_limiter: 0,
      left_inv_lim_stall_limiter: 0,
      left_inv_lim_l2t_limiter: 0,
      left_inv_lim_motor_temp: 0,
      left_inv_lim_igbt_temp: 0,


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
  },
  computed: {
  leftInvLimiters() {
    return [
      { active: this.left_inv_lim_speed_limiter, label: 'lim_speed_limiter' },
      { active: this.left_inv_lim_power_limiter, label: 'lim_power_limiter' },
      { active: this.left_inv_lim_stall_limiter, label: 'lim_stall_limiter' },
      { active: this.left_inv_lim_l2t_limiter, label: 'lim_l2t_limiter' },
      { active: this.left_inv_lim_motor_temp, label: 'lim_motor_limiter' },
      { active: this.left_inv_lim_igbt_temp, label: 'lim_igbt_limiter' },
    ];
  },
  rightInvLimiters() {
    return [
      { active: this.right_inv_lim_speed_limiter, label: 'lim_speed_limiter' },
      { active: this.right_inv_lim_power_limiter, label: 'lim_power_limiter' },
      { active: this.right_inv_lim_stall_limiter, label: 'lim_stall_limiter' },
      { active: this.right_inv_lim_l2t_limiter, label: 'lim_l2t_limiter' },
      { active: this.right_inv_lim_motor_temp, label: 'lim_motor_limiter' },
      { active: this.right_inv_lim_igbt_temp, label: 'lim_igbt_limiter' },
    ];
  },
},
})

</script>
