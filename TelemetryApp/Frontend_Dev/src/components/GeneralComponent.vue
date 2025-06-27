<!-- Κάτι σαν AccuGeneralComponent -->
<template>
  <div
      class="flex min-w-full m-2 ml-5 rounded-lg relative"
      :style="{ backgroundColor: ContainerColor }"
  >
    <div
        class="grid gap-1 row-start-1 col-start-2"
        :style="{
        gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))`,
        gridTemplateRows: `repeat(${numRows}, minmax(0, 1fr))`
      }"
    >
      <button
          class=" items-center text-l col-span-1 row-span-1 row-start-1 col-start-1 rounded-lg bg-yellow-200 text-black overflow-hidden"
          @click="toggleInfo"
      >
        <span> {{containername}} </span>
      </button>

      <!-- Loop through the items and create a button for each  -->
      <button
          v-for="(item, index) in items"
          :key="index"
          :class="{
            'flex flex-col justify-start p-1 text-white min-w-full': true,
            'bg-green-500': isBoolean(String(item.label[0])) && item.value && item.value[0]===1,
            'bg-red-500': isBoolean(String(item.label[0])) && item.value && item.value[0]===0,
            'bg-blue-800': (item.value && typeof item.value[0] === undefined) ||  !isBoolean(String(item.label[0])) || item.label[0]===undefined || isBoolean(String(item.label[0])),
            'text-white': true,
            'p-1': true,
            'rounded-lg': true,
            'text-xs': true,
            'text-left': true,
            'text-top': true,
            'overflow-hidden': true, // Hide overflow text
            'cap-size': true // Apply the min-size class

        }"
          @click="showPopup(item)"
      >
        <!-- Show the appropriate content based on the type of item -->
        <template v-if="isBoolean(String(item.label[0])) || item.label[0]==='node_status'"> <!-- write all inclusions for boolean vars. -->
          <span> {{ item?.label?.[0] }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'last_error' || item?.label?.[0] === 'sys_status'">
          <span> {{ item?.label?.[0] }}: <br> {{ printInverterErrors(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'latched_error'">
          <span> {{ item?.label?.[0] }}: <br> {{ printLatchedError(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'aux_hw_status'">
          <span> {{ item?.label?.[0] }}: <br> {{ printAuxHwStatus(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'critical_hw_status'">
          <span> {{ item?.label?.[0] }}: <br> {{ printCriticalHwStatus(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'handler_status'">
          <span> {{ item?.label?.[0] }}: <br> {{ printHandlerStatus(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'actual_inverter_status'">
          <span> {{ item?.label?.[0] }}: <br> {{ printActualInverterStatus(item?.value?.[0]) }} </span>
        </template>
        <template v-else-if="item?.label?.[0] === 'act_control_mode'">
          <span> {{ item?.label?.[0] }}: <br> {{ printActControlMode(item?.value?.[0]) }} </span>
        </template>
        <template v-else>
          <span>{{ item?.label?.[0] }}: <br> {{ item?.value?.[0] }} </span>
        </template>
      </button>
    </div>
    <!-- Popup Box -->

    <div v-if="showPopupFlag" class="popup" :style="{ maxWidth: popupWidth, maxHeight: popupHeight }"> <!-- Adjusted style binding -->
      <!-- Slot for string at the top -->
      <div class="top-space">
        <slot name="top"></slot>
      </div>
      <div class="popup-content">
           {{ popupContent }}
      </div>
      <button @click="closePopup" class="close-btn">Close</button>
    </div>

    <div v-if="showInfoPopup" class="popup" :style="{ maxWidth: popupWidth, maxHeight: popupHeight }"> <!-- Adjusted style binding -->
      <!-- Slot for string at the top -->
      <div class="top-space">
        <slot name="top"></slot>
      </div>
      <div class="popup-content">
        <p v-if="showInfoPopup">This is the {{ containername }} info content.</p>
        <button v-if="showInfoPopup" @click="closeInfoPopup" class="close-btn">Close</button>
      </div>
    </div>

    <!-- Other popup components -->
  </div>
</template>

<script lang="ts">
//import GeneralComponent from "@/components/GeneralComponent.vue";
import {defineComponent} from 'vue';
import { variableContainer } from '../types/live_telemetry'; // Adjust path as necessary

export default defineComponent({
  name: 'GeneralComponent',

  props: {
    items: Array as () => variableContainer[],
    numRows: Number,
    numCols: Number,
    containername: String
  },
  computed: {

  },
  data() {
    return {
      digitCount: 0,
      ContainerColor: '#001f3f', // Dark hue of navy blue color
      showPopupFlag: false,
      showInfoPopup: false,
      popupWidth: '80%', // Initial popup width
      popupContent: '',
      popupHeight: '80%', // Initial popup height
      BooleanList: ['accu_over_60v_dclink', 'accu_air_m_state', 'sd_closed', 'precharge_done', 'pc_flag', 'r2d_flag', 'watchdog_status', 'bspdState',
        'fan_right', 'fan_left', 'pump_right', 'pump_left', 'apps_right_implausibility', 'apps_left_implausibility', 'res_k3_switch', 'res_k2_switch',
        'lim_speed_limiter', 'lim_power_limiter', 'lim_stall_limiter', 'lim_l2t_limiter', 'lim_motor_temp', 'lim_igbt_temp', 'pumps_state', 'service_hatch_fan'
        ] // enniaia lista booleans gia OLA TA CONTAINERS -- {accu}
    };
  },
  methods: {
    rightShift(num: number, index: number): number {
      if (index === 0) {
        return num;
      }
      else {
        return num >> index;
      }
    },
    // Add these two methods
    toggleInfo() {
      this.closeAllPopups();
      this.showInfoPopup = !this.showInfoPopup;
    },
    closeInfoPopup() {
      this.showInfoPopup = false;
    },
    isBoolean(label: string): boolean {
      return this.BooleanList.includes(label);
    },
    printInverterErrors(ind: number) {
      const messages = [
        'INVERTER_OK',
        'OCD_FAULT',
        'INVERTED_PHASE_POLARITY',
        'HW_FAULT',
        'OVERVOLTAGE',
        'UNDERVOLTAGE',
        'IGBT_OVERTEMP',
        'MOTOR_OVERTEMP',
        'ADC_ERROR',
        'ADC_INIT_ERROR',
        'SPI_ERROR',
        'RESOLVER_READ_ERROR',
        'ENDAT_INIT_ERROR',
        'VELOCITY_EXCEEDS_MAXIMUM',
        'PWM_OVERMODULATION',
        'INVERSE_TRANSFORM_TIMEOUT',
        'TIMER_INIT_ERROR',
        'PWN_START_FAILURE',
        'PWN_STOP_FAILURE',
        'INVALID_CONTROL_MODE',
        'CONFIGURATION_ERROR',
        'WHILE1_TIMEOUT',
        'CANRX_ERROR',
        'CANTX_ERROR',
        'CAN_TIMEOUT_ERROR',
        'SUPPLY_3V3_ERROR',
        'SUPPLY_5V0_ERROR',
        'SUPPLY_5V6_ERROR',
        'SUPPLY_12V0_ERROR',
        'VREF_ERROR',
        'NO LV SUPPLY',
        'MCU OVERTEMP',
        'MCU DISABLE IMPLAUSIBILITY',
        'MCU ENABLE IMPLAUSIBILITY',
        'GD DISABLE IMPLAUSIBILITY'
      ];

      return messages[ind] || 'Not Available';
    },
    printLatchedError(ind: number) {
      const messages = [
        'ERROR_RESET',
        'FATAL_ERROR_EXISTING',
        'CRITICAL_ERROR_EXISTING',
        'WARNING_EXISTING'
      ];

      return messages[ind] || 'Not available';
    },
    printHandlerStatus(ind: number): string {
      const messages = [
        'NO_ERRORS',
        'FATAL_ERROR',
        'CRITICAL_ERROR',
        'WARNING',
        'INITIALIZING'
      ];

      return messages[ind] || 'Not available';
    },
    printAuxHwStatus(ind: number): string {
      if (typeof ind !== 'number') return 'Not available';

      const statusMap: { [key: number]: string } = {
        1: 'HW_TSAL_OVER60',
        2: 'HW_DISCHARGE_ENABLED',
        4: 'HW_USB_CONNECTED',
        8: 'HW_ST_LINK_CONNECTED'
      };

      return statusMap[ind] ?? 'Not available';
    },
    printCriticalHwStatus(ind: number): string {
      if (typeof ind !== 'number') return 'Not available';

      const statusMap: { [key: number]: string } = {
        0: 'HW_INVERTER_ENABLED',
        1: 'HW_INVERTER_DISABLED',
        2: 'HW_OCD_A',
        4: 'HW_OCD_B',
        8: 'CC HW_OCD_C',
        16: 'HW_INV_ERROR',
        32: 'HW_OVERVOLTAGE',
        64: 'HW_FAULT_LATCHED',
        128: 'HW_MCU_DISABLE',
        256: 'HW_GD_FLT',
        512: 'HW_GD_RDY_ERROR',
        1024: 'HW_SENSOR_A_DC',
        2048: 'HW_SENSOR_B_DC',
        4096: 'HW_SENSOR_C_DC'
      };

      return statusMap[ind] ?? 'Not available';
    },
    printActualInverterStatus(ind: number): string {
      const messages = [
        'INVERTER_DISABLE', // 0
        'INVERTER_ENABLE'   // 1
      ];

      return messages[ind] || 'Not available';
    },
    printActControlMode(ind: number): string {
      const modes = [
        'CURRENT_CONTROL_MODE', // 0
        'SPEED_CONTROL_MODE',   // 1
        'FAULT_MODE'            // 2
      ];

      return modes[ind] || 'Not available';
    },
    showPopup(item: variableContainer): void {
      this.closeAllPopups();
      if (item.label[0] === undefined || (item.value[0] === undefined )) {
        return;
      }
      let content = ` \n${item.label[0]}: ${item.value[0]}\n `;

      if (item.label[1] !== undefined && item.label[0] === 'node_status') { // node status popup formatting

        if (item.value && item.value[0] === 0) {
          this.popupContent = content;
          this.showPopupFlag = true;
        }
        if (item.value && item.value[0] !== 0) {
          for (let i = 0; i <= 7; i++) { //where: -------  8 === number of labels of node_status
            if (this.rightShift(item.value[0], i) === 1) { //here----------------------------------------------------------------------------------
              content += `\n${item.label[i]}\n`;
            }
          }
        }
      }

      if (item.label[0] === 'handler_status') {
        content = `${item.label[0]} : ${this.printHandlerStatus(item?.value?.[0])}`
      }
      if (item.label[0] === 'aux_hw_status') {
        content = `${item.label[0]}: ${this.printAuxHwStatus(item?.value?.[0])}`
      }
      if (item.label[0] === 'last_error' || item.label[0] === 'sys_status') {
        content = `${item.label[0]} : ${this.printInverterErrors(item?.value?.[0])}`
      }
      if (item.label[0] === 'critical_hw_status') {
        content = `${item.label[0]} : ${this.printCriticalHwStatus(item?.value?.[0])}`
      }
      if (item.label[0] === 'actual_inverter_status') {
        content = `${item.label[0]} : ${this.printActualInverterStatus(item?.value?.[0])}`
      }
      if (item.label[0] === 'act_control_mode') {
        content = `${item.label[0]} : ${this.printActControlMode(item?.value?.[0])}`
      }
      if (item.label[0] === 'latched_error') {
        content = `${item.label[0]} : ${this.printLatchedError(item?.value?.[0])}`
      }

      this.popupContent = content;
      this.showPopupFlag = true;
    },
    closePopup(): void {
      this.showPopupFlag = false;
    },
    closeAllPopups(): void {
      this.showPopupFlag = false;
    }
  }
});
</script>

<style scoped>
.min-size {
  min-width: 90px;
  min-height: 40px;
}

.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: dimgray; /* Darker shade of orange */
  padding: 2%; /* Adjust padding as needed */
  border: 1px solid #ccc;
  border-radius: 5px;
  z-index: 999;
  max-width: 80%; /* Adjust as needed */
  max-height: 80%; /* Adjust as needed */
  overflow: auto; /* Enable scrolling if content exceeds max dimensions */
}
.flex {
  position: relative; /* Ensure the container is positioned relative */
}

.popup-content {
  /* Add styles for the popup content */
}

.cap-size {
  min-width: 90px;
  min-height: 40px;
  max-width: 120px;
  max-height: 40px;
}

.overflow-hidden {
  overflow: hidden;
  text-overflow: ellipsis; /* Show ellipsis for overflow text */
  white-space: nowrap; /* Prevent text from wrapping */
}
</style>
