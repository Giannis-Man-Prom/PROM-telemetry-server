import {VehicleTelemetry_data} from "./live_telemetry.ts";

//Ορίζουμε τα μηνύματα που θα χρησιμοποιήσουμε για το communication
export type event_connection_res = {
  'status': string,
  'msg'?: string // In case of an unsuccessful connection we are returning also the exception error
}

//Στο App.vue θα είναι το response που θα είναι τύπου VehicleTelemetry_data
export type api_res = {
  'data': VehicleTelemetry_data // In case of an unsuccessful connection we are returning also the exception error
}
