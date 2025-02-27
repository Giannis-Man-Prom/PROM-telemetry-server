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
          <span> {{ item.label[0] }} </span>
        </template>


        <template v-if="item.label[0] === 'as_status' "> <!-- fix for ith- msb ----2^k-------------------->
          <template v-if="item.value && rightShift(item.value[0], 0) === 1">
            <span> AS OFF </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 1) === 1">
            <span> AS READY </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 2) === 1">
            <span> AS DRIVING </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 3) === 1">
            <span> AS FINISHED </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 4) === 1">
            <span> AS EMERGENCY </span>
          </template>
        </template>

        <template v-if="item.label[0] === 'critical_hw_status' "> <!-- fix for ith- msb !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->
          <template v-if="item.value && rightShift(item.value[0], 0) === 1">
            <span> {{item.label[0]}}: {{item.value[0]}} <br> HW_TSAL_OVER60 </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 1) === 1">
            <span> {{item.label[0]}}: {{item.value[0]}} <br>  HW_DISCHARGE_ENABLED </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 2) === 1">
            <span> {{item.label[0]}}: {{item.value[0]}} <br>  HW_USB_CONNECTED </span>
          </template>
          <template v-if="item.value && rightShift(item.value[0], 3) === 1">
            <span> {{item.label[0]}}: {{item.value[0]}} <br>  HW_ST_LINK_CONNECTED </span>
          </template>
        </template>

        <template v-if="item.label[0] === 'aux_hw_status' "> <!-- fix for ith- msb !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->
          <template v-if="item.value && item.value[0] === 0">
            <span> aux_hw-status: <br> NO_ERRORS </span>
          </template>
          <template v-if="item.value && item.value[0] === 1">
            <span> aux_hw-status: <br> FATAL_ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 2">
            <span> aux_hw-status: <br> CRITICAL_ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 3">
            <span>aux_hw-status: <br> WARNING </span>
          </template>
          <template v-if="item.value && item.value[0] === 4">
            <span> aux_hw-status: <br> INITIALIZING </span>
          </template>
        </template>

        <template v-if="item.label[0] === 'latched_error' "> <!-- fix for ith- msb !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->
          <template v-if="item.value && item.value[0] === 0">
            <span> latched_error: <br>
              ERROR_RESET </span>
          </template>
          <template v-if="item.value &&item.value[0] === 1">
            <span> latched_error: <br>
              CRITICAL_ERROR_EXISTING </span>
          </template>
          <template v-if="item.value && item.value[0] === 2">
            <span> latched_error: <br>
              WARNING_EXISTING </span>
          </template>

        </template>



        <template v-if="item.label[0] === 'last_error' ">                       <!-- INVERTER LAST ERROR -->
          <template v-if="item.value && item.value[0] === 0">
            <span> last_error: <br> INVERTER OK </span>
          </template>
          <template v-if="item.value && item.value[0] === 1">
            <span> last_error: <br> OCD FAULT </span>
          </template>
          <template v-if="item.value && item.value[0] === 2">
            <span> last_error: <br> CC FAILURE </span>
          </template>
          <template v-if="item.value && item.value[0] === 3">
            <span> last_error: <br> SHORT </span>
          </template>
          <template v-if="item.value && item.value[0] === 4">
            <span> last_error: <br> CC WATCHDOG ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 5">
            <span> last_error: <br> OVERVOLTAGE </span>
          </template>
          <template v-if="item.value && item.value[0] === 6">
            <span> last_error: <br> UNDERVOLTAGE </span>
          </template>
          <template v-if="item.value && item.value[0] === 7">
            <span> last_error: <br> IGBT OVERTEMP </span>
          </template>
          <template v-if="item.value && item.value[0] === 8">
            <span> last_error: <br> MOTOR OVERTEMP </span>
          </template>
          <template v-if="item.value && item.value[0] === 9">
            <span> last_error: <br> ADC ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 10">
            <span> last_error: <br> ADC INIT ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 11">
            <span> last_error: <br> SPI ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 12">
            <span> last_error: <br> ENCODER READ ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 13">
            <span> last_error: <br> ENDAT INIT ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 14">
            <span> last_error: <br> VELOCITY EXCEEDS MAXIMUM </span>
          </template>
          <template v-if="item.value && item.value[0] === 15">
            <span> last_error: <br> PWM OVERMODULATION </span>
          </template>
          <template v-if="item.value && item.value[0] === 16">
            <span> last_error: <br> INVERSE TRANSFORM TIMEOUT </span>
          </template>
          <template v-if="item.value && item.value[0] === 17">
            <span> last_error: <br> CANRX ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 18">
            <span> last_error: <br> CANTX ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 19">
            <span> last_error: <br> CAN TIMEOUT ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 20">
            <span> last_error: <br> SUPPLY 3V3 ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 21">
            <span> last_error: <br> SUPPLY 5V0 ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 22">
            <span> last_error: <br> VREF ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 23">
            <span> last_error: <br> INVERTED PHASE POLARITY </span>
          </template>
          <template v-if="item.value && item.value[0] === 24">
            <span> last_error: <br> TIMER INIT ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 25">
            <span> last_error: <br> PWM START FAILURE </span>
          </template>
          <template v-if="item.value && item.value[0] === 26">
            <span> last_error: <br> PWM STOP FAILURE </span>
          </template>
          <template v-if="item.value && item.value[0] === 27">
            <span> last_error: <br> MCU DISABLE IMPLAUSIBILITY </span>
          </template>
          <template v-if="item.value && item.value[0] === 28">
            <span> last_error: <br> MCU ENABLE IMPLAUSIBILITY </span>
          </template>
          <template v-if="item.value && item.value[0] === 29">
            <span> last_error: <br> GD DISABLE IMPLAUSIBILITY </span>
          </template>
          <template v-if="item.value && item.value[0] === 30">
            <span> last_error: <br> GD ENABLE IMPLAUSIBILITY </span>
          </template>
          <template v-if="item.value && item.value[0] === 31">
            <span> last_error: <br> HW FAULT </span>
          </template>
          <template v-if="item.value && item.value[0] === 32">
            <span> last_error: <br> WHILE1 TIMEOUT </span>
          </template>
          <template v-if="item.value && item.value[0] === 33">
            <span> last_error: <br> INVALID CONTROL MODE </span>
          </template>
          <template v-if="item.value && item.value[0] === 34">
            <span> last_error: <br> EXCESSIVE REGEN REQUESTED </span>
          </template>
          <template v-if="item.value && item.value[0] === 35">
            <span> last_error: <br> EXCESSIVE REGEN DETECTED </span>
          </template>
          <template v-if="item.value && item.value[0] === 36">
            <span> last_error: <br> CONFIGURATION ERROR </span>
          </template>
          <template v-if="item.value && item.value[0] === 37">
            <span> last_error: <br> MCU OVERTEMP </span>
          </template>
          <template v-if="item.value && item.value[0] === 38">
            <span> last_error: <br> NO LV SUPPLY </span>
          </template>
        </template>

        <template v-if="item.label[0]!=='node_status' && item.label[0]!=='critical_hw_status'  && item.label[0]!=='latched_error' && item.label[0]!=='aux_hw_status' && !isBoolean(String(item.label[0])) && item.label[0]!=='last_error'  "> <!-- write all exceptions..... -->
          <div>
            <span>{{ item.label[0] }}: </span>
            <br />
            <template v-if="item.label && item.label[0] !== undefined">
              <span v-if="item.value && item.value[0] !== undefined"> {{ item.value[0] }} </span>
            </template>

          </div>
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

        <p v-if="showInfoPopup">This is the accu info content.</p>
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
    showPopup(item: variableContainer): void {
      this.closeAllPopups();
      if (item.value )
      if (
          item.label[0] === undefined || (item.value[0] === undefined )

          // item.value1 === undefined ||
          // item.label1 === undefined ||
          // (item.value2 === undefined && item.label2 !== undefined) ||
          // (item.value3 === undefined && item.label3 !== undefined) ||
          // (item.value4 === undefined && item.label4 !== undefined) || ------------CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!
          // (item.value5 === undefined && item.label5 !== undefined) ||
          // (item.value6 === undefined && item.label6 !== undefined) ||
          // (item.value7 === undefined && item.label7 !== undefined) ||
          // (item.value8 === undefined && item.label8 !== undefined)
      ) {
        return;
      }
      if (item.value ) {
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
            // this.popupContent = content;
            // this.showPopupFlag = true;
            // return;
          }
        }

        if (item.label[0] === 'latched_error') { // latched_error formatting
          if (item.value[0] === 0) {
            content += `\n ERROR_RESET\n`;
          }
          if (item.value[0] === 1) {
            content += `\n CRITICAL_ERROR_EXISTING\n`;
          }
          if (item.value[0] === 2) {
            content += `\n WARNING_EXISTING\n`;
          }
        }

        if (item.label[0] === 'critical_hw_status') { // critical_hw_status formatting
          if (this.rightShift(item.value[0], 0) === 1) {
            content += `\n HW_TSAL_OVER60\n`;
          }
          if (this.rightShift(item.value[0], 1) === 1) {
            content += `\n HW_DISCHARGE_ENABLED\n`;
          }
          if (this.rightShift(item.value[0], 2) === 1) {
            content += `\n HW_USB_CONNECTED \n`;
          }
          if (this.rightShift(item.value[0], 3) === 1) {
            content += `\n HW_ST_LINK_CONNECTED \n`;
          }

        }

        if (item.label[0] === 'aux_hw_status') {
          if (item.value[0] === 0) {
            content += `\n NO_ERRORS\n`;
          }
          if (item.value[0] === 1) {
            content += `\n FATAL_ERROR \n`;
          }
          if (item.value[0] === 2) {
            content += `\n CRITICAL_ERROR\n`;
          }
          if (item.value[0] === 3) {
            content += `\n WARNING \n`;
          }
          if (item.value[0] === 4) {
            content += `\n INITIALIZING \n`;
          }
        }

        if (item.label[0] === 'last_error') {
          switch (item.value[0]) {
            case 0:
              content += `\n INVERTER OK\n`;
              break;
            case 1:
              content += `\n OCD FAULT \n`;
              break;
            case 2:
              content += `\n CC FAILURE \n`;
              break;
            case 3:
              content += `\n SHORT \n`;
              break;
            case 4:
              content += `\n CC WATCHDOG ERROR \n`;
              break;
            case 5:
              content += `\n OVERVOLTAGE \n`;
              break;
            case 6:
              content += `\n UNDERVOLTAGE \n`;
              break;
            case 7:
              content += `\n IGBT OVERTEMP \n`;
              break;
            case 8:
              content += `\n MOTOR OVERTEMP \n`;
              break;
            case 9:
              content += `\n ADC ERROR \n`;
              break;
            case 10:
              content += `\n ADC INIT ERROR \n`;
              break;
            case 11:
              content += `\n SPI ERROR \n`;
              break;
            case 12:
              content += `\n ENCODER READ ERROR \n`;
              break;
            case 13:
              content += `\n ENDAT INIT ERROR \n`;
              break;
            case 14:
              content += `\n VELOCITY EXCEEDS MAXIMUM \n`;
              break;
            case 15:
              content += `\n PWM OVERMODULATION \n`;
              break;
            case 16:
              content += `\n INVERSE TRANSFORM TIMEOUT \n`;
              break;
            case 17:
              content += `\n CANRX ERROR \n`;
              break;
            case 18:
              content += `\n CANTX ERROR \n`;
              break;
            case 19:
              content += `\n CAN TIMEOUT ERROR \n`;
              break;
            case 20:
              content += `\n SUPPLY 3V3 ERROR \n`;
              break;
            case 21:
              content += `\n SUPPLY 5V0 ERROR \n`;
              break;
            case 22:
              content += `\n VREF ERROR \n`;
              break;
            case 23:
              content += `\n INVERTED PHASE POLARITY \n`;
              break;
            case 24:
              content += `\n TIMER INIT ERROR \n`;
              break;
            case 25:
              content += `\n PWM START FAILURE \n`;
              break;
            case 26:
              content += `\n PWM STOP FAILURE \n`;
              break;
            case 27:
              content += `\n MCU DISABLE IMPLAUSIBILITY \n`;
              break;
            case 28:
              content += `\n MCU ENABLE IMPLAUSIBILITY \n`;
              break;
            case 29:
              content += `\n GD DISABLE IMPLAUSIBILITY \n`;
              break;
            case 30:
              content += `\n GD ENABLE IMPLAUSIBILITY \n`;
              break;
            case 31:
              content += `\n HW FAULT \n`;
              break;
            case 32:
              content += `\n WHILE1 TIMEOUT \n`;
              break;
            case 33:
              content += `\n INVALID CONTROL MODE \n`;
              break;
            case 34:
              content += `\n EXCESSIVE REGEN REQUESTED \n`;
              break;
            case 35:
              content += `\n EXCESSIVE REGEN DETECTED \n`;
              break;
            case 36:
              content += `\n CONFIGURATION ERROR \n`;
              break;
            case 37:
              content += `\n MCU OVERTEMP \n`;
              break;
            case 38:
              content += `\n NO LV SUPPLY \n`;
              break;
            default:
              content += ''; // Handle default case if necessary
              break;
          }
        }


        this.popupContent = content;
        this.showPopupFlag = true;
      }

      //if item.label[0]==node_status && sum==0 ==> content = dk
      //if item.label[0]==node_status && sum !=0 ==> for all content: content=content++ tespa, display all content whose msb!=0



      //window.addEventListener('click', this.handleOutsideClick);
    },
    closePopup(): void {
      this.showPopupFlag = false;
      //window.removeEventListener('click', this.handleOutsideClick);
    },
    // handleOutsideClick(event: MouseEvent): void {
    //   const popupContent = this.$refs.popupContent as HTMLElement;
    //   if (popupContent && !popupContent.contains(event.target)) { /// maybe should be deleted---------------------------------------------
    //     this.closePopup();
    //   }
    // },
    closeAllPopups(): void {
      this.showPopupFlag = false;
      //window.removeEventListener('click', this.handleOutsideClick);
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
