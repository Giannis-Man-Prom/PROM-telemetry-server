import {VehicleTelemetry_data} from "./live_telemetry.ts";

export type event_connection_res = {
  'status': string,
  'msg'?: string // In case of an unsuccessful connection we are returning also the exception error
}

export type api_res = {
  'data': VehicleTelemetry_data // In case of an unsuccessful connection we are returning also the exception error
}
