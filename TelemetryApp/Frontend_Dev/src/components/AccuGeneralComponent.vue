<!-- Αρχικά ορίζουμε πως θα μοιάζει το component -->
<template>
  <!-- Αρχικά φτιάχνουμε το container που θα βρίσκεται γύρω από τα κουτάκια και θα είναι flex min-h ... -->
  <div
      class="flex min-w-full m-2 rounded-lg relative"
      :style="{ backgroundColor: AccuContainerColor }"
  >
  <!-- Στην συνέχεια μέσα του ορίζουμε grid -->
  <!-- Για γραμμές στήλες, φτιάχνουμε όσες και τα numCols, numRows και κάθε κελί θα είναι από μηδενικό, πολύ μικρό, 
  μέχει και 1fr (1 fraction του χωρου) το οποίο σημαίνει ότι όλα θα ειναι ομοιόμορφα -->
    <div
        class="grid gap-1 row-start-2 col-start-1"
        :style="{
        gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))`,
        gridTemplateRows: `repeat(${numRows}, minmax(0, 1fr))`
      }"
    >
      <!-- Από εδώ και κάτω ορίζουμε τα buttons που θα χρησιμοποιήσουμε -->
      <!-- Κάποια έχουν onclick που κάνουν trigger μία συνάρτηση popup που ορίζεται παρακάτω στο defineComponent -->
      <button
          class="items-center text-l col-span-1 row-span-1 row-start-1 col-start-1 rounded-lg bg-yellow-200 text-black overflow-hidden"
          @click="toggleAccuInfo"
      >
        <span>ACCU</span>
      </button>

      <button
          class="flex flex-col col-span-2 row-span-1 col-start-2 row-start-1 items-start justify-start p-1 text-white min-w-full bg-purple-800 rounded-lg text-xs text-center overflow-hidden"
          @click="toggleBmsError"
      >
        <span> BMS ERROR:</span>
        <span>(click to see past Errors)</span>
      </button>

      <button
          class="flex flex-col col-span-2 row-span-1 col-start-4 row-start-1 items-start justify-start p-1 text-white min-w-full bg-purple-800 rounded-lg text-xs overflow-hidden"
          @click="toggleTsacError"
      >
        <span>TSAC ERROR:</span>
        <span>(click to see past Errors)</span>
      </button>


      <!-- Items είναι τα δεδομένα που παίρνουμε και πάνω σε αυτά κάνουμε loop για να φτιάξουμε τα υπόλοιπα κουμπιά -->
      <!-- <template v-if="items?.length===0">-->
      <!-- Όταν έχουμε Boolean μεταβλητές τότε ορίζουμε το κουτί να είναι πράσινο/κόκκινο ενώ το default είναι μπλε -->
        <button
            v-for="(item, index) in items"
            :key="index"
            :class="{ //Εδώ ορίζουμε το πως θα μοιάζει το κουτί
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
          <!-- Αν έχουμε boolean τότε μας νοιάζει μόνο το πράσινο/κόκκινο -->
          <template v-if="isBoolean(String(item.label[0]))"> <!-- write all inclusions for boolean vars. -->
            {{ item.label[0] }}
          </template>
          <template v-else-if="item?.label[0] === 'tsac_error'">                       <!-- INVERTER LAST ERROR -->
            <span> {{ item?.label[0] }}: <br> {{ printTSACerror(item?.value?.[0]) }} </span>
          </template>
          <template v-else-if="item?.label[0] === 'bms_error'">                       <!-- INVERTER LAST ERROR -->
            <span> {{ item?.label[0] }}: <br> {{ printBMSerror(item?.value?.[0]) }} </span>
          </template>
          <template v-else-if="item?.label[0] === 'last_tsac_error'">                       <!-- INVERTER LAST ERROR -->
            <span> {{ item?.label[0] }}: <br> {{ printTSACerror(item?.value?.[0]) }} </span>
          </template>
          <template v-else-if="item?.label[0] === 'last_bms_error'">                       <!-- INVERTER LAST ERROR -->
            <span> {{ item?.label[0] }}: <br> {{ printBMSerror(item?.value?.[0]) }} </span>
          </template>
          <template v-else-if="item?.label[0] === 'dynamic_mode'">                       <!-- INVERTER LAST ERROR -->
            <span> {{ item?.label[0] }}: <br> {{ printDynamic(item?.value?.[0]) }} </span>
          </template>
          <!-- Αλλιώς θέλουμε και όνομα και τιμή -->
          <template v-else> <!-- write all exceptions..... -->
            <div>
              <span>{{ item.label[0]}}:</span>
              <br />
              <span> {{item.value && item.value[0]}} </span>
            </div>
          </template>

        </button>
    </div>

    <!-- Popup Box -->
    <div v-if="showPopupFlag" class="popup" :style="{ maxWidth: popupWidth, maxHeight: popupHeight }"> <!-- Adjusted style binding -->
      <!-- Slot for string at the top -->
      <div class="top-space">
        <slot name="top">

        </slot>
      </div>
      <div class="popup-content">
        {{ popupContent }}
      </div>
      <button @click="closePopup" class="close-btn">Close</button>
    </div>
    <!-- Όταν κάποιο button είναι assigned για να έχει ειδικό popup τότε έχουμε το από κάτω και παίρνουμε περιπτώσεις-->
    <div v-if="showBmsErrorPopup || showTsacErrorPopup || showAccuInfoPopup" class="popup" :style="{ maxWidth: popupWidth, maxHeight: popupHeight }"> <!-- Adjusted style binding -->
      <!-- Slot for string at the top -->
      <div class="top-space">
        <slot name="top"></slot>
      </div>
      <div class="popup-content">
        <p v-if="showBmsErrorPopup"> BMS Error: {{ printBMSerror(items?.[14].value?.[0]) }} </p>
        <p v-if="showTsacErrorPopup"> TSAC Error: {{ printTSACerror(items?.[15].value?.[0]) }}</p>
        <p v-if="showAccuInfoPopup">This is the accu info content.</p>
        <button v-if="showBmsErrorPopup" @click="closeBmsErrorPopup" class="close-btn">Close</button>
        <button v-if="showTsacErrorPopup" @click="closeTsacErrorPopup" class="close-btn">Close</button>
        <button v-if="showAccuInfoPopup" @click="closeAccuInfoPopup" class="close-btn">Close</button>
      </div>
    </div>

  </div>
</template>

<!-- Εδώ αρχίζει το component definition -->
<script lang="ts">
import { defineComponent } from 'vue';
import { variableContainer } from '../types/live_telemetry'; // Adjust path as necessary

export default defineComponent({
  name: 'AccuGeneralComponent',
  /* Τα props είναι αυτά που περνάνε στο component */
  props: {
    items: Array as () => variableContainer[],
    numRows: Number,
    numCols: Number
  },
  /* Στο data κρατάμε το state του component, εδώ ορίζουμε τι θα είναι boolean για πριν */
  data() {
    return {
      AccuContainerColor: '#001f3f',
      showBmsErrorPopup: false,
      showTsacErrorPopup: false,
      showAccuInfoPopup: false,
      showPopupFlag: false,
      popupContent: '',
      popupWidth: '80%',
      popupHeight: '80%',
      BooleanList: ['over_60v_dclink', 'air_m_state', 'air_m_supp', 'air_p_state', 'air_p_supp', 'precharge_state', 'ts_active', 'vicor_overtemp', 'imd_sd_state', 'imd_ok', 'ams_sd_state', 'ams_ok']
    };
  },
  /* Εδώ έχουμε όλες τις συναρτήσεις που χρησιμοποιήσαμε πριν για να βλέπουμε αν κάτι είναι boolean και για τα popup/κουμπιά */
  methods: {
    isBoolean(label: string): boolean {
      return this.BooleanList.includes(label);
    },
    printBMSerror(ind: number) {
      const messages = [
        'BMS_OK',
        'BMS_OVERVOLTAGE',
        'BMS_UNDERVOLTAGE',
        'OVERCURRENT_CHARGE',
        'OVERCURRENT_DISCHARGE',
        'OVERTEMP',
        'UNDERTEMP',
        'ISABELLE_DEAD',
        'COMMUNICATION_ERROR',
        'SLAVE_ERROR',
        'HUMIDITY_ERROR',
        'ISABELLE_NO_VOLTAGE',
        'OVERCURRENT',
        'OVERCURRENT_REGEN'
      ];

      return messages[ind] || 'Unknown BMS error';
    },
    printTSACerror(ind: number) {
      const messages = [
        'TSAC_OK',
        'IMD_ERROR',
        'AVI_STATUS_ERROR',
        'AIR_M_STUCK',
        'AIR_P_STUCK',
        'AIR_M_IMPLAUSIBILITY',
        'AIR_P_IMPLAUSIBILITY',
        'PC_RELAY_IMPLAUSIBILITY',
        'PC_CIRCUIT_ERROR',
        'DCDC_OVERTEMP',
        'ELCON_HW_FAILURE',
        'ELCON_OVERTEMP_PROTECTION',
        'ELCON_INPUT_ERROR',
        'ELCON_REVERSE_POLARITY',
        'ELCON_COMMUNICATION_ERROR'
      ];
      return messages[ind] || 'Unknown TSAC error';
    },
    printDynamic(ind: number) {
      const messages = [
        'Inspection',
        'Testing',
        'Track',
        'Charging',
      ];

      return messages[ind] || 'Unknown Value';
    },
    showPopup(item: variableContainer): void {
      this.closeAllPopups();

      if (
          item.label[0] === undefined || (item.value && item.value[0] === undefined)
      ) {
        return;
      }

      let content = `${item.label[0]}: ${item.value ? item.value[0] : ''}`;

      for (let i = 1; i < item.label.length; i++) {
        if (item.label[i] && item.value && item.value[i] !== undefined) {
          content += `${item.label[i]}: ${item.value[i]} `;
        }
      }
      if (item.label[0] == 'last_tsac_error') {
        content = `${item.label[0]}: ${this.printTSACerror(item?.value?.[0])} `;
      }
      if (item.label[0] == 'last_bms_error') {
        content = `${item.label[0]}: ${this.printBMSerror(item?.value?.[0])} `;
      }
      if (item.label[0] == 'dynamic_mode') {
        content = `${item.label[0]}: ${this.printDynamic(item?.value?.[0])} `;
      }
      if (item.label[0] == 'tsac_error') {
        content = `${item.label[0]}: ${this.printTSACerror(item?.value?.[0])} `;
      }
      if (item.label[0] == 'bms_error') {
        content = `${item.label[0]}: ${this.printBMSerror(item?.value?.[0])} `;
      }

      this.popupContent = content;
      this.showPopupFlag = true;

    },
    closePopup(): void {
      this.showPopupFlag = false;
    },

    toggleBmsError(): void {
      this.closeAllPopups();
      this.showBmsErrorPopup = !this.showBmsErrorPopup;
    },
    closeBmsErrorPopup(): void {
      this.showBmsErrorPopup = false;
    },
    toggleTsacError(): void {
      this.closeAllPopups();
      this.showTsacErrorPopup = !this.showTsacErrorPopup;
    },
    closeTsacErrorPopup(): void {
      this.showTsacErrorPopup = false;
    },
    toggleAccuInfo(): void {
      this.closeAllPopups();
      this.showAccuInfoPopup = !this.showAccuInfoPopup;
    },
    closeAccuInfoPopup(): void {
      this.showAccuInfoPopup = false;
    },
    closeAllPopups(): void {
      this.showPopupFlag = false;
      this.showBmsErrorPopup = false;
      this.showTsacErrorPopup = false;
      this.showAccuInfoPopup = false;
    },
  }
});
</script>

<!-- Εδώ κάνουμε css styling στα παραπάνω όπως στα popups -->
<style scoped>

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

.cap-size {
  min-width: 90px;
  min-height: 40px;
  max-width: 120px;
  max-height: 48px;
}

.overflow-hidden {
  overflow: hidden;
  text-overflow: ellipsis; /* Show ellipsis for overflow text */
  white-space: nowrap; /* Prevent text from wrapping */
}

</style>