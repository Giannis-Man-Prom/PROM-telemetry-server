<script lang="ts">
import { defineComponent } from "vue";
import SideBar from "@/components/SideBar.vue";
import SideBarList from "@/components/SideBarList.vue";
import Dashboard from "@/views/Dashboard_vd.vue"; // Import the Dashboard component
import StatusBar from "@/components/StatusBar.vue";
import ShowCustomCharts from "@/views/ShowCustomCharts.vue";
import StatusListComponent from "@/components/StatusListComponent.vue";
import {io} from "socket.io-client";
import {
  variableContainer,
  VehicleTelemetry_data
} from "@/types/live_telemetry.ts";
import {api_res, event_connection_res} from "@/types/socketIO.types.ts";



const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

export default defineComponent({
  name: "App",
  computed: {
    StatusListComponent() {
      return StatusListComponent
    }
  },
  components: {
    SideBar,
    StatusBar,
    Dashboard,
    SideBarList,
    ShowCustomCharts,
  },
  created() {

    this.SideBarListItems = [
      { label: ['R2D']},
      { label: ['precharge_done']},
      { label: ['TS ACTIVE']},
      { label: ['TS ACTIVE']},
      { label: ['TS ACTIVE']},
      { label: ['TS ACTIVE']},
      { label: ['TS ACTIVE'] },
      { label: ['TS ACTIVE']},
      { label: ['max_cell_voltage']}
    ];

    this.StatusItemList = [
      { label: ['radio_rssi']},
      { label: ['radio_packet_loss']},
      { label: ['radio_wrong_crc']},
      { label: ['radio_kbps']},
    ];


    socket.on('telemetry_data', (telemetry_data: api_res) => {
      //Here we are updating the object every time we get a new message from the socket,


      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data) as VehicleTelemetry_data;
      } catch (e) {
        console.error('Invalid JSON string');
        return null;
      }


          this.SideBarListItems = [
            { label: ['R2D'], value: [this.telemetry_data_obj.dv_R2D] },
            { label: ['precharge_done'], value: [this.telemetry_data_obj.accu_precharge_state] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
            { label: ['max_cell_voltage'], value: [this.telemetry_data_obj.accu_max_cell_voltage] }
          ];

        this.StatusItemList = [
          { label: ['radio_rssi'], value: [this.telemetry_data_obj.radio_rssi] },
          { label: ['radio_packet_loss'], value: [parseFloat(this.telemetry_data_obj.radio_packet_loss.toFixed(3))] },
          { label: ['radio_wrong_crc'], value: [this.telemetry_data_obj.radio_wrong_crc] },
          { label: ['radio_kbps'], value: [this.telemetry_data_obj.radio_kbps] },
        ];
    });



    socket.on('connection_response', (message: event_connection_res) => {
      console.log("Connection Status: " + message.status)
    });

  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data, //Object as typeof VehicleTelemetry_data
      SideBarListItems: [] as variableContainer,
      StatusItemList: [] as variableContainer,
      fake_packet_obj: {} as VehicleTelemetry_data
    }
  }
});
</script>
<template>
<!--  <v-app class="flex min-h-screen">-->
  <div class="flex min-h-screen">
    <side-bar
      :items="SideBarListItems"
    />

    <StatusBar
      :items="StatusItemList"
    />
<!--      <template v-slot:custom-list>-->
<!--        &lt;!&ndash; Here we will add our own list items that we need to the vd dashboard component &ndash;&gt;-->
<!--&lt;!&ndash;        <SideBarList&ndash;&gt;-->
<!--&lt;!&ndash;            :R2D="R2D"&ndash;&gt;-->
<!--&lt;!&ndash;            :Precharge_done="Precharge_done"&ndash;&gt;-->
<!--&lt;!&ndash;            :SDC_open="SDC_open"&ndash;&gt;-->
<!--&lt;!&ndash;            :min_accu="min_accu"&ndash;&gt;-->
<!--&lt;!&ndash;            :min_LV="min_LV"&ndash;&gt;-->
<!--&lt;!&ndash;            :max_accu="max_accu"&ndash;&gt;-->
<!--&lt;!&ndash;            :max_LV="max_LV"&ndash;&gt;-->
<!--&lt;!&ndash;            :SoC="SoC"&ndash;&gt;-->
<!--&lt;!&ndash;        />&ndash;&gt;-->


<!--        &lt;!&ndash; Add more custom list items as needed &ndash;&gt;-->
<!--        <ul class="space-y-2 font-medium">-->
<!--          &lt;!&ndash; Add more custom list items as needed &ndash;&gt;-->
<!--        </ul>-->
<!--        &lt;!&ndash; End of custom list items &ndash;&gt;-->
<!--      </template>-->

      <div>
      <!-- Here the main page and components will be rendered -->
        <router-view/>
      </div>

  </div>
</template>



<style scoped>
/* Add your scoped styles here */
</style>
