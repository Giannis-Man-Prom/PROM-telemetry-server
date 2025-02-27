<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue'
import {io} from "socket.io-client";
import {api_res, event_connection_res} from "../types/socketIO.types.ts"; //"@" instead of ".."
import AccuGeneralComponent from "@/components/AccuGeneralComponent.vue";
import {
  sidebarItems,
  statusItems,
  variableContainer,
  VehicleTelemetry_data
} from "../types/live_telemetry.ts";
import GeneralComponent from "@/components/GeneralComponent.vue";
import SideBar from "@/components/SideBar.vue";
import StatusBar from "@/App.vue";

const socket = io('http://0.0.0.0:8081').connect()


export default defineComponent({
  name: "Dash_LiveTelemetry",
  components: {
    StatusBar,

    AccuGeneralComponent,
    GeneralComponent,
    SideBar
  },
  setup() {
    const showPopup = ref(false);
    //const SideBarListItems = ref<sidebarItems[]>([]);
    const closePopup = () => {
      showPopup.value = false;
    };

    // Close popup when clicking outside of it
    const handleClickOutside = (event: MouseEvent) => {
      const popup = document.querySelector('.popup');
      if (popup && !popup.contains(event.target as Node)) {
        closePopup();
      }
    };

    onMounted(() => {
      document.body.addEventListener('click', handleClickOutside);
    });

    return { showPopup, closePopup };
  },
  data() {

    return {
      AccuContainerItems: [] as variableContainer[],
      VCUContainerItems: [] as variableContainer[],
      PDUContainerItems: [] as variableContainer[],
      LeftInverterContainerItems: [] as variableContainer[],
      RightInverterContainerItems: [] as variableContainer[],
      MotorContainerItems: [] as variableContainer[],
      DVContainerItems: [] as variableContainer[],
      SensorsContainerItems: [] as variableContainer[],
      telemetry_data_obj: {} as VehicleTelemetry_data, //Object as typeof VehicleTelemetry_data
      SideBarListItems: [] as sidebarItems[],
      StatusItemList: [] as statusItems[],
      InverterContainerItems: [] as variableContainer[],
      fake_packet_obj: {} as VehicleTelemetry_data,
      PDU: String,
      VCU: String,
      Left_INV: String,
      Right_INV: String,
      //here, I initialized all container-items-object values inside the first [.....] for every object
      //should sth happen, try THIS FOR A FIX---------------------------------------------
    }
  },
  watch: {
    // telemetry_data_obj: {
    //   handler(newVal) {
    //     this.UpdateContainerItems();
    //   },
    //   deep: true // Watch for nested changes in telemetry_data_obj
    // }
  },
  created() {
    //Listen for 'telemetry_data' event from server

    this.AccuContainerItems = [
      { label: ['over_60v_dclink'], value: [99999] },
      { label: ['air_m_state'], value: [99999] },
      { label: ['air_m_supp'], value: [99999] },
      { label: ['air_p_state'], value: [99999] },
      { label: ['air_p_supp'], value: [99999] },
      { label: ['precharge_state'], value: [99999] },
      { label: ['ts_active'], value: [99999] },
      { label: ['vicor_overtemp'], value: [99999] },
      { label: ['max_cell_temp'], value: [99999] },
      { label: ['min_cell_temp'], value: [99999] },
      { label: ['dcdc_temp'], value: [99999] },
      { label: ['max_humidity'], value: [99999] },
      { label: ['bms_error_code'], value: [99999] },
      { label: ['tsac_error_code'], value: [99999] },
      { label: ['max_soc'], value: [99999] },
      { label: ['min_soc'], value: [99999] },
      { label: ['total_voltage_vs'], value: [99999] },
      { label: ['accu_current'], value: [99999] },
      { label: ['max_cell_voltage'], value: [99999] },
      { label: ['min_cell_voltage'], value: [99999] },
      { label: ['wh_consumed'], value: [99999] },
      { label: ['ah_consumed'], value: [99999] },
      { label: ['error_position'], value: [99999] },
      { label: ['min_cell_voltage_pos'], value: [99999] },
      { label: ['max_cell_voltage_pos'], value: [99999] },
      { label: ['last_bms_error_code'], value: [99999] },
      { label: ['last_tsac_error_code'], value: [99999] },
      { label: ['power'], value: [99999] }
    ]

    this.VCUContainerItems = [
      { label: ['water_temp_in_right'], value: [99999] },
      { label: ['water_temp_out_right'], value: [99999] },
      { label: ['pc_flag'], value: [99999] },
      { label: ['r2d_flag'], value: [99999] },
      { label: ['watchdog_status'], value: [99999] },
      { label: ['bspdState'], value: [99999] },
      { label: ['fan_right'], value: [99999] },
      { label: ['fan_left'], value: [99999] },
      { label: ['pump_right'], value: [99999] },
      { label: ['pump_left'], value: [99999] },
      { label: ['gearbox_ntc_left'], value: [99999] },
      { label: ['apps1'], value: [99999] },
      { label: ['apps2'], value: [99999] },
      { label: ['brake_front'], value: [99999] },
      { label: ['brake_rear'], value: [99999] },
      { label: ['hall_fr'], value: [99999] },
      { label: ['hall_fl'], value: [99999] },
      { label: ['apps_right_implausibility'], value: [99999] },
      { label: ['apps_left_implausibility'], value: [99999] },
      { label: ['apps_deviation'], value: [99999] },
      { label: ['as_ready_delay_passed'], value: [99999] },
      { label: ['maxon_brake_enable'], value: [99999] },
      { label: ['res_k3_switch'], value: [99999] },
      { label: ['res_k2_switch'], value: [99999] },
      { label: ['res_estop'], value: [99999] },
      { label: ['res_radio_quality'], value: [99999] },
      { label: ['GE_right_dutyCycle'], value: [99999] },
      { label: ['GE_left_dutyCycle'], value: [99999] },
      { label: ['initial_check_state'], value: [99999] },
      { label: ['as_status'], value: [99999] },
      { label: ['dv_status'], value: [99999] },
      { label: ['node_status', 'clock', 'inverence', 'velocity_estimation', 'slam', 'path_planning', 'controls', 'camera_right', 'camera_left'], value: [99999] },
      { label: ['gearbox_ntc_right'], value: [99999] },
      { label: ['water_temp_in_left'], value: [99999] },
      { label: ['water_temp_out_left'], value: [99999] }
    ]

    socket.on('telemetry_data', (telemetry_data: api_res) => {
      //Here we are updating the object every time we get a new message from the socket,

      //TODO - FIXXXX
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

      this.AccuContainerItems = [
        { label: ['over_60v_dclink'], value: [this.telemetry_data_obj?.accu_over_60v_dclink] },
        { label: ['air_m_state'], value: [this.telemetry_data_obj?.accu_air_m_state] },
        { label: ['air_m_supp'], value: [this.telemetry_data_obj?.accu_air_m_supp] },
        { label: ['air_p_state'], value: [this.telemetry_data_obj?.accu_air_p_state] },
        { label: ['air_p_supp'], value: [this.telemetry_data_obj?.accu_air_p_supp] },
        { label: ['precharge_state'], value: [this.telemetry_data_obj?.accu_precharge_state] },
        { label: ['ts_active'], value: [this.telemetry_data_obj?.accu_ts_active] },
        { label: ['vicor_overtemp'], value: [this.telemetry_data_obj?.accu_vicor_overtemp] },
        { label: ['max_cell_temp'], value: [this.telemetry_data_obj?.accu_max_cell_temp] },
        { label: ['min_cell_temp'], value: [this.telemetry_data_obj?.accu_min_cell_temp] },
        { label: ['dcdc_temp'], value: [this.telemetry_data_obj?.accu_dcdc_temp] },
        { label: ['max_humidity'], value: [this.telemetry_data_obj?.accu_max_humidity] },
        { label: ['bms_error_code'], value: [this.telemetry_data_obj?.accu_bms_error_code] },
        { label: ['tsac_error_code'], value: [this.telemetry_data_obj?.accu_tsac_error_code] },
        { label: ['max_soc'], value: [this.telemetry_data_obj?.accu_max_soc] },
        { label: ['min_soc'], value: [this.telemetry_data_obj?.accu_min_soc] },
        { label: ['total_voltage_vs'], value: [this.telemetry_data_obj?.accu_total_voltage_vs] },
        { label: ['accu_current'], value: [this.telemetry_data_obj?.accu_accu_current] },
        { label: ['max_cell_voltage'], value: [this.telemetry_data_obj?.accu_max_cell_voltage] },
        { label: ['min_cell_voltage'], value: [this.telemetry_data_obj?.accu_min_cell_voltage] },
        { label: ['wh_consumed'], value: [this.telemetry_data_obj?.accu_wh_consumed] },
        { label: ['ah_consumed'], value: [this.telemetry_data_obj?.accu_ah_consumed] },
        { label: ['error_position'], value: [this.telemetry_data_obj?.accu_error_position] },
        { label: ['min_cell_voltage_pos'], value: [this.telemetry_data_obj?.accu_min_cell_voltage_pos] },
        { label: ['max_cell_voltage_pos'], value: [this.telemetry_data_obj?.accu_max_cell_voltage_pos] },
        { label: ['last_bms_error_code'], value: [this.telemetry_data_obj?.accu_last_bms_error_code] },
        { label: ['last_tsac_error_code'], value: [this.telemetry_data_obj?.accu_last_tsac_error_code] },
        { label: ['power'], value: [this.telemetry_data_obj?.accu_power] }
      ]

      this.VCUContainerItems = [
        { label: ['water_temp_in_right'], value: [this.telemetry_data_obj?.accu_over_60v_dclink] },
        { label: ['water_temp_out_right'], value: [this.telemetry_data_obj?.vcu_water_temp_out_right] },
        { label: ['pc_flag'], value: [this.telemetry_data_obj?.vcu_pc_flag] },
        { label: ['r2d_flag'], value: [this.telemetry_data_obj?.vcu_r2d_flag] },
        { label: ['watchdog_status'], value: [this.telemetry_data_obj?.vcu_watchdog_status] },
        { label: ['bspdState'], value: [this.telemetry_data_obj?.vcu_bspdState] },
        { label: ['fan_right'], value: [this.telemetry_data_obj?.vcu_fan_right] },
        { label: ['fan_left'], value: [this.telemetry_data_obj?.vcu_fan_left] },
        { label: ['pump_right'], value: [this.telemetry_data_obj?.vcu_pump_right] },
        { label: ['pump_left'], value: [this.telemetry_data_obj?.vcu_pump_left] },
        { label: ['gearbox_ntc_left'], value: [this.telemetry_data_obj?.vcu_gearbox_ntc_left] },
        { label: ['apps1'], value: [this.telemetry_data_obj?.vcu_apps1] },
        { label: ['apps2'], value: [this.telemetry_data_obj?.vcu_apps2] },
        { label: ['brake_front'], value: [this.telemetry_data_obj?.vcu_brake_front] },
        { label: ['brake_rear'], value: [this.telemetry_data_obj?.vcu_brake_rear] },
        { label: ['hall_fr'], value: [this.telemetry_data_obj?.vcu_hall_fr] },
        { label: ['hall_fl'], value: [this.telemetry_data_obj?.vcu_hall_fl] },
        { label: ['apps_right_implausibility'], value: [this.telemetry_data_obj?.vcu_apps_right_implausibility] },
        { label: ['apps_left_implausibility'], value: [this.telemetry_data_obj?.vcu_apps_left_implausibility] },
        { label: ['apps_deviation'], value: [this.telemetry_data_obj?.vcu_apps_deviation] },
        { label: ['as_ready_delay_passed'], value: [this.telemetry_data_obj?.vcu_as_ready_delay_passed] },
        { label: ['maxon_brake_enable'], value: [this.telemetry_data_obj?.vcu_maxon_brake_enable] },
        { label: ['res_k3_switch'], value: [this.telemetry_data_obj?.vcu_res_k3_switch] },
        { label: ['res_k2_switch'], value: [this.telemetry_data_obj?.vcu_res_k2_switch] },
        { label: ['res_estop'], value: [this.telemetry_data_obj?.vcu_res_estop] },
        { label: ['res_radio_quality'], value: [this.telemetry_data_obj?.vcu_res_radio_quality] },
        { label: ['GE_right_dutyCycle'], value: [this.telemetry_data_obj?.vcu_GE_right_dutyCycle] },
        { label: ['GE_left_dutyCycle'], value: [this.telemetry_data_obj?.vcu_GE_left_dutyCycle] },
        { label: ['initial_check_state'], value: [this.telemetry_data_obj?.vcu_initial_check_state] },
        { label: ['as_status'], value: [this.telemetry_data_obj?.vcu_as_status] },
        { label: ['dv_status'], value: [this.telemetry_data_obj?.vcu_dv_status] },
        { label: ['node_status', 'clock', 'inverence', 'velocity_estimation', 'slam', 'path_planning', 'controls', 'camera_right', 'camera_left' ], value: [this.telemetry_data_obj?.vcu_node_status] },
        { label: ['gearbox_ntc_right'], value: [this.telemetry_data_obj?.vcu_gearbox_ntc_right] },
        { label: ['water_temp_in_left'], value: [this.telemetry_data_obj?.vcu_water_temp_in_left] },
        { label: ['water_temp_out_left'], value: [this.telemetry_data_obj?.vcu_water_temp_out_left] }
      ]

    })

    // Listen for event transmitting the connection status.
    socket.on('connection_response', (message: event_connection_res) => {
      console.log("Connection Status: " + message.status)
    })


  },
  methods: {

    resetContainerItems() {
      this.AccuContainerItems.forEach(item => {
        item.value = [78345348];
      });
      this.VCUContainerItems.forEach(item => {
        item.value = [78345348];
      });
      this.PDUContainerItems.forEach(item => {
        item.value = [78345348];
      });
      this.LeftInverterContainerItems.forEach(item => {
        item.value = [78345348];
      });
      this.RightInverterContainerItems.forEach(item => {
        item.value = [78345348];
      });
    }

  },
  computed: {
    // // Add computed property to return SideBarListItems

  },
  props: {
  }
})
</script>
<!-- in the numrows remember to always include the header, in your calculations!!!!!!!!!!!!!!-->




<template>
  <!-- Main content -->
  <div class="p-0 mx-0 ml-40 mt-20 min-w-full overflow-y-auto"> <!-- ml==40 because max-w of side bar == 40 AND mt==20 bc statusbar height==3 -->
    <div class="grid grid-rows-20 grid-cols-12 gap-5">
      <!--      <div class="p-0 mx-0 min-w-full min-h-full overflow-y-auto mt-20 ml-40">  Add overflow-y-auto to enable vertical scrolling -->
      <!--      <div class="grid grid-rows-20 grid-cols-12 gap-5"> &lt;!&ndash; Remove h-screen from here &ndash;&gt;&ndash;&gt;-->
      <!-- Components -->



      <AccuGeneralComponent
          :items="AccuContainerItems"
          :numRows="7"
          :numCols="5"
          class="ml-5 row-span-3 col-span-5 row-start-1 col-start-1"
      />

      <GeneralComponent
          :items="VCUContainerItems"
          :numRows="5"
          :numCols="5"
          containername="VCU"
          class=" row-span-3 col-span-5 row-start-1"
      />
    </div>
  </div>
</template>

<style scoped>
/* Adjust sidebar width and other styles as needed */



</style>
