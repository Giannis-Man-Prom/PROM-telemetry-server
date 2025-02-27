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
const socket = io(import.meta.env.VITE_SOCKET_URL).connect()

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
    }
  },
  watch: {

  },
  created() {
    //Listen for 'telemetry_data' event from server

    this.AccuContainerItems = [
      { label: ['over_60v_dclink'] },
      { label: ['air_m_state'] },
      { label: ['air_m_supp'] },
      { label: ['air_p_state'] },
      { label: ['air_p_supp'] },
      { label: ['precharge_state'] },
      { label: ['ts_active'] },
      { label: ['vicor_overtemp'] },
      { label: ['max_cell_temp'] },
      { label: ['min_cell_temp'] },
      { label: ['dcdc_temp'] },
      { label: ['max_humidity'] },
      { label: ['bms_error_code'] },
      { label: ['tsac_error_code'] },
      { label: ['max_soc'] },
      { label: ['min_soc'] },
      { label: ['total_voltage_vs'] },
      { label: ['accu_current'] },
      { label: ['max_cell_voltage'] },
      { label: ['min_cell_voltage'] },
      { label: ['wh_consumed'] },
      { label: ['ah_consumed'] },
      { label: ['error_position'] },
      { label: ['min_cell_voltage_pos'] },
      { label: ['max_cell_voltage_pos'] },
      { label: ['last_bms_error_code'] },
      { label: ['last_tsac_error_code'] },
      { label: ['power'] }
    ];

    this.VCUContainerItems = [
      { label: ['water_temp_in_right'] },
      { label: ['water_temp_out_right'] },
      { label: ['pc_flag'] },
      { label: ['r2d_flag'] },
      { label: ['watchdog_status'] },
      { label: ['bspdState'] },
      { label: ['fan_right'] },
      { label: ['fan_left'] },
      { label: ['pump_right'] },
      { label: ['pump_left'] },
      { label: ['gearbox_ntc_left'] },
      { label: ['apps1'] },
      { label: ['apps2'] },
      { label: ['brake_front'] },
      { label: ['brake_rear'] },
      { label: ['hall_fr'] },
      { label: ['hall_fl'] },
      { label: ['apps_right_implausibility'] },
      { label: ['apps_left_implausibility'] },
      { label: ['apps_deviation'] },
      { label: ['as_ready_delay_passed'] },
      { label: ['maxon_brake_enable'] },
      { label: ['res_k3_switch'] },
      { label: ['res_k2_switch'] },
      { label: ['res_estop'] },
      { label: ['res_radio_quality'] },
      { label: ['GE_right_dutyCycle'] },
      { label: ['GE_left_dutyCycle'] },
      { label: ['initial_check_state'] },
      { label: ['as_status'] },
      { label: ['dv_status'] },
      { label: ['node_status', 'clock', 'inverence', 'velocity_estimation', 'slam', 'path_planning', 'controls', 'camera_right', 'camera_left'] },
      { label: ['gearbox_ntc_right'] },
      { label: ['water_temp_in_left'] },
      { label: ['water_temp_out_left'] }
    ];

    this.RightInverterContainerItems = [
      { label: ['critical_hw_status'] },
      { label: ['last_error'] },
      { label: ['can_state'] },
      { label: ['sys_status'] },
      { label: ['handler_status'] },
      { label: ['latched_error'] },
      { label: ['actual_inverter_status'] },
      { label: ['actual_control_mode'] },
      { label: ['aux_hw_status'] },
      { label: ['id_ref'] },
      { label: ['iq_ref'] },
      { label: ['id'] },
      { label: ['iq'] },
      { label: ['iq_ref_request'] },
      { label: ['vdc_max'] },
      { label: ['vdc'] },
      { label: ['i1max'] },
      { label: ['i2max'] },
      { label: ['i3max'] },
      { label: ['Imax'] },
      { label: ['Imin'] },
      { label: ['trq_ref'] },
      { label: ['pwr_ref'] },
      { label: ['pwr_actual'] },
      { label: ['speed_limiter'] },
      { label: ['power_limiter'] },
      { label: ['stall_limiter'] },
      { label: ['l2t_limiter'] },
      { label: ['motor_temp'] },
      { label: ['igbt_temp'] },
      { label: ['motor_rpm'] },
      { label: ['num_max_trq'] },
      { label: ['vcu_max_velocity'] },
      { label: ['trq_actual'] },
      { label: ['max_velocity'] },
      { label: ['min_velocity'] },
      { label: ['distance'] }
    ];

    this.LeftInverterContainerItems = [
      { label: ['critical_hw_status'] },
      { label: ['last_error'] },
      { label: ['can_state'] },
      { label: ['sys_status'] },
      { label: ['handler_status'] },
      { label: ['latched_error'] },
      { label: ['actual_inverter_status'] },
      { label: ['actual_control_mode'] },
      { label: ['aux_hw_status'] },
      { label: ['id_ref'] },
      { label: ['iq_ref'] },
      { label: ['id'] },
      { label: ['iq'] },
      { label: ['iq_ref_request'] },
      { label: ['Vdc_max'] },
      { label: ['Dtorque'] },
      { label: ['Vdc'] },
      { label: ['i1max'] },
      { label: ['i2max'] },
      { label: ['i3max'] },
      { label: ['Imax'] },
      { label: ['Imin'] },
      { label: ['trq_ref'] },
      { label: ['pwr_ref'] },
      { label: ['pwr_actual'] },
      { label: ['speed_limiter'] },
      { label: ['power_limiter'] },
      { label: ['stall_limiter'] },
      { label: ['l2t_limiter'] },
      { label: ['motor_temp'] },
      { label: ['igbt_temp'] },
      { label: ['motor_rpm'] },
      { label: ['num_max_trq'] },
      { label: ['vcu_max_velocity'] },
      { label: ['trq_actual'] },
      { label: ['max_velocity'] },
      { label: ['min_velocity'] },
      { label: ['distance'] }
    ];

    this.SensorsContainerItems = [
      { label: ['fr_channel1'] },
      { label: ['fr_channel2'] },
      { label: ['fr_channel3'] },
      { label: ['fr_channel4'] },
      { label: ['fl_avg'] },
      { label: ['fl_channel1'] },
      { label: ['fl_channel2'] },
      { label: ['fl_channel3'] },
      { label: ['fl_channel4'] },
      { label: ['rr_avg'] },
      { label: ['rr_channel1'] },
      { label: ['rr_channel2'] },
      { label: ['rr_channel3'] },
      { label: ['rr_channel4'] },
      { label: ['rl_avg'] },
      { label: ['rl_channel1'] },
      { label: ['rl_channel2'] },
      { label: ['rl_channel3'] },
      { label: ['rl_channel4'] },
      { label: ['rol'] },
      { label: ['heave'] },
      { label: ['rl'] },
      { label: ['rr'] },
      { label: ['pressure'] },
      { label: ['speed'] },
      { label: ['temp'] },
      { label: ['fr_press'] },
      { label: ['fr_temp'] },
      { label: ['fl_press'] },
      { label: ['fl_temp'] },
      { label: ['rr_press'] },
      { label: ['rr_temp'] },
      { label: ['rl_press'] },
      { label: ['rl_temp'] },
      { label: ['accel_long'] },
      { label: ['accel_lat'] },
      { label: ['gps_speed'] },
      { label: ['front'] },
      { label: ['rear'] },
      { label: ['apps1'] },
      { label: ['apps2'] },
      { label: ['fr'] },
      { label: ['fl'] },
      { label: ['rr'] },
      { label: ['rl'] },
      { label: ['requested_torque'] },
      { label: ['actual_torque'] },
      { label: ['motor_rpm'] },
      { label: ['motor_temp_too_high'] },
      { label: ['motor_temp_limit_reached'] },
      { label: ['motor_temp'] }
    ];

    this.MotorContainerItems = [
      { label: ['requested_torque'] },
      { label: ['actual_torque'] },
      { label: ['motor_rpm'] },
      { label: ['motor_temp_too_high'] },
      { label: ['motor_temp_limit_reached'] },
      { label: ['motor_temp'] }
    ];

    this.PDUContainerItems = [
      { label: ['bms_state'] },
      { label: ['bms_last_error'] },
      { label: ['pdu_state'] },
      { label: ['pdu_last_error'] },
      { label: ['position_of_error'] },
      { label: ['TDK1_temp'] },
      { label: ['TDK2_temp'] },
      { label: ['max_humidity'] },
      { label: ['max_temperature'] },
      { label: ['enable_tdk1'] },
      { label: ['enable_tdk2'] },
      { label: ['precharge_enabled'] },
      { label: ['ams_error'] },
      { label: ['tdkLV_overtemp'] },
      { label: ['tdkTS_overtemp'] },
      { label: ['tdkLV_overcurrent'] },
      { label: ['tdkTS_overcurrent'] },
      { label: ['pdu_error'] },
      { label: ['DAC1'] },
      { label: ['DAC2'] },
      { label: ['max_cell_temp'] },
      { label: ['max_cell_temp_pos'] },
      { label: ['min_cell_temp'] },
      { label: ['min_cell_tep_pos'] },
      { label: ['avg_cell_temp'] },
      { label: ['max_cell_voltage'] },
      { label: ['max_cell_voltage_pos'] },
      { label: ['min_cell_voltage'] },
      { label: ['min_cell_voltage_pos'] },
      { label: ['min_SoC'] },
      { label: ['max_Soc'] },
      { label: ['current_sense1'] },
      { label: ['current_sense2'] }
    ];






    socket.on('telemetry_data', (telemetry_data: api_res) => {
      //Here we are updating the object every time we get a new message from the socket,

      //TODO - FIXXXX
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

      /////////////        ACCU    /////////////////////////////////////////////////////////////////////////////////

      if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
        this.AccuContainerItems[0].value = [this.telemetry_data_obj.accu_over_60v_dclink];
      }
      if (this.telemetry_data_obj.accu_air_m_state !== undefined) {
        this.AccuContainerItems[1].value = [this.telemetry_data_obj.accu_air_m_state];
      }
      if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
        this.AccuContainerItems[2].value = [this.telemetry_data_obj.accu_air_m_supp];
      }
      if (this.telemetry_data_obj.accu_air_p_state !== undefined) {
        this.AccuContainerItems[3].value = [this.telemetry_data_obj.accu_air_p_state];
      }
      if (this.telemetry_data_obj.accu_air_p_supp !== undefined) {
        this.AccuContainerItems[4].value = [this.telemetry_data_obj.accu_air_p_supp];
      }
      if (this.telemetry_data_obj.accu_precharge_state !== undefined) {
        this.AccuContainerItems[5].value = [this.telemetry_data_obj.accu_precharge_state];
      }
      if (this.telemetry_data_obj.accu_ts_active !== undefined) {
        this.AccuContainerItems[6].value = [this.telemetry_data_obj.accu_ts_active];
      }
      if (this.telemetry_data_obj.accu_vicor_overtemp !== undefined) {
        this.AccuContainerItems[7].value = [this.telemetry_data_obj.accu_vicor_overtemp];
      }
      if (this.telemetry_data_obj.accu_max_cell_temp !== undefined) {
        this.AccuContainerItems[8].value = [this.telemetry_data_obj.accu_max_cell_temp];
      }
      if (this.telemetry_data_obj.accu_min_cell_temp !== undefined) {
        this.AccuContainerItems[9].value = [this.telemetry_data_obj.accu_min_cell_temp];
      }
      if (this.telemetry_data_obj.accu_dcdc_temp !== undefined) {
        this.AccuContainerItems[10].value = [this.telemetry_data_obj.accu_dcdc_temp];
      }
      if (this.telemetry_data_obj.accu_max_humidity !== undefined) {
        this.AccuContainerItems[11].value = [this.telemetry_data_obj.accu_max_humidity];
      }
      if (this.telemetry_data_obj.accu_bms_error_code !== undefined) {
        this.AccuContainerItems[12].value = [this.telemetry_data_obj.accu_bms_error_code];
      }
      if (this.telemetry_data_obj.accu_tsac_error_code !== undefined) {
        this.AccuContainerItems[13].value = [this.telemetry_data_obj.accu_tsac_error_code];
      }
      if (this.telemetry_data_obj.accu_max_soc !== undefined) {
        this.AccuContainerItems[14].value = [this.telemetry_data_obj.accu_max_soc];
      }
      if (this.telemetry_data_obj.accu_min_soc !== undefined) {
        this.AccuContainerItems[15].value = [this.telemetry_data_obj.accu_min_soc];
      }
      if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
        this.AccuContainerItems[16].value = [this.telemetry_data_obj.accu_total_voltage_vs];
      }
      if (this.telemetry_data_obj.accu_accu_current !== undefined) {
        this.AccuContainerItems[17].value = [this.telemetry_data_obj.accu_accu_current];
      }
      if (this.telemetry_data_obj.accu_max_cell_voltage !== undefined) {
        this.AccuContainerItems[18].value = [this.telemetry_data_obj.accu_max_cell_voltage];
      }
      if (this.telemetry_data_obj.accu_min_cell_voltage !== undefined) {
        this.AccuContainerItems[19].value = [this.telemetry_data_obj.accu_min_cell_voltage];
      }
      if (this.telemetry_data_obj.accu_wh_consumed !== undefined) {
        this.AccuContainerItems[20].value = [this.telemetry_data_obj.accu_wh_consumed];
      }
      if (this.telemetry_data_obj.accu_ah_consumed !== undefined) {
        this.AccuContainerItems[21].value = [this.telemetry_data_obj.accu_ah_consumed];
      }
      if (this.telemetry_data_obj.accu_error_position !== undefined) {
        this.AccuContainerItems[22].value = [this.telemetry_data_obj.accu_error_position];
      }
      if (this.telemetry_data_obj.accu_min_cell_voltage_pos !== undefined) {
        this.AccuContainerItems[23].value = [this.telemetry_data_obj.accu_min_cell_voltage_pos];
      }
      if (this.telemetry_data_obj.accu_max_cell_voltage_pos !== undefined) {
        this.AccuContainerItems[24].value = [this.telemetry_data_obj.accu_max_cell_voltage_pos];
      }
      if (this.telemetry_data_obj.accu_last_bms_error_code !== undefined) {
        this.AccuContainerItems[25].value = [this.telemetry_data_obj.accu_last_bms_error_code];
      }
      if (this.telemetry_data_obj.accu_last_tsac_error_code !== undefined) {
        this.AccuContainerItems[26].value = [this.telemetry_data_obj.accu_last_tsac_error_code];
      }
      if (this.telemetry_data_obj.accu_power !== undefined) {
        this.AccuContainerItems[27].value = [this.telemetry_data_obj.accu_power];
      }



      /////////////            VCU            /////////////////////////////////////////////////////////////////////////////////////////////




      if (this.telemetry_data_obj.vcu_water_temp_in_right !== undefined) {
        this.VCUContainerItems[0].value = [this.telemetry_data_obj.vcu_water_temp_in_right];
      }
      if (this.telemetry_data_obj.vcu_water_temp_out_right !== undefined) {
        this.VCUContainerItems[1].value = [this.telemetry_data_obj.vcu_water_temp_out_right];
      }
      if (this.telemetry_data_obj.vcu_pc_flag !== undefined) {
        this.VCUContainerItems[2].value = [this.telemetry_data_obj.vcu_pc_flag];
      }
      if (this.telemetry_data_obj.vcu_r2d_flag !== undefined) {
        this.VCUContainerItems[3].value = [this.telemetry_data_obj.vcu_r2d_flag];
      }
      if (this.telemetry_data_obj.vcu_watchdog_status !== undefined) {
        this.VCUContainerItems[4].value = [this.telemetry_data_obj.vcu_watchdog_status];
      }
      if (this.telemetry_data_obj.vcu_bspdState !== undefined) {
        this.VCUContainerItems[5].value = [this.telemetry_data_obj.vcu_bspdState];
      }
      if (this.telemetry_data_obj.vcu_fan_right !== undefined) {
        this.VCUContainerItems[6].value = [this.telemetry_data_obj.vcu_fan_right];
      }
      if (this.telemetry_data_obj.vcu_fan_left !== undefined) {
        this.VCUContainerItems[7].value = [this.telemetry_data_obj.vcu_fan_left];
      }
      if (this.telemetry_data_obj.vcu_pump_right !== undefined) {
        this.VCUContainerItems[8].value = [this.telemetry_data_obj.vcu_pump_right];
      }
      if (this.telemetry_data_obj.vcu_pump_left !== undefined) {
        this.VCUContainerItems[9].value = [this.telemetry_data_obj.vcu_pump_left];
      }
      if (this.telemetry_data_obj.vcu_gearbox_ntc_left !== undefined) {
        this.VCUContainerItems[10].value = [this.telemetry_data_obj.vcu_gearbox_ntc_left];
      }
      if (this.telemetry_data_obj.vcu_apps1 !== undefined) {
        this.VCUContainerItems[11].value = [this.telemetry_data_obj.vcu_apps1];
      }
      if (this.telemetry_data_obj.vcu_apps2 !== undefined) {
        this.VCUContainerItems[12].value = [this.telemetry_data_obj.vcu_apps2];
      }
      if (this.telemetry_data_obj.vcu_brake_front !== undefined) {
        this.VCUContainerItems[13].value = [this.telemetry_data_obj.vcu_brake_front];
      }
      if (this.telemetry_data_obj.vcu_brake_rear !== undefined) {
        this.VCUContainerItems[14].value = [this.telemetry_data_obj.vcu_brake_rear];
      }
      if (this.telemetry_data_obj.vcu_hall_fr !== undefined) {
        this.VCUContainerItems[15].value = [this.telemetry_data_obj.vcu_hall_fr];
      }
      if (this.telemetry_data_obj.vcu_hall_fl !== undefined) {
        this.VCUContainerItems[16].value = [this.telemetry_data_obj.vcu_hall_fl];
      }
      if (this.telemetry_data_obj.vcu_apps_right_implausibility !== undefined) {
        this.VCUContainerItems[17].value = [this.telemetry_data_obj.vcu_apps_right_implausibility];
      }
      if (this.telemetry_data_obj.vcu_apps_left_implausibility !== undefined) {
        this.VCUContainerItems[18].value = [this.telemetry_data_obj.vcu_apps_left_implausibility];
      }
      if (this.telemetry_data_obj.vcu_apps_deviation !== undefined) {
        this.VCUContainerItems[19].value = [this.telemetry_data_obj.vcu_apps_deviation];
      }
      if (this.telemetry_data_obj.vcu_as_ready_delay_passed !== undefined) {
        this.VCUContainerItems[20].value = [this.telemetry_data_obj.vcu_as_ready_delay_passed];
      }
      if (this.telemetry_data_obj.vcu_maxon_brake_enable !== undefined) {
        this.VCUContainerItems[21].value = [this.telemetry_data_obj.vcu_maxon_brake_enable];
      }
      if (this.telemetry_data_obj.vcu_res_k3_switch !== undefined) {
        this.VCUContainerItems[22].value = [this.telemetry_data_obj.vcu_res_k3_switch];
      }
      if (this.telemetry_data_obj.vcu_res_k2_switch !== undefined) {
        this.VCUContainerItems[23].value = [this.telemetry_data_obj.vcu_res_k2_switch];
      }
      if (this.telemetry_data_obj.vcu_res_estop !== undefined) {
        this.VCUContainerItems[24].value = [this.telemetry_data_obj.vcu_res_estop];
      }
      if (this.telemetry_data_obj.vcu_res_radio_quality !== undefined) {
        this.VCUContainerItems[25].value = [this.telemetry_data_obj.vcu_res_radio_quality];
      }
      if (this.telemetry_data_obj.vcu_GE_right_dutyCycle !== undefined) {
        this.VCUContainerItems[26].value = [this.telemetry_data_obj.vcu_GE_right_dutyCycle];
      }
      if (this.telemetry_data_obj.vcu_GE_left_dutyCycle !== undefined) {
        this.VCUContainerItems[27].value = [this.telemetry_data_obj.vcu_GE_left_dutyCycle];
      }
      if (this.telemetry_data_obj.vcu_initial_check_state !== undefined) {
        this.VCUContainerItems[28].value = [this.telemetry_data_obj.vcu_initial_check_state];
      }
      if (this.telemetry_data_obj.vcu_as_status !== undefined) {
        this.VCUContainerItems[29].value = [this.telemetry_data_obj.vcu_as_status];
      }
      if (this.telemetry_data_obj.vcu_dv_status !== undefined) {
        this.VCUContainerItems[30].value = [this.telemetry_data_obj.vcu_dv_status];
      }
      if (this.telemetry_data_obj.vcu_node_status !== undefined) {
        this.VCUContainerItems[31].value = [this.telemetry_data_obj.vcu_node_status];
      }
      if (this.telemetry_data_obj.vcu_gearbox_ntc_right !== undefined) {
        this.VCUContainerItems[32].value = [this.telemetry_data_obj.vcu_gearbox_ntc_right];
      }
      if (this.telemetry_data_obj.vcu_water_temp_in_left !== undefined) {
        this.VCUContainerItems[33].value = [this.telemetry_data_obj.vcu_water_temp_in_left];
      }
      if (this.telemetry_data_obj.vcu_water_temp_out_left !== undefined) {
        this.VCUContainerItems[34].value = [this.telemetry_data_obj.vcu_water_temp_out_left];
      }


/////////////////////      RIGHT INV     ////////////////////////////////////////////////////////////////////////////////////



      if (this.telemetry_data_obj.right_inv_critical_hw_status !== undefined) {
        this.RightInverterContainerItems[0].value = [this.telemetry_data_obj.right_inv_critical_hw_status];
      }
      if (this.telemetry_data_obj.right_inv_last_error !== undefined) {
        this.RightInverterContainerItems[1].value = [this.telemetry_data_obj.right_inv_last_error];
      }
      if (this.telemetry_data_obj.right_inv_can_state !== undefined) {
        this.RightInverterContainerItems[2].value = [this.telemetry_data_obj.right_inv_can_state];
      }
      if (this.telemetry_data_obj.right_inv_sys_status !== undefined) {
        this.RightInverterContainerItems[3].value = [this.telemetry_data_obj.right_inv_sys_status];
      }
      if (this.telemetry_data_obj.right_inv_handler_status !== undefined) {
        this.RightInverterContainerItems[4].value = [this.telemetry_data_obj.right_inv_handler_status];
      }
      if (this.telemetry_data_obj.right_inv_latched_error !== undefined) {
        this.RightInverterContainerItems[5].value = [this.telemetry_data_obj.right_inv_latched_error];
      }
      if (this.telemetry_data_obj.right_inv_actual_inverter_status !== undefined) {
        this.RightInverterContainerItems[6].value = [this.telemetry_data_obj.right_inv_actual_inverter_status];
      }
      if (this.telemetry_data_obj.right_inv_actual_control_mode !== undefined) {
        this.RightInverterContainerItems[7].value = [this.telemetry_data_obj.right_inv_actual_control_mode];
      }
      if (this.telemetry_data_obj.right_inv_aux_hw_status !== undefined) {
        this.RightInverterContainerItems[8].value = [this.telemetry_data_obj.right_inv_aux_hw_status];
      }
      if (this.telemetry_data_obj.right_inv_id_ref !== undefined) {
        this.RightInverterContainerItems[9].value = [this.telemetry_data_obj.right_inv_id_ref];
      }
      if (this.telemetry_data_obj.right_inv_iq_ref !== undefined) {
        this.RightInverterContainerItems[10].value = [this.telemetry_data_obj.right_inv_iq_ref];
      }
      if (this.telemetry_data_obj.right_inv_id !== undefined) {
        this.RightInverterContainerItems[11].value = [this.telemetry_data_obj.right_inv_id];
      }
      if (this.telemetry_data_obj.right_inv_iq !== undefined) {
        this.RightInverterContainerItems[12].value = [this.telemetry_data_obj.right_inv_iq];
      }
      if (this.telemetry_data_obj.right_inv_iq_ref_request !== undefined) {
        this.RightInverterContainerItems[13].value = [this.telemetry_data_obj.right_inv_iq_ref_request];
      }
      if (this.telemetry_data_obj.right_inv_vdc_max !== undefined) {
        this.RightInverterContainerItems[14].value = [this.telemetry_data_obj.right_inv_vdc_max];
      }
      if (this.telemetry_data_obj.right_inv_vdc !== undefined) {
        this.RightInverterContainerItems[15].value = [this.telemetry_data_obj.right_inv_vdc];
      }
      if (this.telemetry_data_obj.right_inv_i1max !== undefined) {
        this.RightInverterContainerItems[16].value = [this.telemetry_data_obj.right_inv_i1max];
      }
      if (this.telemetry_data_obj.right_inv_i2max !== undefined) {
        this.RightInverterContainerItems[17].value = [this.telemetry_data_obj.right_inv_i2max];
      }
      if (this.telemetry_data_obj.right_inv_i3max !== undefined) {
        this.RightInverterContainerItems[18].value = [this.telemetry_data_obj.right_inv_i3max];
      }
      if (this.telemetry_data_obj.right_inv_Imax !== undefined) {
        this.RightInverterContainerItems[19].value = [this.telemetry_data_obj.right_inv_Imax];
      }
      if (this.telemetry_data_obj.right_inv_Imin !== undefined) {
        this.RightInverterContainerItems[20].value = [this.telemetry_data_obj.right_inv_Imin];
      }
      if (this.telemetry_data_obj.right_inv_trq_ref !== undefined) {
        this.RightInverterContainerItems[21].value = [this.telemetry_data_obj.right_inv_trq_ref];
      }
      if (this.telemetry_data_obj.right_inv_pwr_ref !== undefined) {
        this.RightInverterContainerItems[22].value = [this.telemetry_data_obj.right_inv_pwr_ref];
      }
      if (this.telemetry_data_obj.right_inv_pwr_actual !== undefined) {
        this.RightInverterContainerItems[23].value = [this.telemetry_data_obj.right_inv_pwr_actual];
      }
      if (this.telemetry_data_obj.right_inv_speed_limiter !== undefined) {
        this.RightInverterContainerItems[24].value = [this.telemetry_data_obj.right_inv_speed_limiter];
      }
      if (this.telemetry_data_obj.right_inv_power_limiter !== undefined) {
        this.RightInverterContainerItems[25].value = [this.telemetry_data_obj.right_inv_power_limiter];
      }
      if (this.telemetry_data_obj.right_inv_stall_limiter !== undefined) {
        this.RightInverterContainerItems[26].value = [this.telemetry_data_obj.right_inv_stall_limiter];
      }
      if (this.telemetry_data_obj.right_inv_l2t_limiter !== undefined) {
        this.RightInverterContainerItems[27].value = [this.telemetry_data_obj.right_inv_l2t_limiter];
      }
      if (this.telemetry_data_obj.right_inv_motor_temp !== undefined) {
        this.RightInverterContainerItems[28].value = [this.telemetry_data_obj.right_inv_motor_temp];
      }
      if (this.telemetry_data_obj.right_inv_igbt_temp !== undefined) {
        this.RightInverterContainerItems[29].value = [this.telemetry_data_obj.right_inv_igbt_temp];
      }
      if (this.telemetry_data_obj.right_inv_motor_rpm !== undefined) {
        this.RightInverterContainerItems[30].value = [this.telemetry_data_obj.right_inv_motor_rpm];
      }
      if (this.telemetry_data_obj.right_inv_num_max_trq !== undefined) {
        this.RightInverterContainerItems[31].value = [this.telemetry_data_obj.right_inv_num_max_trq];
      }
      if (this.telemetry_data_obj.right_inv_vcu_max_velocity !== undefined) {
        this.RightInverterContainerItems[32].value = [this.telemetry_data_obj.right_inv_vcu_max_velocity];
      }
      if (this.telemetry_data_obj.right_inv_trq_actual !== undefined) {
        this.RightInverterContainerItems[33].value = [this.telemetry_data_obj.right_inv_trq_actual];
      }
      if (this.telemetry_data_obj.right_inv_max_velocity !== undefined) {
        this.RightInverterContainerItems[34].value = [this.telemetry_data_obj.right_inv_max_velocity];
      }
      if (this.telemetry_data_obj.right_inv_min_velocity !== undefined) {
        this.RightInverterContainerItems[35].value = [this.telemetry_data_obj.right_inv_min_velocity];
      }
      if (this.telemetry_data_obj.right_inv_distance !== undefined) {
        this.RightInverterContainerItems[36].value = [this.telemetry_data_obj.right_inv_distance];
      }




/////////////////////      LEFT INV     ////////////////////////////////////////////////////////////////////////////////////



      if (this.telemetry_data_obj.left_inv_critical_hw_status !== undefined) {
        this.LeftInverterContainerItems[0].value = [this.telemetry_data_obj.left_inv_critical_hw_status];
      }
      if (this.telemetry_data_obj.left_inv_last_error !== undefined) {
        this.LeftInverterContainerItems[1].value = [this.telemetry_data_obj.left_inv_last_error];
      }
      if (this.telemetry_data_obj.left_inv_can_state !== undefined) {
        this.LeftInverterContainerItems[2].value = [this.telemetry_data_obj.left_inv_can_state];
      }
      if (this.telemetry_data_obj.left_inv_sys_status !== undefined) {
        this.LeftInverterContainerItems[3].value = [this.telemetry_data_obj.left_inv_sys_status];
      }
      if (this.telemetry_data_obj.left_inv_handler_status !== undefined) {
        this.LeftInverterContainerItems[4].value = [this.telemetry_data_obj.left_inv_handler_status];
      }
      if (this.telemetry_data_obj.left_inv_latched_error !== undefined) {
        this.LeftInverterContainerItems[5].value = [this.telemetry_data_obj.left_inv_latched_error];
      }
      if (this.telemetry_data_obj.left_inv_actual_inverter_status !== undefined) {
        this.LeftInverterContainerItems[6].value = [this.telemetry_data_obj.left_inv_actual_inverter_status];
      }
      if (this.telemetry_data_obj.left_inv_actual_control_mode !== undefined) {
        this.LeftInverterContainerItems[7].value = [this.telemetry_data_obj.left_inv_actual_control_mode];
      }
      if (this.telemetry_data_obj.left_inv_aux_hw_status !== undefined) {
        this.LeftInverterContainerItems[8].value = [this.telemetry_data_obj.left_inv_aux_hw_status];
      }
      if (this.telemetry_data_obj.left_inv_id_ref !== undefined) {
        this.LeftInverterContainerItems[9].value = [this.telemetry_data_obj.left_inv_id_ref];
      }
      if (this.telemetry_data_obj.left_inv_iq_ref !== undefined) {
        this.LeftInverterContainerItems[10].value = [this.telemetry_data_obj.left_inv_iq_ref];
      }
      if (this.telemetry_data_obj.left_inv_id !== undefined) {
        this.LeftInverterContainerItems[11].value = [this.telemetry_data_obj.left_inv_id];
      }
      if (this.telemetry_data_obj.left_inv_iq !== undefined) {
        this.LeftInverterContainerItems[12].value = [this.telemetry_data_obj.left_inv_iq];
      }
      if (this.telemetry_data_obj.left_inv_iq_ref_request !== undefined) {
        this.LeftInverterContainerItems[13].value = [this.telemetry_data_obj.left_inv_iq_ref_request];
      }
      if (this.telemetry_data_obj.left_inv_vdc_max !== undefined) {
        this.LeftInverterContainerItems[14].value = [this.telemetry_data_obj.left_inv_vdc_max];
      }
      if (this.telemetry_data_obj.left_inv_dtorque !== undefined) {
        this.LeftInverterContainerItems[15].value = [this.telemetry_data_obj.left_inv_dtorque];
      }
      if (this.telemetry_data_obj.left_inv_vdc !== undefined) {
        this.LeftInverterContainerItems[16].value = [this.telemetry_data_obj.left_inv_vdc];
      }
      if (this.telemetry_data_obj.left_inv_i1max !== undefined) {
        this.LeftInverterContainerItems[17].value = [this.telemetry_data_obj.left_inv_i1max];
      }
      if (this.telemetry_data_obj.left_inv_i2max !== undefined) {
        this.LeftInverterContainerItems[18].value = [this.telemetry_data_obj.left_inv_i2max];
      }
      if (this.telemetry_data_obj.left_inv_i3max !== undefined) {
        this.LeftInverterContainerItems[19].value = [this.telemetry_data_obj.left_inv_i3max];
      }
      if (this.telemetry_data_obj.left_inv_Imax !== undefined) {
        this.LeftInverterContainerItems[20].value = [this.telemetry_data_obj.left_inv_Imax];
      }
      if (this.telemetry_data_obj.left_inv_Imin !== undefined) {
        this.LeftInverterContainerItems[21].value = [this.telemetry_data_obj.left_inv_Imin];
      }
      if (this.telemetry_data_obj.left_inv_trq_ref !== undefined) {
        this.LeftInverterContainerItems[22].value = [this.telemetry_data_obj.left_inv_trq_ref];
      }
      if (this.telemetry_data_obj.left_inv_pwr_ref !== undefined) {
        this.LeftInverterContainerItems[23].value = [this.telemetry_data_obj.left_inv_pwr_ref];
      }
      if (this.telemetry_data_obj.left_inv_pwr_actual !== undefined) {
        this.LeftInverterContainerItems[24].value = [this.telemetry_data_obj.left_inv_pwr_actual];
      }
      if (this.telemetry_data_obj.left_inv_speed_limiter !== undefined) {
        this.LeftInverterContainerItems[25].value = [this.telemetry_data_obj.left_inv_speed_limiter];
      }
      if (this.telemetry_data_obj.left_inv_power_limiter !== undefined) {
        this.LeftInverterContainerItems[26].value = [this.telemetry_data_obj.left_inv_power_limiter];
      }
      if (this.telemetry_data_obj.left_inv_stall_limiter !== undefined) {
        this.LeftInverterContainerItems[27].value = [this.telemetry_data_obj.left_inv_stall_limiter];
      }
      if (this.telemetry_data_obj.left_inv_l2t_limiter !== undefined) {
        this.LeftInverterContainerItems[28].value = [this.telemetry_data_obj.left_inv_l2t_limiter];
      }
      if (this.telemetry_data_obj.left_inv_motor_temp !== undefined) {
        this.LeftInverterContainerItems[29].value = [this.telemetry_data_obj.left_inv_motor_temp];
      }
      if (this.telemetry_data_obj.left_inv_igbt_temp !== undefined) {
        this.LeftInverterContainerItems[30].value = [this.telemetry_data_obj.left_inv_igbt_temp];
      }
      if (this.telemetry_data_obj.left_inv_motor_rpm !== undefined) {
        this.LeftInverterContainerItems[31].value = [this.telemetry_data_obj.left_inv_motor_rpm];
      }
      if (this.telemetry_data_obj.left_inv_num_max_trq !== undefined) {
        this.LeftInverterContainerItems[32].value = [this.telemetry_data_obj.left_inv_num_max_trq];
      }
      if (this.telemetry_data_obj.left_inv_vcu_max_velocity !== undefined) {
        this.LeftInverterContainerItems[33].value = [this.telemetry_data_obj.left_inv_vcu_max_velocity];
      }
      if (this.telemetry_data_obj.left_inv_trq_actual !== undefined) {
        this.LeftInverterContainerItems[34].value = [this.telemetry_data_obj.left_inv_trq_actual];
      }
      if (this.telemetry_data_obj.left_inv_max_velocity !== undefined) {
        this.LeftInverterContainerItems[35].value = [this.telemetry_data_obj.left_inv_max_velocity];
      }
      if (this.telemetry_data_obj.left_inv_min_velocity !== undefined) {
        this.LeftInverterContainerItems[36].value = [this.telemetry_data_obj.left_inv_min_velocity];
      }
      if (this.telemetry_data_obj.left_inv_distance !== undefined) {
        this.LeftInverterContainerItems[37].value = [this.telemetry_data_obj.left_inv_distance];
      }






/////////////////////////////////      SENSORS        ///////////////////////////////////////





      if (this.telemetry_data_obj.sensors_fr_channel1 !== undefined) {
        this.SensorsContainerItems[0].value = [this.telemetry_data_obj.sensors_fr_channel1];
      }
      if (this.telemetry_data_obj.sensors_fr_channel2 !== undefined) {
        this.SensorsContainerItems[1].value = [this.telemetry_data_obj.sensors_fr_channel2];
      }
      if (this.telemetry_data_obj.sensors_fr_channel3 !== undefined) {
        this.SensorsContainerItems[2].value = [this.telemetry_data_obj.sensors_fr_channel3];
      }
      if (this.telemetry_data_obj.sensors_fr_channel4 !== undefined) {
        this.SensorsContainerItems[3].value = [this.telemetry_data_obj.sensors_fr_channel4];
      }
      if (this.telemetry_data_obj.sensors_fl_avg !== undefined) {
        this.SensorsContainerItems[4].value = [this.telemetry_data_obj.sensors_fl_avg];
      }
      if (this.telemetry_data_obj.sensors_fl_channel1 !== undefined) {
        this.SensorsContainerItems[5].value = [this.telemetry_data_obj.sensors_fl_channel1];
      }
      if (this.telemetry_data_obj.sensors_fl_channel2 !== undefined) {
        this.SensorsContainerItems[6].value = [this.telemetry_data_obj.sensors_fl_channel2];
      }
      if (this.telemetry_data_obj.sensors_fl_channel3 !== undefined) {
        this.SensorsContainerItems[7].value = [this.telemetry_data_obj.sensors_fl_channel3];
      }
      if (this.telemetry_data_obj.sensors_fl_channel4 !== undefined) {
        this.SensorsContainerItems[8].value = [this.telemetry_data_obj.sensors_fl_channel4];
      }
      if (this.telemetry_data_obj.sensors_rr_avg !== undefined) {
        this.SensorsContainerItems[9].value = [this.telemetry_data_obj.sensors_rr_avg];
      }
      if (this.telemetry_data_obj.sensors_rr_channel1 !== undefined) {
        this.SensorsContainerItems[10].value = [this.telemetry_data_obj.sensors_rr_channel1];
      }
      if (this.telemetry_data_obj.sensors_rr_channel2 !== undefined) {
        this.SensorsContainerItems[11].value = [this.telemetry_data_obj.sensors_rr_channel2];
      }
      if (this.telemetry_data_obj.sensors_rr_channel3 !== undefined) {
        this.SensorsContainerItems[12].value = [this.telemetry_data_obj.sensors_rr_channel3];
      }
      if (this.telemetry_data_obj.sensors_rr_channel4 !== undefined) {
        this.SensorsContainerItems[13].value = [this.telemetry_data_obj.sensors_rr_channel4];
      }
      if (this.telemetry_data_obj.sensors_rl_avg !== undefined) {
        this.SensorsContainerItems[14].value = [this.telemetry_data_obj.sensors_rl_avg];
      }
      if (this.telemetry_data_obj.sensors_rl_channel1 !== undefined) {
        this.SensorsContainerItems[15].value = [this.telemetry_data_obj.sensors_rl_channel1];
      }
      if (this.telemetry_data_obj.sensors_rl_channel2 !== undefined) {
        this.SensorsContainerItems[16].value = [this.telemetry_data_obj.sensors_rl_channel2];
      }
      if (this.telemetry_data_obj.sensors_rl_channel3 !== undefined) {
        this.SensorsContainerItems[17].value = [this.telemetry_data_obj.sensors_rl_channel3];
      }
      if (this.telemetry_data_obj.sensors_rl_channel4 !== undefined) {
        this.SensorsContainerItems[18].value = [this.telemetry_data_obj.sensors_rl_channel4];
      }
      if (this.telemetry_data_obj.sensors_rol !== undefined) {
        this.SensorsContainerItems[19].value = [this.telemetry_data_obj.sensors_rol];
      }
      if (this.telemetry_data_obj.sensors_heave !== undefined) {
        this.SensorsContainerItems[20].value = [this.telemetry_data_obj.sensors_heave];
      }
      if (this.telemetry_data_obj.sensors_rl !== undefined) {
        this.SensorsContainerItems[21].value = [this.telemetry_data_obj.sensors_rl];
      }
      if (this.telemetry_data_obj.sensors_rr !== undefined) {
        this.SensorsContainerItems[22].value = [this.telemetry_data_obj.sensors_rr];
      }
      if (this.telemetry_data_obj.sensors_pressure !== undefined) {
        this.SensorsContainerItems[23].value = [this.telemetry_data_obj.sensors_pressure];
      }
      if (this.telemetry_data_obj.sensors_speed !== undefined) {
        this.SensorsContainerItems[24].value = [this.telemetry_data_obj.sensors_speed];
      }
      if (this.telemetry_data_obj.sensors_temp !== undefined) {
        this.SensorsContainerItems[25].value = [this.telemetry_data_obj.sensors_temp];
      }
      if (this.telemetry_data_obj.sensors_fr_press !== undefined) {
        this.SensorsContainerItems[26].value = [this.telemetry_data_obj.sensors_fr_press];
      }
      if (this.telemetry_data_obj.sensors_fr_temp !== undefined) {
        this.SensorsContainerItems[27].value = [this.telemetry_data_obj.sensors_fr_temp];
      }
      if (this.telemetry_data_obj.sensors_fl_press !== undefined) {
        this.SensorsContainerItems[28].value = [this.telemetry_data_obj.sensors_fl_press];
      }
      if (this.telemetry_data_obj.sensors_fl_temp !== undefined) {
        this.SensorsContainerItems[29].value = [this.telemetry_data_obj.sensors_fl_temp];
      }
      if (this.telemetry_data_obj.sensors_rr_press !== undefined) {
        this.SensorsContainerItems[30].value = [this.telemetry_data_obj.sensors_rr_press];
      }
      if (this.telemetry_data_obj.sensors_rr_temp !== undefined) {
        this.SensorsContainerItems[31].value = [this.telemetry_data_obj.sensors_rr_temp];
      }
      if (this.telemetry_data_obj.sensors_rl_press !== undefined) {
        this.SensorsContainerItems[32].value = [this.telemetry_data_obj.sensors_rl_press];
      }
      if (this.telemetry_data_obj.sensors_rl_temp !== undefined) {
        this.SensorsContainerItems[33].value = [this.telemetry_data_obj.sensors_rl_temp];
      }
      if (this.telemetry_data_obj.sensors_accel_long !== undefined) {
        this.SensorsContainerItems[34].value = [this.telemetry_data_obj.sensors_accel_long];
      }
      if (this.telemetry_data_obj.sensors_accel_lat !== undefined) {
        this.SensorsContainerItems[35].value = [this.telemetry_data_obj.sensors_accel_lat];
      }
      if (this.telemetry_data_obj.sensors_gps_speed !== undefined) {
        this.SensorsContainerItems[36].value = [this.telemetry_data_obj.sensors_gps_speed];
      }
      if (this.telemetry_data_obj.sensors_front !== undefined) {
        this.SensorsContainerItems[37].value = [this.telemetry_data_obj.sensors_front];
      }
      if (this.telemetry_data_obj.sensors_rear !== undefined) {
        this.SensorsContainerItems[38].value = [this.telemetry_data_obj.sensors_rear];
      }
      if (this.telemetry_data_obj.sensors_apps1 !== undefined) {
        this.SensorsContainerItems[39].value = [this.telemetry_data_obj.sensors_apps1];
      }
      if (this.telemetry_data_obj.sensors_apps2 !== undefined) {
        this.SensorsContainerItems[40].value = [this.telemetry_data_obj.sensors_apps2];
      }
      if (this.telemetry_data_obj.sensors_fr !== undefined) {
        this.SensorsContainerItems[41].value = [this.telemetry_data_obj.sensors_fr];
      }
      if (this.telemetry_data_obj.sensors_fl !== undefined) {
        this.SensorsContainerItems[42].value = [this.telemetry_data_obj.sensors_fl];
      }
      if (this.telemetry_data_obj.sensors_rr !== undefined) {
        this.SensorsContainerItems[43].value = [this.telemetry_data_obj.sensors_rr];
      }
      if (this.telemetry_data_obj.sensors_rl !== undefined) {
        this.SensorsContainerItems[44].value = [this.telemetry_data_obj.sensors_rl];
      }
      if (this.telemetry_data_obj.sensors_requested_torque !== undefined) {
        this.SensorsContainerItems[45].value = [this.telemetry_data_obj.sensors_requested_torque];
      }
      if (this.telemetry_data_obj.sensors_actual_torque !== undefined) {
        this.SensorsContainerItems[46].value = [this.telemetry_data_obj.sensors_actual_torque];
      }
      if (this.telemetry_data_obj.sensors_motor_rpm !== undefined) {
        this.SensorsContainerItems[47].value = [this.telemetry_data_obj.sensors_motor_rpm];
      }
      if (this.telemetry_data_obj.sensors_motor_temp_too_high !== undefined) {
        this.SensorsContainerItems[48].value = [this.telemetry_data_obj.sensors_motor_temp_too_high];
      }
      if (this.telemetry_data_obj.sensors_motor_temp_limit_reached !== undefined) {
        this.SensorsContainerItems[49].value = [this.telemetry_data_obj.sensors_motor_temp_limit_reached];
      }
      if (this.telemetry_data_obj.sensors_motor_temp !== undefined) {
        this.SensorsContainerItems[50].value = [this.telemetry_data_obj.sensors_motor_temp];
      }


/////////////////////////////////      PDU        ///////////////////////////////////////////////////////



      if (this.telemetry_data_obj.pdu_bms_state !== undefined) {
        this.PDUContainerItems[0].value = [this.telemetry_data_obj.pdu_bms_state];
      }
      if (this.telemetry_data_obj.pdu_bms_last_error !== undefined) {
        this.PDUContainerItems[1].value = [this.telemetry_data_obj.pdu_bms_last_error];
      }
      if (this.telemetry_data_obj.pdu_pdu_state !== undefined) {
        this.PDUContainerItems[2].value = [this.telemetry_data_obj.pdu_pdu_state];
      }
      if (this.telemetry_data_obj.pdu_pdu_last_error !== undefined) {
        this.PDUContainerItems[3].value = [this.telemetry_data_obj.pdu_pdu_last_error];
      }
      if (this.telemetry_data_obj.pdu_position_of_error !== undefined) {
        this.PDUContainerItems[4].value = [this.telemetry_data_obj.pdu_position_of_error];
      }
      if (this.telemetry_data_obj.pdu_TDK1_temp !== undefined) {
        this.PDUContainerItems[5].value = [this.telemetry_data_obj.pdu_TDK1_temp];
      }
      if (this.telemetry_data_obj.pdu_TDK2_temp !== undefined) {
        this.PDUContainerItems[6].value = [this.telemetry_data_obj.pdu_TDK2_temp];
      }
      if (this.telemetry_data_obj.pdu_max_humidity !== undefined) {
        this.PDUContainerItems[7].value = [this.telemetry_data_obj.pdu_max_humidity];
      }
      if (this.telemetry_data_obj.pdu_max_temperature !== undefined) {
        this.PDUContainerItems[8].value = [this.telemetry_data_obj.pdu_max_temperature];
      }
      if (this.telemetry_data_obj.pdu_enable_tdk1 !== undefined) {
        this.PDUContainerItems[9].value = [this.telemetry_data_obj.pdu_enable_tdk1];
      }
      if (this.telemetry_data_obj.pdu_enable_tdk2 !== undefined) {
        this.PDUContainerItems[10].value = [this.telemetry_data_obj.pdu_enable_tdk2];
      }
      if (this.telemetry_data_obj.pdu_precharge_enabled !== undefined) {
        this.PDUContainerItems[11].value = [this.telemetry_data_obj.pdu_precharge_enabled];
      }
      if (this.telemetry_data_obj.pdu_ams_error !== undefined) {
        this.PDUContainerItems[12].value = [this.telemetry_data_obj.pdu_ams_error];
      }
      if (this.telemetry_data_obj.pdu_tdkLV_overtemp !== undefined) {
        this.PDUContainerItems[13].value = [this.telemetry_data_obj.pdu_tdkLV_overtemp];
      }
      if (this.telemetry_data_obj.pdu_tdkTS_overtemp !== undefined) {
        this.PDUContainerItems[14].value = [this.telemetry_data_obj.pdu_tdkTS_overtemp];
      }
      if (this.telemetry_data_obj.pdu_tdkLV_overcurrent !== undefined) {
        this.PDUContainerItems[15].value = [this.telemetry_data_obj.pdu_tdkLV_overcurrent];
      }
      if (this.telemetry_data_obj.pdu_tdkTS_overcurrent !== undefined) {
        this.PDUContainerItems[16].value = [this.telemetry_data_obj.pdu_tdkTS_overcurrent];
      }
      if (this.telemetry_data_obj.pdu_pdu_error !== undefined) {
        this.PDUContainerItems[17].value = [this.telemetry_data_obj.pdu_pdu_error];
      }
      if (this.telemetry_data_obj.pdu_DAC1 !== undefined) {
        this.PDUContainerItems[18].value = [this.telemetry_data_obj.pdu_DAC1];
      }
      if (this.telemetry_data_obj.pdu_DAC2 !== undefined) {
        this.PDUContainerItems[19].value = [this.telemetry_data_obj.pdu_DAC2];
      }
      if (this.telemetry_data_obj.pdu_max_cell_temp !== undefined) {
        this.PDUContainerItems[20].value = [this.telemetry_data_obj.pdu_max_cell_temp];
      }
      if (this.telemetry_data_obj.pdu_max_cell_temp_pos !== undefined) {
        this.PDUContainerItems[21].value = [this.telemetry_data_obj.pdu_max_cell_temp_pos];
      }
      if (this.telemetry_data_obj.pdu_min_cell_temp !== undefined) {
        this.PDUContainerItems[22].value = [this.telemetry_data_obj.pdu_min_cell_temp];
      }
      if (this.telemetry_data_obj.pdu_min_cell_temp_pos !== undefined) {
        this.PDUContainerItems[23].value = [this.telemetry_data_obj.pdu_min_cell_temp_pos];
      }
      if (this.telemetry_data_obj.pdu_avg_cell_temp !== undefined) {
        this.PDUContainerItems[24].value = [this.telemetry_data_obj.pdu_avg_cell_temp];
      }
      if (this.telemetry_data_obj.pdu_max_cell_voltage !== undefined) {
        this.PDUContainerItems[25].value = [this.telemetry_data_obj.pdu_max_cell_voltage];
      }
      if (this.telemetry_data_obj.pdu_max_cell_voltage_pos !== undefined) {
        this.PDUContainerItems[26].value = [this.telemetry_data_obj.pdu_max_cell_voltage_pos];
      }
      if (this.telemetry_data_obj.pdu_min_cell_voltage !== undefined) {
        this.PDUContainerItems[27].value = [this.telemetry_data_obj.pdu_min_cell_voltage];
      }
      if (this.telemetry_data_obj.pdu_min_cell_voltage_pos !== undefined) {
        this.PDUContainerItems[28].value = [this.telemetry_data_obj.pdu_min_cell_voltage_pos];
      }
      if (this.telemetry_data_obj.pdu_min_SoC !== undefined) {
        this.PDUContainerItems[29].value = [this.telemetry_data_obj.pdu_min_SoC];
      }
      if (this.telemetry_data_obj.pdu_max_SoC !== undefined) {
        this.PDUContainerItems[30].value = [this.telemetry_data_obj.pdu_max_SoC];
      }
      if (this.telemetry_data_obj.pdu_current_sense1 !== undefined) {
        this.PDUContainerItems[31].value = [this.telemetry_data_obj.pdu_current_sense1];
      }
      if (this.telemetry_data_obj.pdu_current_sense2 !== undefined) {
        this.PDUContainerItems[32].value = [this.telemetry_data_obj.pdu_current_sense2];
      }


      ////////////////////////////////////// MOTORS /////////////////////////////////////////////////////////////



      if (this.telemetry_data_obj.motor_requested_torque !== undefined) {
        this.MotorContainerItems[0].value = [this.telemetry_data_obj.motor_requested_torque];
      }
      if (this.telemetry_data_obj.motor_actual_torque !== undefined) {
        this.MotorContainerItems[1].value = [this.telemetry_data_obj.motor_actual_torque];
      }
      if (this.telemetry_data_obj.motor_rpm !== undefined) {
        this.MotorContainerItems[2].value = [this.telemetry_data_obj.motor_rpm];
      }
      if (this.telemetry_data_obj.motor_temp_too_high !== undefined) {
        this.MotorContainerItems[3].value = [this.telemetry_data_obj.motor_temp_too_high];
      }
      if (this.telemetry_data_obj.motor_temp_limit_reached !== undefined) {
        this.MotorContainerItems[4].value = [this.telemetry_data_obj.motor_temp_limit_reached];
      }
      if (this.telemetry_data_obj.motor_temp !== undefined) {
        this.MotorContainerItems[5].value = [this.telemetry_data_obj.motor_temp];
      }















    });

    // Listen for event transmitting the connection status.
    socket.on('connection_response', (message: event_connection_res) => {
      console.log("Connection Status: " + message.status)
      console.log("Connection Msg: " + message.msg)
    });


  },
  methods: {

  },
  computed: {
    // // Add computed property to return SideBarListItems

  },
  props: {
    //   statusbarstuff(): statusItems[] {
    //    return this.StatusItemList;
    //   }
  }
})
</script>
<!-- in the numrows remember to always include the header, in your calculations!!!!!!!!!!!!!!-->




<template>
    <!-- Main content -->
  <div class="p-0 mx-0 ml-35 mt-15 min-w-full overflow-y-auto"> <!-- ml==40 because max-w of side bar == 40 AND mt==20 bc statusbar height==3 -->
    <div class="grid grid-rows-20 grid-cols-12 gap-5">
      <AccuGeneralComponent
          :items="AccuContainerItems"
          :numRows="7"
          :numCols="5"
          class="ml-5 row-span-2 col-span-5 row-start-1 col-start-1"
      />

      <GeneralComponent
          :items="VCUContainerItems"
          :numRows="7"
          :numCols="5"
          containername="VCU"
          class=" ml-5 row-span-2 col-span-5"
      />

      <GeneralComponent
          :items="LeftInverterContainerItems"
          :numRows="7"
          :numCols="6"
          containername="Left_INV"
          class="row-span-5 col-span-5 col-start-1 "
      />
      <GeneralComponent
          :items="RightInverterContainerItems"
          :numRows="7"
          :numCols="6"
          containername="Right_INV"
          class="ml-15 row-span-5 col-span-5  col-start-6"
      />

      <GeneralComponent
          :items="PDUContainerItems"
          :numRows="3"
          :numCols="6"
          containername='PDU'
          class="row-span-2 col-span-5 ml-15"
      />

      <GeneralComponent
          :items="SensorsContainerItems"
          :numRows="7"
          :numCols="6"
          containername='SENSORS'
          class="row-span-3 col-span-5 ml-15"

        />

      <GeneralComponent
          :items="MotorContainerItems"
          :numRows="2"
          :numCols="3"
          containername='MOTOR'
          class="row-span-1 col-span-4 ml-15"
      />
    </div>
  </div>
</template>

<style scoped>
/* Adjust sidebar width and other styles as needed */



</style>
