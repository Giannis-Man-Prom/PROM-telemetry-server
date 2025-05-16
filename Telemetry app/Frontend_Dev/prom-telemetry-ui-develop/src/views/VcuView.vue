<template>
  <div class="p-35 mb-40 ml-10 mx-2 min-w-full">
    <div class="grid grid-cols-2 gap-x-8 gap-y-4 h-screen">
      
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent} from 'vue';
import {io} from "socket.io-client";
import {VehicleTelemetry_data} from "../types/live_telemetry.ts";

const socket = io(import.meta.env.VITE_SOCKET_URL).connect()


export default defineComponent({
  name: 'VcuView',
  components: {
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

      if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
        this.air_m_supp = this.telemetry_data_obj.accu_air_m_supp;
      }
    });
  },
  data() {
    return {
      telemetry_data_obj: {} as VehicleTelemetry_data,
    }
  }
})

</script>
