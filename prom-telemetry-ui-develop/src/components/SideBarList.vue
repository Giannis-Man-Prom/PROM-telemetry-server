<template>
  <aside id="default-sidebar" class="max-w-56 transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
    <div class="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
      <ul class="space-y-2 font-medium">
        <!-- Boolean variables -->
        <li>
          <button :class="{'bg-green-500': R2D, 'bg-red-500': !R2D}" class="flex items-center p-2 text-white rounded-full min-w-full">
            <span class="ms-3">R2D</span>
          </button>
        </li>
        <li>
          <button :class="{'bg-green-500': Precharge_done, 'bg-red-500': !Precharge_done}" class="flex items-center p-2 text-white rounded-full min-w-full">
            <span class="ms-3">Precharge_done</span>
          </button>
        </li>
        <li>
          <button :class="{'bg-green-500': SDC_open, 'bg-red-500': !SDC_open}" class="flex items-center p-2 text-white rounded-full min-w-full">
            <span class="ms-3">SDC_open</span>
          </button>
        </li>

        <!-- Integer variables -->
        <li>Min_accu: {{  }}</li>
        <li>Min_LV: {{ min_LV }}</li>
        <li>Max_accu: {{ max_accu }}</li>
        <li>Max_LV: {{ max_LV }}</li>
        <li>SoC: {{ SoC }}</li>
      </ul>
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
//import { telemetry_data_obj, AccuContainerItems, SensorsContainerItems, InverterContainerItems, MotorContainerItems, PDUContainerItems, DVContainerItems, VCUContainerItems, SideBarListItems} from '@/ContainerData/TelemetryData.ts';


export default defineComponent({
  name: 'SideBarList',
  props: {
    R2D: Number,
    Precharge_done: Boolean,
    SDC_open: Boolean,
    min_cell_temp: Number,
    min_LV: Number,
    max_accu: Number,
    max_LV: Number,
    SoC: Number
  },
  data(){
    return {
      // Initialize R2D variable
      BooleanList: ['R2D', 'Precharge_done', 'SDC_open', 'air_p_state', 'air_p_supp', 'precharge_state', 'ts_active', 'vicor_overtemp']

    };
  },
  created() {
    // Set R2D value from telemetry data
    //this.R2D = telemetry_data_obj.R2d;
  }
});
</script>

<style scoped>
</style>
