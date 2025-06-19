<!-- Εδώ είναι το view που έχει τις περισσότερες μετρήσεις -->

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
  name: "Live_Values",
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
      accu_containeritems: [] as variableContainer[],
      vcu_containeritems: [] as variableContainer[],
      left_inv_containeritems: [] as variableContainer[],
      right_inv_containeritems: [] as variableContainer[],
      dv_containeritems: [] as variableContainer[],
	  sensors_containeritems: [] as variableContainer[],

      telemetry_data_obj: {} as VehicleTelemetry_data, //Object as typeof VehicleTelemetry_data
    }
  },
  watch: {

  },
  created() {
    //Listen for 'telemetry_data' event from server

this.accu_containeritems = [
 { label : ['total_voltage_vs'] },
 { label : ['accu_current'] },
 { label : ['over_60v_dclink'] },
 { label : ['air_m_state'] },
 { label : ['air_m_supp'] },
 { label : ['air_p_state'] },
 { label : ['air_p_supp'] },
 { label : ['precharge_state'] },
 { label : ['ts_active'] },
 { label : ['vicor_overtemp'] },
 { label : ['max_cell_temp'] },
 { label : ['min_cell_temp'] },
 { label : ['dcdc_temp'] },
 { label : ['max_humidity'] },
 { label : ['bms_error'] },
 { label : ['tsac_error'] },
 { label : ['max_soc'] },
 { label : ['min_soc'] },
 { label : ['imd_isolation_kOhms'] },
 { label : ['max_cell_voltage'] },
 { label : ['min_cell_voltage'] },
 { label : ['wh_consumed'] },
 { label : ['ah_consumed'] },
 { label : ['error_position'] },
 { label : ['min_cell_voltage_pos'] },
 { label : ['max_cell_voltage_pos'] },
 { label : ['last_bms_error'] },
 { label : ['last_tsac_error'] },
 { label : ['power'] },
 { label : ['tsac_fans'] },
 { label : ['turbine_fans'] },
 { label : ['pdu_max_temp'] },
 { label : ['pdu_current'] },
 { label : ['last_error'] },
 { label : ['dynamic_mode'] },
 { label : ['comm_error_ids'] },
 { label : ['HVroom_hum'] },
 { label : ['HVroom_temp'] },
 { label : ['precharge_voltage'] },
 { label : ['precharge_time'] },
 { label : ['imd_status'] },
 { label : ['imd_ok'] },
 { label : ['imd_sd_state'] },
 { label : ['ams_ok'] },
 { label : ['ams_sd_state'] },
]; 
this.vcu_containeritems = [
 { label : ['dtorque'] },
 { label : ['water_temp_in_right'] },
 { label : ['water_temp_out_right'] },
 { label : ['bspdState'] },
 { label : ['fan_right'] },
 { label : ['fan_left'] },
 { label : ['pump_right'] },
 { label : ['pump_left'] },
 { label : ['apps_right_implausibility'] },
 { label : ['apps_left_implausibility'] },
 { label : ['apps_deviation'] },
 { label : ['initial_check_state'] },
 { label : ['water_temp_in_left'] },
 { label : ['water_temp_out_left'] },
 { label : ['dash_power_limiter'] },
 { label : ['dash_traction_def'] },
 { label : ['yaw_rate_ref'] },
 { label : ['torque_left'] },
 { label : ['torque_right'] },
 { label : ['dw'] },
 { label : ['TVtrqLeft'] },
 { label : ['TVtrqRight'] },
 { label : ['antiw'] },
 { label : ['error'] },
 { label : ['integral'] },
 { label : ['integral_error'] },
 { label : ['m_z_nonsat'] },
 { label : ['m_z_sat'] },
 { label : ['prevError'] },
 { label : ['SteeringLinear_mm'] },
 { label : ['proportional'] },
]; 
this.right_inv_containeritems = [
 { label : ['critical_hw_status'] },
 { label : ['last_error'] },
 { label : ['can_state'] },
 { label : ['sys_status'] },
 { label : ['handler_status'] },
 { label : ['latched_error'] },
 { label : ['actual_inverter_status'] },
 { label : ['act_control_mode'] },
 { label : ['aux_hw_status'] },
 { label : ['id_ref'] },
 { label : ['iq_ref'] },
 { label : ['id'] },
 { label : ['iq'] },
 { label : ['iq_ref_request'] },
 { label : ['vdc_max'] },
 { label : ['vdc'] },
 { label : ['i1max'] },
 { label : ['i2max'] },
 { label : ['i3max'] },
 { label : ['Imax'] },
 { label : ['Imin'] },
 { label : ['trq_ref'] },
 { label : ['pwr_ref'] },
 { label : ['pwr_actual'] },
 { label : ['lim_speed_limiter'] },
 { label : ['lim_power_limiter'] },
 { label : ['lim_stall_limiter'] },
 { label : ['lim_l2t_limiter'] },
 { label : ['lim_motor_temp'] },
 { label : ['lim_igbt_temp'] },
 { label : ['motor_rpm'] },
 { label : ['num_max_trq'] },
 { label : ['vcu_max_velocity'] },
 { label : ['motor_temp'] },
 { label : ['igbt_temp'] },
 { label : ['trq_actual'] },
 { label : ['max_velocity'] },
 { label : ['min_velocity'] },
 { label : ['distance'] },
 { label : ['requested_torque_right'] },
]; 
this.left_inv_containeritems = [
 { label : ['ar'] },
 { label : ['Imax_ar'] },
 { label : ['critical_hw_status'] },
 { label : ['last_error'] },
 { label : ['can_state'] },
 { label : ['sys_status'] },
 { label : ['handler_status'] },
 { label : ['latched_error'] },
 { label : ['actual_inverter_status'] },
 { label : ['act_control_mode'] },
 { label : ['aux_hw_status'] },
 { label : ['id_ref'] },
 { label : ['iq_ref'] },
 { label : ['id'] },
 { label : ['iq'] },
 { label : ['iq_ref_request'] },
 { label : ['vdc_max'] },
 { label : ['dtorque'] },
 { label : ['vdc'] },
 { label : ['i1max'] },
 { label : ['i2max'] },
 { label : ['i3max'] },
 { label : ['Imax'] },
 { label : ['Imin'] },
 { label : ['trq_ref'] },
 { label : ['pwr_ref'] },
 { label : ['pwr_actual'] },
 { label : ['lim_speed_limiter'] },
 { label : ['lim_power_limiter'] },
 { label : ['lim_stall_limiter'] },
 { label : ['lim_l2t_limiter'] },
 { label : ['lim_motor_temp'] },
 { label : ['lim_igbt_temp'] },
 { label : ['motor_rpm'] },
 { label : ['num_max_trq'] },
 { label : ['vcu_max_velocity'] },
 { label : ['motor_temp'] },
 { label : ['igbt_temp'] },
 { label : ['trq_actual'] },
 { label : ['max_velocity'] },
 { label : ['min_velocity'] },
 { label : ['distance'] },
 { label : ['requested_torque_left'] },
]; 
this.dv_containeritems = [
 { label : ['as_ready'] },
 { label : ['maxon_brake_enable'] },
 { label : ['r2d_flag'] },
 { label : ['res_k3_switch'] },
 { label : ['res_k2_switch'] },
 { label : ['res_estop'] },
 { label : ['res_radio_quality'] },
 { label : ['as_status'] },
 { label : ['dv_status'] },
 { label : ['node_status'] },
 { label : ['steering_target'] },
 { label : ['brake_target'] },
 { label : ['speed_target'] },
 { label : ['pc_temp'] },
 { label : ['lap_counter'] },
 { label : ['DV_Velx'] },
 { label : ['DV_Vely'] },
 { label : ['dv_accel_x'] },
 { label : ['dv_accel_y'] },
 { label : ['dv_yaw_rate'] },
 { label : ['pc_flag'] },
 { label : ['as_ready_delay_passed'] },
]; 
this.sensors_containeritems = [
 { label : ['linear_rl'] },
 { label : ['linear_rr'] },
 { label : ['linear_fl'] },
 { label : ['linear_fr'] },
 { label : ['apps1'] },
 { label : ['apps2'] },
 { label : ['brake_front'] },
 { label : ['brake_rear'] },
 { label : ['hall_fr'] },
 { label : ['hall_fl'] },
 { label : ['VelX'] },
 { label : ['VelY'] },
 { label : ['yaw_rate'] },
 { label : ['Accel_x'] },
 { label : ['Accel_y'] },
 { label : ['Accel_z'] },
 { label : ['Gyro_x'] },
 { label : ['Gyro_y'] },
 { label : ['Gyro_z'] },
];  


    socket.on('telemetry_data', (telemetry_data: api_res) => {
      //Here we are updating the object every time we get a new message from the socket,

      //TODO - FIXXXX
      try {
        this.telemetry_data_obj = JSON.parse(telemetry_data.data as unknown as string) as VehicleTelemetry_data;
      } catch (e) {
        return null;
      }

	  ////////////     accu     ////////////
			if (this.telemetry_data_obj.accu_total_voltage_vs !== undefined) {
				this.accu_containeritems[0].value = [this.telemetry_data_obj.accu_total_voltage_vs];
			}
			if (this.telemetry_data_obj.accu_accu_current !== undefined) {
				this.accu_containeritems[1].value = [this.telemetry_data_obj.accu_accu_current];
			}
			if (this.telemetry_data_obj.accu_over_60v_dclink !== undefined) {
				this.accu_containeritems[2].value = [this.telemetry_data_obj.accu_over_60v_dclink];
			}
			if (this.telemetry_data_obj.accu_air_m_state !== undefined) {
				this.accu_containeritems[3].value = [this.telemetry_data_obj.accu_air_m_state];
			}
			if (this.telemetry_data_obj.accu_air_m_supp !== undefined) {
				this.accu_containeritems[4].value = [this.telemetry_data_obj.accu_air_m_supp];
			}
			if (this.telemetry_data_obj.accu_air_p_state !== undefined) {
				this.accu_containeritems[5].value = [this.telemetry_data_obj.accu_air_p_state];
			}
			if (this.telemetry_data_obj.accu_air_p_supp !== undefined) {
				this.accu_containeritems[6].value = [this.telemetry_data_obj.accu_air_p_supp];
			}
			if (this.telemetry_data_obj.accu_precharge_state !== undefined) {
				this.accu_containeritems[7].value = [this.telemetry_data_obj.accu_precharge_state];
			}
			if (this.telemetry_data_obj.accu_ts_active !== undefined) {
				this.accu_containeritems[8].value = [this.telemetry_data_obj.accu_ts_active];
			}
			if (this.telemetry_data_obj.accu_vicor_overtemp !== undefined) {
				this.accu_containeritems[9].value = [this.telemetry_data_obj.accu_vicor_overtemp];
			}
			if (this.telemetry_data_obj.accu_max_cell_temp !== undefined) {
				this.accu_containeritems[10].value = [this.telemetry_data_obj.accu_max_cell_temp];
			}
			if (this.telemetry_data_obj.accu_min_cell_temp !== undefined) {
				this.accu_containeritems[11].value = [this.telemetry_data_obj.accu_min_cell_temp];
			}
			if (this.telemetry_data_obj.accu_dcdc_temp !== undefined) {
				this.accu_containeritems[12].value = [this.telemetry_data_obj.accu_dcdc_temp];
			}
			if (this.telemetry_data_obj.accu_max_humidity !== undefined) {
				this.accu_containeritems[13].value = [this.telemetry_data_obj.accu_max_humidity];
			}
			if (this.telemetry_data_obj.accu_bms_error !== undefined) {
				this.accu_containeritems[14].value = [this.telemetry_data_obj.accu_bms_error];
			}
			if (this.telemetry_data_obj.accu_tsac_error !== undefined) {
				this.accu_containeritems[15].value = [this.telemetry_data_obj.accu_tsac_error];
			}
			if (this.telemetry_data_obj.accu_max_soc !== undefined) {
				this.accu_containeritems[16].value = [this.telemetry_data_obj.accu_max_soc];
			}
			if (this.telemetry_data_obj.accu_min_soc !== undefined) {
				this.accu_containeritems[17].value = [this.telemetry_data_obj.accu_min_soc];
			}
			if (this.telemetry_data_obj.accu_imd_isolation_kOhms !== undefined) {
				this.accu_containeritems[18].value = [this.telemetry_data_obj.accu_imd_isolation_kOhms];
			}
			if (this.telemetry_data_obj.accu_max_cell_voltage !== undefined) {
				this.accu_containeritems[19].value = [this.telemetry_data_obj.accu_max_cell_voltage];
			}
			if (this.telemetry_data_obj.accu_min_cell_voltage !== undefined) {
				this.accu_containeritems[20].value = [this.telemetry_data_obj.accu_min_cell_voltage];
			}
			if (this.telemetry_data_obj.accu_wh_consumed !== undefined) {
				this.accu_containeritems[21].value = [this.telemetry_data_obj.accu_wh_consumed];
			}
			if (this.telemetry_data_obj.accu_ah_consumed !== undefined) {
				this.accu_containeritems[22].value = [this.telemetry_data_obj.accu_ah_consumed];
			}
			if (this.telemetry_data_obj.accu_error_position !== undefined) {
				this.accu_containeritems[23].value = [this.telemetry_data_obj.accu_error_position];
			}
			if (this.telemetry_data_obj.accu_min_cell_voltage_pos !== undefined) {
				this.accu_containeritems[24].value = [this.telemetry_data_obj.accu_min_cell_voltage_pos];
			}
			if (this.telemetry_data_obj.accu_max_cell_voltage_pos !== undefined) {
				this.accu_containeritems[25].value = [this.telemetry_data_obj.accu_max_cell_voltage_pos];
			}
			if (this.telemetry_data_obj.accu_last_bms_error !== undefined) {
				this.accu_containeritems[26].value = [this.telemetry_data_obj.accu_last_bms_error];
			}
			if (this.telemetry_data_obj.accu_last_tsac_error !== undefined) {
				this.accu_containeritems[27].value = [this.telemetry_data_obj.accu_last_tsac_error];
			}
			if (this.telemetry_data_obj.accu_power !== undefined) {
				this.accu_containeritems[28].value = [this.telemetry_data_obj.accu_power];
			}
			if (this.telemetry_data_obj.accu_tsac_fans !== undefined) {
				this.accu_containeritems[29].value = [this.telemetry_data_obj.accu_tsac_fans];
			}
			if (this.telemetry_data_obj.accu_turbine_fans !== undefined) {
				this.accu_containeritems[30].value = [this.telemetry_data_obj.accu_turbine_fans];
			}
			if (this.telemetry_data_obj.pdu_max_temp !== undefined) {
				this.accu_containeritems[31].value = [this.telemetry_data_obj.pdu_max_temp];
			}
			if (this.telemetry_data_obj.pdu_current !== undefined) {
				this.accu_containeritems[32].value = [this.telemetry_data_obj.pdu_current];
			}
			if (this.telemetry_data_obj.accu_last_error !== undefined) {
				this.accu_containeritems[33].value = [this.telemetry_data_obj.accu_last_error];
			}
			if (this.telemetry_data_obj.accu_dynamic_mode !== undefined) {
				this.accu_containeritems[34].value = [this.telemetry_data_obj.accu_dynamic_mode];
			}
			if (this.telemetry_data_obj.accu_comm_error_ids !== undefined) {
				this.accu_containeritems[35].value = [this.telemetry_data_obj.accu_comm_error_ids];
			}
			if (this.telemetry_data_obj.accu_HVroom_hum !== undefined) {
				this.accu_containeritems[36].value = [this.telemetry_data_obj.accu_HVroom_hum];
			}
			if (this.telemetry_data_obj.accu_HVroom_temp !== undefined) {
				this.accu_containeritems[37].value = [this.telemetry_data_obj.accu_HVroom_temp];
			}
			if (this.telemetry_data_obj.accu_precharge_voltage !== undefined) {
				this.accu_containeritems[38].value = [this.telemetry_data_obj.accu_precharge_voltage];
			}
			if (this.telemetry_data_obj.accu_precharge_time !== undefined) {
				this.accu_containeritems[39].value = [this.telemetry_data_obj.accu_precharge_time];
			}
			if (this.telemetry_data_obj.accu_imd_status !== undefined) {
				this.accu_containeritems[40].value = [this.telemetry_data_obj.accu_imd_status];
			}
			if (this.telemetry_data_obj.accu_imd_ok !== undefined) {
				this.accu_containeritems[41].value = [this.telemetry_data_obj.accu_imd_ok];
			}
			if (this.telemetry_data_obj.accu_imd_sd_state !== undefined) {
				this.accu_containeritems[42].value = [this.telemetry_data_obj.accu_imd_sd_state];
			}
			if (this.telemetry_data_obj.accu_ams_ok !== undefined) {
				this.accu_containeritems[43].value = [this.telemetry_data_obj.accu_ams_ok];
			}
			if (this.telemetry_data_obj.accu_ams_sd_state !== undefined) {
				this.accu_containeritems[44].value = [this.telemetry_data_obj.accu_ams_sd_state];
			}
////////////     vcu     ////////////
			if (this.telemetry_data_obj.vcu_dtorque !== undefined) {
				this.vcu_containeritems[0].value = [this.telemetry_data_obj.vcu_dtorque];
			}
			if (this.telemetry_data_obj.vcu_water_temp_in_right !== undefined) {
				this.vcu_containeritems[1].value = [this.telemetry_data_obj.vcu_water_temp_in_right];
			}
			if (this.telemetry_data_obj.vcu_water_temp_out_right !== undefined) {
				this.vcu_containeritems[2].value = [this.telemetry_data_obj.vcu_water_temp_out_right];
			}
			if (this.telemetry_data_obj.vcu_bspdState !== undefined) {
				this.vcu_containeritems[3].value = [this.telemetry_data_obj.vcu_bspdState];
			}
			if (this.telemetry_data_obj.vcu_fan_right !== undefined) {
				this.vcu_containeritems[4].value = [this.telemetry_data_obj.vcu_fan_right];
			}
			if (this.telemetry_data_obj.vcu_fan_left !== undefined) {
				this.vcu_containeritems[5].value = [this.telemetry_data_obj.vcu_fan_left];
			}
			if (this.telemetry_data_obj.vcu_pump_right !== undefined) {
				this.vcu_containeritems[6].value = [this.telemetry_data_obj.vcu_pump_right];
			}
			if (this.telemetry_data_obj.vcu_pump_left !== undefined) {
				this.vcu_containeritems[7].value = [this.telemetry_data_obj.vcu_pump_left];
			}
			if (this.telemetry_data_obj.vcu_apps_right_implausibility !== undefined) {
				this.vcu_containeritems[8].value = [this.telemetry_data_obj.vcu_apps_right_implausibility];
			}
			if (this.telemetry_data_obj.vcu_apps_left_implausibility !== undefined) {
				this.vcu_containeritems[9].value = [this.telemetry_data_obj.vcu_apps_left_implausibility];
			}
			if (this.telemetry_data_obj.vcu_apps_deviation !== undefined) {
				this.vcu_containeritems[10].value = [this.telemetry_data_obj.vcu_apps_deviation];
			}
			if (this.telemetry_data_obj.vcu_initial_check_state !== undefined) {
				this.vcu_containeritems[11].value = [this.telemetry_data_obj.vcu_initial_check_state];
			}
			if (this.telemetry_data_obj.vcu_water_temp_in_left !== undefined) {
				this.vcu_containeritems[12].value = [this.telemetry_data_obj.vcu_water_temp_in_left];
			}
			if (this.telemetry_data_obj.vcu_water_temp_out_left !== undefined) {
				this.vcu_containeritems[13].value = [this.telemetry_data_obj.vcu_water_temp_out_left];
			}
			if (this.telemetry_data_obj.dash_power_limiter !== undefined) {
				this.vcu_containeritems[14].value = [this.telemetry_data_obj.dash_power_limiter];
			}
			if (this.telemetry_data_obj.dash_traction_def !== undefined) {
				this.vcu_containeritems[15].value = [this.telemetry_data_obj.dash_traction_def];
			}
			if (this.telemetry_data_obj.vcu_yaw_rate_ref !== undefined) {
				this.vcu_containeritems[16].value = [this.telemetry_data_obj.vcu_yaw_rate_ref];
			}
			if (this.telemetry_data_obj.vcu_torque_left !== undefined) {
				this.vcu_containeritems[17].value = [this.telemetry_data_obj.vcu_torque_left];
			}
			if (this.telemetry_data_obj.vcu_torque_right !== undefined) {
				this.vcu_containeritems[18].value = [this.telemetry_data_obj.vcu_torque_right];
			}
			if (this.telemetry_data_obj.vcu_dw !== undefined) {
				this.vcu_containeritems[19].value = [this.telemetry_data_obj.vcu_dw];
			}
			if (this.telemetry_data_obj.vcu_TVtrqLeft !== undefined) {
				this.vcu_containeritems[20].value = [this.telemetry_data_obj.vcu_TVtrqLeft];
			}
			if (this.telemetry_data_obj.vcu_TVtrqRight !== undefined) {
				this.vcu_containeritems[21].value = [this.telemetry_data_obj.vcu_TVtrqRight];
			}
			if (this.telemetry_data_obj.vcu_antiw !== undefined) {
				this.vcu_containeritems[22].value = [this.telemetry_data_obj.vcu_antiw];
			}
			if (this.telemetry_data_obj.vcu_error !== undefined) {
				this.vcu_containeritems[23].value = [this.telemetry_data_obj.vcu_error];
			}
			if (this.telemetry_data_obj.vcu_integral !== undefined) {
				this.vcu_containeritems[24].value = [this.telemetry_data_obj.vcu_integral];
			}
			if (this.telemetry_data_obj.vcu_integral_error !== undefined) {
				this.vcu_containeritems[25].value = [this.telemetry_data_obj.vcu_integral_error];
			}
			if (this.telemetry_data_obj.vcu_m_z_nonsat !== undefined) {
				this.vcu_containeritems[26].value = [this.telemetry_data_obj.vcu_m_z_nonsat];
			}
			if (this.telemetry_data_obj.vcu_m_z_sat !== undefined) {
				this.vcu_containeritems[27].value = [this.telemetry_data_obj.vcu_m_z_sat];
			}
			if (this.telemetry_data_obj.vcu_prevError !== undefined) {
				this.vcu_containeritems[28].value = [this.telemetry_data_obj.vcu_prevError];
			}
			if (this.telemetry_data_obj.vcu_SteeringLinear_mm !== undefined) {
				this.vcu_containeritems[29].value = [this.telemetry_data_obj.vcu_SteeringLinear_mm];
			}
			if (this.telemetry_data_obj.vcu_proportional !== undefined) {
				this.vcu_containeritems[30].value = [this.telemetry_data_obj.vcu_proportional];
			}
////////////     right_inv     ////////////
			if (this.telemetry_data_obj.right_inv_critical_hw_status !== undefined) {
				this.right_inv_containeritems[0].value = [this.telemetry_data_obj.right_inv_critical_hw_status];
			}
			if (this.telemetry_data_obj.right_inv_last_error !== undefined) {
				this.right_inv_containeritems[1].value = [this.telemetry_data_obj.right_inv_last_error];
			}
			if (this.telemetry_data_obj.right_inv_can_state !== undefined) {
				this.right_inv_containeritems[2].value = [this.telemetry_data_obj.right_inv_can_state];
			}
			if (this.telemetry_data_obj.right_inv_sys_status !== undefined) {
				this.right_inv_containeritems[3].value = [this.telemetry_data_obj.right_inv_sys_status];
			}
			if (this.telemetry_data_obj.right_inv_handler_status !== undefined) {
				this.right_inv_containeritems[4].value = [this.telemetry_data_obj.right_inv_handler_status];
			}
			if (this.telemetry_data_obj.right_inv_latched_error !== undefined) {
				this.right_inv_containeritems[5].value = [this.telemetry_data_obj.right_inv_latched_error];
			}
			if (this.telemetry_data_obj.right_inv_actual_inverter_status !== undefined) {
				this.right_inv_containeritems[6].value = [this.telemetry_data_obj.right_inv_actual_inverter_status];
			}
			if (this.telemetry_data_obj.right_inv_act_control_mode !== undefined) {
				this.right_inv_containeritems[7].value = [this.telemetry_data_obj.right_inv_act_control_mode];
			}
			if (this.telemetry_data_obj.right_inv_aux_hw_status !== undefined) {
				this.right_inv_containeritems[8].value = [this.telemetry_data_obj.right_inv_aux_hw_status];
			}
			if (this.telemetry_data_obj.right_inv_id_ref !== undefined) {
				this.right_inv_containeritems[9].value = [this.telemetry_data_obj.right_inv_id_ref];
			}
			if (this.telemetry_data_obj.right_inv_iq_ref !== undefined) {
				this.right_inv_containeritems[10].value = [this.telemetry_data_obj.right_inv_iq_ref];
			}
			if (this.telemetry_data_obj.right_inv_id !== undefined) {
				this.right_inv_containeritems[11].value = [this.telemetry_data_obj.right_inv_id];
			}
			if (this.telemetry_data_obj.right_inv_iq !== undefined) {
				this.right_inv_containeritems[12].value = [this.telemetry_data_obj.right_inv_iq];
			}
			if (this.telemetry_data_obj.right_inv_iq_ref_request !== undefined) {
				this.right_inv_containeritems[13].value = [this.telemetry_data_obj.right_inv_iq_ref_request];
			}
			if (this.telemetry_data_obj.right_inv_vdc_max !== undefined) {
				this.right_inv_containeritems[14].value = [this.telemetry_data_obj.right_inv_vdc_max];
			}
			if (this.telemetry_data_obj.right_inv_vdc !== undefined) {
				this.right_inv_containeritems[15].value = [this.telemetry_data_obj.right_inv_vdc];
			}
			if (this.telemetry_data_obj.right_inv_i1max !== undefined) {
				this.right_inv_containeritems[16].value = [this.telemetry_data_obj.right_inv_i1max];
			}
			if (this.telemetry_data_obj.right_inv_i2max !== undefined) {
				this.right_inv_containeritems[17].value = [this.telemetry_data_obj.right_inv_i2max];
			}
			if (this.telemetry_data_obj.right_inv_i3max !== undefined) {
				this.right_inv_containeritems[18].value = [this.telemetry_data_obj.right_inv_i3max];
			}
			if (this.telemetry_data_obj.right_inv_Imax !== undefined) {
				this.right_inv_containeritems[19].value = [this.telemetry_data_obj.right_inv_Imax];
			}
			if (this.telemetry_data_obj.right_inv_Imin !== undefined) {
				this.right_inv_containeritems[20].value = [this.telemetry_data_obj.right_inv_Imin];
			}
			if (this.telemetry_data_obj.right_inv_trq_ref !== undefined) {
				this.right_inv_containeritems[21].value = [this.telemetry_data_obj.right_inv_trq_ref];
			}
			if (this.telemetry_data_obj.right_inv_pwr_ref !== undefined) {
				this.right_inv_containeritems[22].value = [this.telemetry_data_obj.right_inv_pwr_ref];
			}
			if (this.telemetry_data_obj.right_inv_pwr_actual !== undefined) {
				this.right_inv_containeritems[23].value = [this.telemetry_data_obj.right_inv_pwr_actual];
			}
			if (this.telemetry_data_obj.right_inv_lim_speed_limiter !== undefined) {
				this.right_inv_containeritems[24].value = [this.telemetry_data_obj.right_inv_lim_speed_limiter];
			}
			if (this.telemetry_data_obj.right_inv_lim_power_limiter !== undefined) {
				this.right_inv_containeritems[25].value = [this.telemetry_data_obj.right_inv_lim_power_limiter];
			}
			if (this.telemetry_data_obj.right_inv_lim_stall_limiter !== undefined) {
				this.right_inv_containeritems[26].value = [this.telemetry_data_obj.right_inv_lim_stall_limiter];
			}
			if (this.telemetry_data_obj.right_inv_lim_l2t_limiter !== undefined) {
				this.right_inv_containeritems[27].value = [this.telemetry_data_obj.right_inv_lim_l2t_limiter];
			}
			if (this.telemetry_data_obj.right_inv_lim_motor_temp !== undefined) {
				this.right_inv_containeritems[28].value = [this.telemetry_data_obj.right_inv_lim_motor_temp];
			}
			if (this.telemetry_data_obj.right_inv_lim_igbt_temp !== undefined) {
				this.right_inv_containeritems[29].value = [this.telemetry_data_obj.right_inv_lim_igbt_temp];
			}
			if (this.telemetry_data_obj.right_inv_motor_rpm !== undefined) {
				this.right_inv_containeritems[30].value = [this.telemetry_data_obj.right_inv_motor_rpm];
			}
			if (this.telemetry_data_obj.right_inv_num_max_trq !== undefined) {
				this.right_inv_containeritems[31].value = [this.telemetry_data_obj.right_inv_num_max_trq];
			}
			if (this.telemetry_data_obj.right_inv_vcu_max_velocity !== undefined) {
				this.right_inv_containeritems[32].value = [this.telemetry_data_obj.right_inv_vcu_max_velocity];
			}
			if (this.telemetry_data_obj.right_inv_motor_temp !== undefined) {
				this.right_inv_containeritems[33].value = [this.telemetry_data_obj.right_inv_motor_temp];
			}
			if (this.telemetry_data_obj.right_inv_igbt_temp !== undefined) {
				this.right_inv_containeritems[34].value = [this.telemetry_data_obj.right_inv_igbt_temp];
			}
			if (this.telemetry_data_obj.right_inv_trq_actual !== undefined) {
				this.right_inv_containeritems[35].value = [this.telemetry_data_obj.right_inv_trq_actual];
			}
			if (this.telemetry_data_obj.right_inv_max_velocity !== undefined) {
				this.right_inv_containeritems[36].value = [this.telemetry_data_obj.right_inv_max_velocity];
			}
			if (this.telemetry_data_obj.right_inv_min_velocity !== undefined) {
				this.right_inv_containeritems[37].value = [this.telemetry_data_obj.right_inv_min_velocity];
			}
			if (this.telemetry_data_obj.right_inv_distance !== undefined) {
				this.right_inv_containeritems[38].value = [this.telemetry_data_obj.right_inv_distance];
			}
			if (this.telemetry_data_obj.vcu_requested_torque_right !== undefined) {
				this.right_inv_containeritems[39].value = [this.telemetry_data_obj.vcu_requested_torque_right];
			}
////////////     left_inv     ////////////
			if (this.telemetry_data_obj.left_inv_ar !== undefined) {
				this.left_inv_containeritems[0].value = [this.telemetry_data_obj.left_inv_ar];
			}
			if (this.telemetry_data_obj.left_inv_Imax_ar !== undefined) {
				this.left_inv_containeritems[1].value = [this.telemetry_data_obj.left_inv_Imax_ar];
			}
			if (this.telemetry_data_obj.left_inv_critical_hw_status !== undefined) {
				this.left_inv_containeritems[2].value = [this.telemetry_data_obj.left_inv_critical_hw_status];
			}
			if (this.telemetry_data_obj.left_inv_last_error !== undefined) {
				this.left_inv_containeritems[3].value = [this.telemetry_data_obj.left_inv_last_error];
			}
			if (this.telemetry_data_obj.left_inv_can_state !== undefined) {
				this.left_inv_containeritems[4].value = [this.telemetry_data_obj.left_inv_can_state];
			}
			if (this.telemetry_data_obj.left_inv_sys_status !== undefined) {
				this.left_inv_containeritems[5].value = [this.telemetry_data_obj.left_inv_sys_status];
			}
			if (this.telemetry_data_obj.left_inv_handler_status !== undefined) {
				this.left_inv_containeritems[6].value = [this.telemetry_data_obj.left_inv_handler_status];
			}
			if (this.telemetry_data_obj.left_inv_latched_error !== undefined) {
				this.left_inv_containeritems[7].value = [this.telemetry_data_obj.left_inv_latched_error];
			}
			if (this.telemetry_data_obj.left_inv_actual_inverter_status !== undefined) {
				this.left_inv_containeritems[8].value = [this.telemetry_data_obj.left_inv_actual_inverter_status];
			}
			if (this.telemetry_data_obj.left_inv_act_control_mode !== undefined) {
				this.left_inv_containeritems[9].value = [this.telemetry_data_obj.left_inv_act_control_mode];
			}
			if (this.telemetry_data_obj.left_inv_aux_hw_status !== undefined) {
				this.left_inv_containeritems[10].value = [this.telemetry_data_obj.left_inv_aux_hw_status];
			}
			if (this.telemetry_data_obj.left_inv_id_ref !== undefined) {
				this.left_inv_containeritems[11].value = [this.telemetry_data_obj.left_inv_id_ref];
			}
			if (this.telemetry_data_obj.left_inv_iq_ref !== undefined) {
				this.left_inv_containeritems[12].value = [this.telemetry_data_obj.left_inv_iq_ref];
			}
			if (this.telemetry_data_obj.left_inv_id !== undefined) {
				this.left_inv_containeritems[13].value = [this.telemetry_data_obj.left_inv_id];
			}
			if (this.telemetry_data_obj.left_inv_iq !== undefined) {
				this.left_inv_containeritems[14].value = [this.telemetry_data_obj.left_inv_iq];
			}
			if (this.telemetry_data_obj.left_inv_iq_ref_request !== undefined) {
				this.left_inv_containeritems[15].value = [this.telemetry_data_obj.left_inv_iq_ref_request];
			}
			if (this.telemetry_data_obj.left_inv_vdc_max !== undefined) {
				this.left_inv_containeritems[16].value = [this.telemetry_data_obj.left_inv_vdc_max];
			}
			if (this.telemetry_data_obj.left_inv_dtorque !== undefined) {
				this.left_inv_containeritems[17].value = [this.telemetry_data_obj.left_inv_dtorque];
			}
			if (this.telemetry_data_obj.left_inv_vdc !== undefined) {
				this.left_inv_containeritems[18].value = [this.telemetry_data_obj.left_inv_vdc];
			}
			if (this.telemetry_data_obj.left_inv_i1max !== undefined) {
				this.left_inv_containeritems[19].value = [this.telemetry_data_obj.left_inv_i1max];
			}
			if (this.telemetry_data_obj.left_inv_i2max !== undefined) {
				this.left_inv_containeritems[20].value = [this.telemetry_data_obj.left_inv_i2max];
			}
			if (this.telemetry_data_obj.left_inv_i3max !== undefined) {
				this.left_inv_containeritems[21].value = [this.telemetry_data_obj.left_inv_i3max];
			}
			if (this.telemetry_data_obj.left_inv_Imax !== undefined) {
				this.left_inv_containeritems[22].value = [this.telemetry_data_obj.left_inv_Imax];
			}
			if (this.telemetry_data_obj.left_inv_Imin !== undefined) {
				this.left_inv_containeritems[23].value = [this.telemetry_data_obj.left_inv_Imin];
			}
			if (this.telemetry_data_obj.left_inv_trq_ref !== undefined) {
				this.left_inv_containeritems[24].value = [this.telemetry_data_obj.left_inv_trq_ref];
			}
			if (this.telemetry_data_obj.left_inv_pwr_ref !== undefined) {
				this.left_inv_containeritems[25].value = [this.telemetry_data_obj.left_inv_pwr_ref];
			}
			if (this.telemetry_data_obj.left_inv_pwr_actual !== undefined) {
				this.left_inv_containeritems[26].value = [this.telemetry_data_obj.left_inv_pwr_actual];
			}
			if (this.telemetry_data_obj.left_inv_lim_speed_limiter !== undefined) {
				this.left_inv_containeritems[27].value = [this.telemetry_data_obj.left_inv_lim_speed_limiter];
			}
			if (this.telemetry_data_obj.left_inv_lim_power_limiter !== undefined) {
				this.left_inv_containeritems[28].value = [this.telemetry_data_obj.left_inv_lim_power_limiter];
			}
			if (this.telemetry_data_obj.left_inv_lim_stall_limiter !== undefined) {
				this.left_inv_containeritems[29].value = [this.telemetry_data_obj.left_inv_lim_stall_limiter];
			}
			if (this.telemetry_data_obj.left_inv_lim_l2t_limiter !== undefined) {
				this.left_inv_containeritems[30].value = [this.telemetry_data_obj.left_inv_lim_l2t_limiter];
			}
			if (this.telemetry_data_obj.left_inv_lim_motor_temp !== undefined) {
				this.left_inv_containeritems[31].value = [this.telemetry_data_obj.left_inv_lim_motor_temp];
			}
			if (this.telemetry_data_obj.left_inv_lim_igbt_temp !== undefined) {
				this.left_inv_containeritems[32].value = [this.telemetry_data_obj.left_inv_lim_igbt_temp];
			}
			if (this.telemetry_data_obj.left_inv_motor_rpm !== undefined) {
				this.left_inv_containeritems[33].value = [this.telemetry_data_obj.left_inv_motor_rpm];
			}
			if (this.telemetry_data_obj.left_inv_num_max_trq !== undefined) {
				this.left_inv_containeritems[34].value = [this.telemetry_data_obj.left_inv_num_max_trq];
			}
			if (this.telemetry_data_obj.left_inv_vcu_max_velocity !== undefined) {
				this.left_inv_containeritems[35].value = [this.telemetry_data_obj.left_inv_vcu_max_velocity];
			}
			if (this.telemetry_data_obj.left_inv_motor_temp !== undefined) {
				this.left_inv_containeritems[36].value = [this.telemetry_data_obj.left_inv_motor_temp];
			}
			if (this.telemetry_data_obj.left_inv_igbt_temp !== undefined) {
				this.left_inv_containeritems[37].value = [this.telemetry_data_obj.left_inv_igbt_temp];
			}
			if (this.telemetry_data_obj.left_inv_trq_actual !== undefined) {
				this.left_inv_containeritems[38].value = [this.telemetry_data_obj.left_inv_trq_actual];
			}
			if (this.telemetry_data_obj.left_inv_max_velocity !== undefined) {
				this.left_inv_containeritems[39].value = [this.telemetry_data_obj.left_inv_max_velocity];
			}
			if (this.telemetry_data_obj.left_inv_min_velocity !== undefined) {
				this.left_inv_containeritems[40].value = [this.telemetry_data_obj.left_inv_min_velocity];
			}
			if (this.telemetry_data_obj.left_inv_distance !== undefined) {
				this.left_inv_containeritems[41].value = [this.telemetry_data_obj.left_inv_distance];
			}
			if (this.telemetry_data_obj.vcu_requested_torque_left !== undefined) {
				this.left_inv_containeritems[42].value = [this.telemetry_data_obj.vcu_requested_torque_left];
			}
////////////     dv     ////////////
			if (this.telemetry_data_obj.vcu_as_ready !== undefined) {
				this.dv_containeritems[0].value = [this.telemetry_data_obj.vcu_as_ready];
			}
			if (this.telemetry_data_obj.vcu_maxon_brake_enable !== undefined) {
				this.dv_containeritems[1].value = [this.telemetry_data_obj.vcu_maxon_brake_enable];
			}
			if (this.telemetry_data_obj.vcu_r2d_flag !== undefined) {
				this.dv_containeritems[2].value = [this.telemetry_data_obj.vcu_r2d_flag];
			}
			if (this.telemetry_data_obj.vcu_res_k3_switch !== undefined) {
				this.dv_containeritems[3].value = [this.telemetry_data_obj.vcu_res_k3_switch];
			}
			if (this.telemetry_data_obj.vcu_res_k2_switch !== undefined) {
				this.dv_containeritems[4].value = [this.telemetry_data_obj.vcu_res_k2_switch];
			}
			if (this.telemetry_data_obj.vcu_res_estop !== undefined) {
				this.dv_containeritems[5].value = [this.telemetry_data_obj.vcu_res_estop];
			}
			if (this.telemetry_data_obj.vcu_res_radio_quality !== undefined) {
				this.dv_containeritems[6].value = [this.telemetry_data_obj.vcu_res_radio_quality];
			}
			if (this.telemetry_data_obj.vcu_as_status !== undefined) {
				this.dv_containeritems[7].value = [this.telemetry_data_obj.vcu_as_status];
			}
			if (this.telemetry_data_obj.vcu_dv_status !== undefined) {
				this.dv_containeritems[8].value = [this.telemetry_data_obj.vcu_dv_status];
			}
			if (this.telemetry_data_obj.vcu_node_status !== undefined) {
				this.dv_containeritems[9].value = [this.telemetry_data_obj.vcu_node_status];
			}
			if (this.telemetry_data_obj.vcu_steering_target !== undefined) {
				this.dv_containeritems[10].value = [this.telemetry_data_obj.vcu_steering_target];
			}
			if (this.telemetry_data_obj.vcu_brake_target !== undefined) {
				this.dv_containeritems[11].value = [this.telemetry_data_obj.vcu_brake_target];
			}
			if (this.telemetry_data_obj.vcu_speed_target !== undefined) {
				this.dv_containeritems[12].value = [this.telemetry_data_obj.vcu_speed_target];
			}
			if (this.telemetry_data_obj.vcu_pc_temp !== undefined) {
				this.dv_containeritems[13].value = [this.telemetry_data_obj.vcu_pc_temp];
			}
			if (this.telemetry_data_obj.vcu_lap_counter !== undefined) {
				this.dv_containeritems[14].value = [this.telemetry_data_obj.vcu_lap_counter];
			}
			if (this.telemetry_data_obj.vcu_DV_Velx !== undefined) {
				this.dv_containeritems[15].value = [this.telemetry_data_obj.vcu_DV_Velx];
			}
			if (this.telemetry_data_obj.vcu_DV_Vely !== undefined) {
				this.dv_containeritems[16].value = [this.telemetry_data_obj.vcu_DV_Vely];
			}
			if (this.telemetry_data_obj.vcu_dv_accel_x !== undefined) {
				this.dv_containeritems[17].value = [this.telemetry_data_obj.vcu_dv_accel_x];
			}
			if (this.telemetry_data_obj.vcu_dv_accel_y !== undefined) {
				this.dv_containeritems[18].value = [this.telemetry_data_obj.vcu_dv_accel_y];
			}
			if (this.telemetry_data_obj.vcu_dv_yaw_rate !== undefined) {
				this.dv_containeritems[19].value = [this.telemetry_data_obj.vcu_dv_yaw_rate];
			}
			if (this.telemetry_data_obj.vcu_pc_flag !== undefined) {
				this.dv_containeritems[20].value = [this.telemetry_data_obj.vcu_pc_flag];
			}
			if (this.telemetry_data_obj.vcu_as_ready_delay_passed !== undefined) {
				this.dv_containeritems[21].value = [this.telemetry_data_obj.vcu_as_ready_delay_passed];
			}
////////////     sensors     ////////////
			if (this.telemetry_data_obj.sensors_linear_rl !== undefined) {
				this.sensors_containeritems[0].value = [this.telemetry_data_obj.sensors_linear_rl];
			}
			if (this.telemetry_data_obj.sensors_linear_rr !== undefined) {
				this.sensors_containeritems[1].value = [this.telemetry_data_obj.sensors_linear_rr];
			}
			if (this.telemetry_data_obj.sensors_linear_fl !== undefined) {
				this.sensors_containeritems[2].value = [this.telemetry_data_obj.sensors_linear_fl];
			}
			if (this.telemetry_data_obj.sensors_linear_fr !== undefined) {
				this.sensors_containeritems[3].value = [this.telemetry_data_obj.sensors_linear_fr];
			}
			if (this.telemetry_data_obj.vcu_apps1 !== undefined) {
				this.sensors_containeritems[4].value = [this.telemetry_data_obj.vcu_apps1];
			}
			if (this.telemetry_data_obj.vcu_apps2 !== undefined) {
				this.sensors_containeritems[5].value = [this.telemetry_data_obj.vcu_apps2];
			}
			if (this.telemetry_data_obj.vcu_brake_front !== undefined) {
				this.sensors_containeritems[6].value = [this.telemetry_data_obj.vcu_brake_front];
			}
			if (this.telemetry_data_obj.vcu_brake_rear !== undefined) {
				this.sensors_containeritems[7].value = [this.telemetry_data_obj.vcu_brake_rear];
			}
			if (this.telemetry_data_obj.vcu_hall_fr !== undefined) {
				this.sensors_containeritems[8].value = [this.telemetry_data_obj.vcu_hall_fr];
			}
			if (this.telemetry_data_obj.vcu_hall_fl !== undefined) {
				this.sensors_containeritems[9].value = [this.telemetry_data_obj.vcu_hall_fl];
			}
			if (this.telemetry_data_obj.vcu_VelX !== undefined) {
				this.sensors_containeritems[10].value = [this.telemetry_data_obj.vcu_VelX];
			}
			if (this.telemetry_data_obj.vcu_VelY !== undefined) {
				this.sensors_containeritems[11].value = [this.telemetry_data_obj.vcu_VelY];
			}
			if (this.telemetry_data_obj.vcu_yaw_rate !== undefined) {
				this.sensors_containeritems[12].value = [this.telemetry_data_obj.vcu_yaw_rate];
			}
			if (this.telemetry_data_obj.vcu_Accel_x !== undefined) {
				this.sensors_containeritems[13].value = [this.telemetry_data_obj.vcu_Accel_x];
			}
			if (this.telemetry_data_obj.vcu_Accel_y !== undefined) {
				this.sensors_containeritems[14].value = [this.telemetry_data_obj.vcu_Accel_y];
			}
			if (this.telemetry_data_obj.vcu_Accel_z !== undefined) {
				this.sensors_containeritems[15].value = [this.telemetry_data_obj.vcu_Accel_z];
			}
			if (this.telemetry_data_obj.vcu_Gyro_x !== undefined) {
				this.sensors_containeritems[16].value = [this.telemetry_data_obj.vcu_Gyro_x];
			}
			if (this.telemetry_data_obj.vcu_Gyro_y !== undefined) {
				this.sensors_containeritems[17].value = [this.telemetry_data_obj.vcu_Gyro_y];
			}
			if (this.telemetry_data_obj.vcu_Gyro_z !== undefined) {
				this.sensors_containeritems[18].value = [this.telemetry_data_obj.vcu_Gyro_z];
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
})
</script>
<!-- in the numrows remember to always include the header, in your calculations!!!!!!!!!!!!!!-->

<template>
    <!-- Main content -->
  <div class="p-0 mx-0 ml-40 mt-20 min-w-full overflow-y-auto"> <!-- ml==40 because max-w of side bar == 40 AND mt==20 bc statusbar height==3 -->
	<div class="grid grid-rows-20 grid-cols-12 gap-5">
      <AccuGeneralComponent
          :items="accu_containeritems"
          :numRows="9"
          :numCols="6"
          class="row-span-2 col-span-5"
      />

      <GeneralComponent
          :items="vcu_containeritems"
          :numRows="9"
          :numCols="6"
          containername="VCU"
          class="row-span-2 col-span-5"
      />

      <GeneralComponent
          :items="left_inv_containeritems"
          :numRows="8"
          :numCols="6"
          containername="Left_INV"
          class="row-span-5 col-span-5"
      />
      <GeneralComponent
          :items="right_inv_containeritems"
          :numRows="8"
          :numCols="6"
          containername="Right_INV"
          class="row-span-5 col-span-5"
      />

      <GeneralComponent
          :items="dv_containeritems"
          :numRows="4"
          :numCols="6"
          containername='DV'
          class="row-span-2 col-span-5"
      />

      <GeneralComponent
          :items="sensors_containeritems"
          :numRows="4"
          :numCols="6"
          containername='Sensors'
          class="row-span-2 col-span-5"
        />
    </div>
  </div>
</template>

<style scoped>
/* Adjust sidebar width and other styles as needed */
</style>
