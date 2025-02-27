<template>
  <div
      class="flex min-w-full m-2 rounded-lg relative"
      :style="{ backgroundColor: AccuContainerColor }"
  >
    <div
        class="grid gap-1 row-start-2 col-start-1"
        :style="{
        gridTemplateColumns: `repeat(${numCols}, minmax(0, 1fr))`,
        gridTemplateRows: `repeat(${numRows}, minmax(0, 1fr))`
      }"
    >
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


      <!-- Loop through the items and create a button for each  -->
<!--      <template v-if="items?.length===0">-->
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
          <template v-if="isBoolean(String(item.label[0]))"> <!-- write all inclusions for boolean vars. -->
            {{ item.label[0] }}
          </template>
          <template v-else> <!-- write all exceptions..... -->
            <div>
              <span>{{ item.label[0]}}:</span>
              <br />
              <span> {{item.value && item.value[0]}} </span>
            </div>
          </template>
        </button>
<!--      </template>-->
<!--      <template v-else>-->
<!--        <button-->
<!--          v-for=""-->
<!--      </template>-->
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
    <div v-if="showBmsErrorPopup || showTsacErrorPopup || showAccuInfoPopup" class="popup" :style="{ maxWidth: popupWidth, maxHeight: popupHeight }"> <!-- Adjusted style binding -->
      <!-- Slot for string at the top -->
      <div class="top-space">
        <slot name="top"></slot>
      </div>
      <div class="popup-content">
        <p v-if="showBmsErrorPopup">This is the BMS Error content.</p>
        <p v-if="showTsacErrorPopup">This is the TSAC Error content.</p>
        <p v-if="showAccuInfoPopup">This is the accu info content.</p>
        <button v-if="showBmsErrorPopup" @click="closeBmsErrorPopup" class="close-btn">Close</button>
        <button v-if="showTsacErrorPopup" @click="closeTsacErrorPopup" class="close-btn">Close</button>
        <button v-if="showAccuInfoPopup" @click="closeAccuInfoPopup" class="close-btn">Close</button>
      </div>
    </div>

    <!-- Other popup components -->
  </div>
</template>





<script lang="ts">
import { defineComponent } from 'vue';
import { variableContainer } from '../types/live_telemetry'; // Adjust path as necessary

export default defineComponent({
  name: 'AccuGeneralComponent',
  props: {
    items: Array as () => variableContainer[],
    numRows: Number,
    numCols: Number
  },
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
      BooleanList: ['over_60v_dclink', 'air_m_state', 'air_m_supp', 'air_p_state', 'air_p_supp', 'precharge_state', 'ts_active', 'vicor_overtemp']
    };
  },
  methods: {
    isBoolean(label: string): boolean {
      return this.BooleanList.includes(label);
    },
    showPopup(item: variableContainer): void {
      this.closeAllPopups();

      if (
          item.label[0] === undefined || (item.value && item.value[0] === undefined)

          // item.value[0] === undefined ||
          // item.label[0] === undefined ||
          // (item.value[1] === undefined && item.label[1] !== undefined) ||
          // (item.value[2] === undefined && item.label[2] !== undefined)
      ) {
        return;
      }

      //let content = `${item.label[0]}: ${item.value[0]}`;
      //let content = `${item.label[0]}: ${item.value && item.value[0] !== undefined ? item.value[0] : 'default value'}`;
      // Assuming item is defined and has a label property and a value property
      let content = `${item.label[0]}: ${item.value ? item.value[0] : ''}`;



      for (let i = 1; i < item.label.length; i++) {
        if (item.label[i] && item.value && item.value[i] !== undefined) {
          content += `${item.label[i]}: ${item.value[i]} `;
        }
      }

      // if (item.label[1] && item.value[1] !== undefined) {
      //   content += ` ${item.label[1]}: ${item.value[1]}`;
      // }
      //
      // if (item.label[2] && item.value[2] !== undefined) {
      //   content += ` ${item.label[2]}: ${item.value[2]}`;
      // }

      this.popupContent = content;
      this.showPopupFlag = true;

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
      //window.removeEventListener('click', this.handleOutsideClick);
    }
  }
});
</script>




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