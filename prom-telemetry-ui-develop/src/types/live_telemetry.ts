//Αυτό το datatype έχει το σύνολο των δεδομένων για την τηλεμετρία
export type VehicleTelemetry_data = {
    //ACCU
    accu_over_60v_dclink?: number; 
    accu_air_m_state?: number;
    accu_air_m_supp?: number ;
    accu_air_p_state?: number;
    accu_air_p_supp?: number;
    accu_precharge_state?: number;
    accu_ts_active?: number;
    accu_vicor_overtemp?: number;
    accu_max_cell_temp?: number;
    accu_min_cell_temp?: number;
    accu_dcdc_temp?: number;
    accu_max_humidity?: number;
    accu_bms_error_code?: number;
    accu_tsac_error_code?: number;
    accu_max_soc?: number;
    accu_min_soc?: number;
    accu_total_voltage_vs?: number;
    accu_accu_current?: number;
    accu_max_cell_voltage?: number;
    accu_min_cell_voltage?: number;
    accu_wh_consumed?: number;
    accu_ah_consumed?: number;
    accu_error_position?: number;
    accu_min_cell_voltage_pos?: number;
    accu_max_cell_voltage_pos?: number;
    accu_last_bms_error_code?: number;
    accu_last_tsac_error_code?: number;
    accu_imd_isolation_kOhms?: number;
    accu_tsac_fans?: number;
    accu_turbine_fans?: number;
    accu_power?: number;

    //PDU
    pdu_bms_state?: number;
    pdu_bms_last_error?: number;
    pdu_pdu_state?: number;
    pdu_pdu_last_error?: number;
    pdu_position_of_error?: number;
    pdu_TDK1_temp?: number;
    pdu_TDK2_temp?: number;
    pdu_max_humidity?: number;
    pdu_max_temperature?: number;
    pdu_enable_tdk1?: number;
    pdu_enable_tdk2?: number;
    pdu_precharge_enabled?: number;
    pdu_ams_error?: number;
    pdu_tdkLV_overtemp?: number;
    pdu_tdkTS_overtemp?: number;
    pdu_tdkLV_overcurrent?: number;
    pdu_tdkTS_overcurrent?: number;
    pdu_pdu_error?: number;
    pdu_DAC_1?: number;
    pdu_DAC_2?: number;
    pdu_max_cell_temp?: number;
    pdu_max_cell_temp_pos?: number;
    pdu_min_cell_temp?: number;
    pdu_min_cell_temp_pos?: number;
    pdu_avg_cell_temp?: number;
    pdu_max_cell_voltage?: number;
    pdu_max_cell_voltage_pos?: number;
    pdu_min_cell_voltage?: number;
    pdu_min_cell_voltage_pos?: number;
    pdu_min_SoC?: number;
    pdu_max_SoC?: number;
    pdu_current_sense1?: number;
    pdu_current_sense2?: number;
    pdu_sharing_enabled?: number;
    pdu_max_tempurature?: number;

    //Sensors NOT FOUND ON MSG
    sensors_fr_channel1?: number;
    sensors_fr_channel2?: number;
    sensors_fr_channel3?: number;
    sensors_fr_channel4?: number;
    sensors_fl_avg?: number;
    sensors_fl_channel1?: number;
    sensors_fl_channel2?: number;
    sensors_fl_channel3?: number;
    sensors_fl_channel4?: number;
    sensors_rr_avg?: number;
    sensors_rr_channel1?: number;
    sensors_rr_channel2?: number;
    sensors_rr_channel3?: number;
    sensors_rr_channel4?: number;
    sensors_rl_avg?: number;
    sensors_rl_channel1?: number;
    sensors_rl_channel2?: number;
    sensors_rl_channel3?: number;
    sensors_rl_channel4?: number;
    sensors_rol?: number;
    sensors_heave?: number;
    sensors_rl?: number;
    sensors_rr?: number;
    sensors_pressure?: number;
    sensors_speed?: number;
    sensors_temp?: number;
    sensors_fr_press?: number;
    sensors_fr_temp?: number;
    sensors_fl_press?: number;
    sensors_fl_temp?: number;
    sensors_rr_press?: number;
    sensors_rr_temp?: number;
    sensors_rl_press?: number;
    sensors_rl_temp?: number;
    sensors_accel_long?: number;
    sensors_accel_lat?: number;
    sensors_gps_speed?: number;
    sensors_front?: number;
    sensors_rear?: number;
    sensors_apps1?: number;
    sensors_apps2?: number;
    sensors_fr?: number;
    sensors_fl?: number;
    sensors_requested_torque?: number;
    sensors_actual_torque?: number;
    sensors_motor_rpm?: number;
    sensors_motor_temp_too_high?: number;
    sensors_motor_temp_limit_reached?: number;
    sensors_motor_temp?: number;

    //Inverter Left
    left_inv_ar?: number;
    left_inv_Imax_ar?: number;
    left_inv_critical_hw_status?: number;
    left_inv_last_error?: number;
    left_inv_can_state?: number;
    left_inv_sys_status?: number;
    left_inv_handler_status?: number;
    left_inv_latched_error?: number;
    left_inv_actual_inverter_status?: number;
    left_inv_actual_control_mode?: number;
    left_inv_aux_hw_status?: number;
    left_inv_id_ref?: number;
    left_inv_iq_ref?: number;
    left_inv_id?: number;
    left_inv_iq?: number;
    left_inv_iq_ref_request?: number;
    left_inv_vdc_max?: number;
    left_inv_dtorque?: number;
    left_inv_vdc?: number;
    left_inv_i1max?: number;
    left_inv_i2max?: number;
    left_inv_i3max?: number;
    left_inv_Imax?: number;
    left_inv_Imin?: number;
    left_inv_trq_ref?: number;
    left_inv_pwr_ref?: number;
    left_inv_pwr_actual?: number;
    left_inv_lim_speed_limiter?: number;
    left_inv_lim_power_limiter?: number;
    left_inv_lim_stall_limiter?: number;
    left_inv_lim_l2t_limiter?: number;
    left_inv_motor_temp?: number;
    left_inv_igbt_temp?: number;
    left_inv_motor_rpm?: number;
    left_inv_num_max_trq?: number;
    left_inv_vcu_max_velocity?: number;
    left_inv_trq_actual?: number;
    left_inv_max_velocity?: number;
    left_inv_min_velocity?: number;
    left_inv_distance?: number;

    //Inverter Right
    right_inv_critical_hw_status?: number;
    right_inv_last_error?: number;
    right_inv_can_state?: number;
    right_inv_sys_status?: number;
    right_inv_handler_status?: number;
    right_inv_latched_error?: number;
    right_inv_actual_inverter_status?: number;
    right_inv_actual_control_mode?: number;
    right_inv_aux_hw_status?: number;
    right_inv_id_ref?: number;
    right_inv_iq_ref?: number;
    right_inv_id?: number;
    right_inv_iq?: number;
    right_inv_iq_ref_request?: number;
    right_inv_vdc_max?: number;
    right_inv_vdc?: number;
    right_inv_i1max?: number;
    right_inv_i2max?: number;
    right_inv_i3max?: number;
    right_inv_Imax?: number;
    right_inv_Imin?: number;
    right_inv_trq_ref?: number;
    right_inv_pwr_ref?: number;
    right_inv_pwr_actual?: number;
    right_inv_lim_speed_limiter?: number;
    right_inv_lim_power_limiter?: number;
    right_inv_lim_stall_limiter?: number;
    right_inv_lim_l2t_limiter?: number;
    right_inv_lim_motor_temp?: number;
    right_inv_lim_igbt_temp?: number;
    right_inv_motor_rpm?: number;
    right_inv_num_max_trq?: number;
    right_inv_vcu_max_velocity?: number;
    right_inv_motor_temp?: number;
    right_inv_igbt_temp?: number;
    right_inv_trq_actual?: number;
    right_inv_max_velocity?: number;
    right_inv_min_velocity?: number;
    right_inv_distance?: number;

    //VCU
    vcu_water_temp_in_right?: number;
    vcu_water_temp_out_right?: number;
    vcu_pc_flag?: number;
    vcu_r2d_flag?: number;
    vcu_watchdog_status?: number;
    vcu_bspdState?: number;
    vcu_fan_right?: number;
    vcu_fan_left?: number;
    vcu_pump_right?: number;
    vcu_pump_left?: number;
    vcu_gearbox_ntc_left?: number;
    vcu_apps1?: number;
    vcu_apps2?: number;
    vcu_brake_front?: number;
    vcu_brake_rear?: number;
    vcu_hall_fr?: number;
    vcu_hall_fl?: number;
    vcu_apps_right_implausibility?: number;
    vcu_apps_left_implausibility?: number;
    vcu_apps_deviation?: number;
    vcu_as_ready_delay_passed?: number;
    vcu_maxon_brake_enable?: number;
    vcu_res_k3_switch?: number;
    vcu_res_k2_switch?: number;
    vcu_res_estop?: number;
    vcu_res_radio_quality?: number;
    vcu_GE_right_dutyCycle?: number;
    vcu_GE_left_dutyCycle?: number;
    vcu_initial_check_state?: number;
    vcu_as_status?: number;
    vcu_dv_status?: number;
    vcu_node_status?: number;
    vcu_gearbox_ntc_right?: number;
    vcu_water_temp_in_left?: number;
    vcu_water_temp_out_left?: number;
    dash_power_limiter?: number;
    dash_traction_def?: number;
    vcu_accel_x?: number;
    vcu_accel_y?: number;
    vcu_accel_z?: number;
    vcu_gyro_x?: number;
    vcu_gyro_y?: number;
    vcu_gyro_z?: number;
    vcu_pc_temp?: number;
    vcu_lap_counter?: number;
    vcu_steering_target?: number;
    vcu_brake_target?: number;
    vcu_speed_target?: number;
    vcu_Vx?: number;
    vcu_Vy?: number;
    vcu_yaw_rate?: number;
    vcu_ax?: number;
    vcu_ay?: number;

    //Motor
    motor_requested_torque?: number;
    motor_actual_torque?: number;
    motor_rpm?: number;
    motor_temp_too_high?: number;
    motor_temp_limit_reached?: number;
    motor_temp?: number;

    //Radio
    radio_rssi?: number;
    radio_packet_loss?: number;
    radio_wrong_crc?: number;
    radio_kbps?: number;
    dv_R2D?: number;
};



//Εδώ ορίζουμε έναν τύπο δεδομένων με optional (?) όνομα, υποχρεωτικό label list που περιέχει είτε string
//είτε undefined και τέλος value list με αριθμούς optional
export type variableContainer = {
    containerName?: string,
    label: (string | undefined)[]; // Indexable type for label
    value?: (number)[]; // Indexable type for value
};

//Αντίστοιχα αλλά με τις αλλαγές που φαίνονται
export type sidebarItems = {
    label: (string)[];
    value?: (number)[];
    //lastNumber?: (number)[];
    // label2?: string;
    // value2?: number;
    // label3?: string;
    // value3?: number;
}

export type statusItems = {
    label: (string | undefined)[];
    value?: (number)[];
}

export type linechartItems = {
    variableName?: string;
    label?: string[];
    value?: number[];
}
