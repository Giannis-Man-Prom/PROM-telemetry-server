<!-- Εδώ φτιάχνουμε το Sidebar που δείχνει το εικονίδιο μέχρι και το dropdown -->

<template>
  <aside id="default-sidebar" class="fixed transition-transform sm:translate-x-0 z-40 w-40 h-screen bg-gray-50 dark:bg-gray-800 ">
    <div class="h-full px-3 py-4 overflow-y-auto">
      <div class="mb-4 ml-12">
        <img src="@/assets/prom_logo.png" alt="Sidebar Image" class="w-13 h-13 rounded-full">
      </div>
      <ul class="space-y-2 font-medium">
        <!-- Render sidebar items using props -->
        <li v-for="(item, index) in items" :key="index">
          <a href="#" class="flex items-center p-0 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
            <button v-if="item.label" :class="{
              'bg-green-500 items-center p-2 text-white text-base justify-center rounded-lg min-w-full': isBoolean(String(item.label[0])) && lastNumber[item.label[0]] === 1,
              'bg-red-500 items-center p-2 text-white text-base justify-center rounded-lg min-w-full': isBoolean(String(item.label[0])) && lastNumber[item.label[0]] === 0,
              'bg-blue-900 items-center p-2 text-white text-base justify-center rounded-lg min-w-full': (!isBoolean(String(item.label[0]))),
              'overflow-hidden': true,
              'items-center p-2 text-white text-base justify-center rounded-lg min-w-full': true
            }" class="flex">
              <!-- Display the label -->
              <span>{{ item.label[0] }}:</span>
              <br v-if="!isBoolean(String(item.label[0]))">
              <!-- Show item.value[0] if it's defined; otherwise, show the last known value -->
              <span v-if="!isBoolean(String(item.label[0]))" > {{ item.value && item.value[0] !== undefined ? item.value[0] : lastNumber[item.label[0]] }}</span>

            </button>
          </a>
        </li>
        <li>
          <div class="relative">
            <button @click="toggleDropdown" class="flex items-center justify-between w-30 p-2 mt-33 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group focus:outline-none">
              <span>Navigation</span>
              <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M6.293 7.293a1 1 0 011.414 0L10 9.586l2.293-2.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"/>
              </svg>
            </button>
            <ul v-if="isDropdownOpen" class="absolute left-0 z-30 w-40 mt-2 ml-0 origin-top-right bg-white border border-gray-200 rounded-md shadow-lg dark:bg-gray-800 dark:border-gray-700">
              <!-- Εδώ βλέπουμε πως είναι linked μέσω του router τα κουμπιά -->
              <li>
                <router-link to="/" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Live Values</router-link>
              </li>
              <li>
                <router-link to="/accuview" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">ACCU</router-link>
              </li>
              <li>
                <router-link to="/invview" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">INVERTERS</router-link>
              </li>
              <li>
                <router-link to="/sensorsview" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">SENSORS</router-link>
              </li>
              <li>
                <router-link to="/vcuview" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">VCU</router-link>
              </li>
              <li>
                <router-link to="/vd/telemetry" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">VD View</router-link>
              </li>
              <li>
                <router-link to="/charts" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Custom Charts</router-link>
              </li>
              <li>
                <router-link to="/vd-csv" class="block px-4 py-2 text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">CSV VD</router-link>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </aside>
</template>




<script lang="ts">
import { defineComponent } from 'vue';
//import { telemetry_data_obj } from '@/ContainerData/TelemetryData.ts';
//import {variableContainer, VehicleTelemetry_data} from "@/types/live_telemetry.ts";

import SideBar from '@/components/SideBar.vue';
import { sidebarItems, variableContainer, VehicleTelemetry_data } from '../types/live_telemetry.ts';

export default defineComponent({
  name: 'SideBar',
  data() {
    return {
      //sidebaritemlist: [] as sidebarItems[],
      lastNumber: {} as Record<string, any>,
      BooleanList: ['R2D', 'precharge_done', 'TS ACTIVE', 'SDC_open', 'air_p_state', 'air_p_supp', 'precharge_state', 'ts_active', 'vicor_overtemp'],
      DropletColor: '#001f3f', // Dark hue of navy blue color
      isDropdownOpen:false,
      lastKnownValue: []  // Store the last known values for each item
    }
  },
  props: {
    items: Array as () => sidebarItems[]
  },
  created() {
    if (this.items != undefined) {
    this.items.forEach(item => {
      this.lastNumber[item.label[0]] = item.value ? item.value[0] : undefined;
    });
    }
  },
  watch: {
    items: {
      handler(newItems) {
        newItems.forEach(item => {
          if (item.value && item.value[0] !== undefined) {
            // Update the last number in the dictionary
            this.lastNumber[item.label[0]] = item.value[0];
          }
        });
      },
      deep: true,
    },
  },
  methods: {
    isBoolean(label: string): boolean {
      return this.BooleanList.includes(label);
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    // lastnumber(label: string): number {
    //
    // }
  }
});
</script>

<style scoped>
/* Add your scoped styles here */
</style>
