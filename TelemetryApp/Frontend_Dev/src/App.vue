<!-- Εδώ μέσα φτιάχνουμε το script που θα δημιοργήσουμε το custom Vue component μας -->
<script lang="ts">
//Εισάγουμε το Vue definecomponent για να ορίσουμε από κάτω ένα δικό μας μαζί με το configuration του
import { defineComponent } from "vue";
//Εισάγουμε άλλα δικά μας components, components είναι blocks που δομούν τον κώδικα
import SideBar from "@/components/SideBar.vue";
import VD_View from "@/views/VD_View.vue"; // Import the VD_View component
import StatusBar from "@/components/StatusBar.vue";
import CustomCharts from "@/views/CustomCharts.vue";
import {io} from "socket.io-client";
//Εδώ είναι το data type που χρησιμοποιείται για την τηλεμετρία
import {
  variableContainer,
  VehicleTelemetry_data
} from "./types/live_telemetry.ts";

import {api_res, event_connection_res} from "./types/socketIO.types.ts";


//Χρησιμοποιεί το socket για να λαμβάνει από το back-end, παίρνει την διεύθυνση απο το env.VITE_SOCKET_URL
const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

//Εδώ φτιάχνουμε το component μας
export default defineComponent({
  name: "App",
  //Εδώ είναι τα components που ενσωματώνει το vue component
  components: {
    SideBar,
    StatusBar,
    VD_View,
    CustomCharts,
  },
  //Τρέχει όταν δημιουργείται και κάνει αρχικοποιήσεις τιμών και φροντίζει για την επικοινωνία
  created() {
    this.SideBarListItems = [
      { label: ['R2D']},
      { label: ['precharge_done']},
      { label: ['TS ACTIVE']},
      { label: ['max_cell_vol']}
    ];

    this.StatusItemList = [
      { label: ['radio_rssi']},
      { label: ['radio_packet_loss']},
      { label: ['radio_wrong_crc']},
      { label: ['radio_kbps']},
    ];

    //Η συνάρτηση created καλείται μία φορά αλλά η επικοινωνία λειτουργεί συνέχεια
    socket.on('telemetry_data', (telemetry_data: api_res) => {
      //Εδώ ενημερώνουμε όταν λαμβάνουμε packet από το socket
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        console.error('Invalid JSON string');
        return null;
      }

      this.SideBarListItems = [
        { label: ['R2D'], value: [this.telemetry_data_obj.vcu_r2d_flag] },
        { label: ['precharge_done'], value: [this.telemetry_data_obj.accu_precharge_state] },
        { label: ['TS ACTIVE'], value: [this.telemetry_data_obj.accu_ts_active] },
        { label: ['max_cell_vol'], value: [this.telemetry_data_obj.accu_max_cell_voltage] }
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
  //Στο data το Vue κοιτάει τις αλλαγές σε αυτές τις τιμές και τις ενημερώνει στο website (reactive)
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data, //Object as typeof VehicleTelemetry_data
      SideBarListItems: [] as unknown as variableContainer,
      StatusItemList: [] as unknown as variableContainer,
    }
  }
});

</script>  

<!-- Εδώ ορίζουμε πως το vue object θα φαίνεται στην html -->
<template>
<!--  <v-app class="flex min-h-screen">-->
  <!-- ορίζει το Vue item να μοιάζει με flex box που να παίρνει minimum το height της οθόνης -->
  <div class="flex min-h-screen">
    <!-- τα sidebar(αριστερά)/statusbar(πάνω)/router(κύρια περιοχή) είναι κομμάτια του flexbox και τους βάζουμε τα component μας -->
    <side-bar
      :items="SideBarListItems"
    />

    <StatusBar
      :items="StatusItemList"
    />

    <div class="flex-grow">
    <!-- Το router view αλλάζει αυτό που βλέπουμε ανάλογα με το link που είμαστε. η αντιστοιχία link-view είναι στο router.ts -->
      <router-view/>
    </div>

  </div>
</template>

<style scoped>
/* Add your scoped styles here */
</style>
