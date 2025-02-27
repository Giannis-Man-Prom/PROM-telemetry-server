import axiosInstance from "../helpers/http-common.helper.ts";

export function post_start_logging(): Promise<any> {

    const options = {
        data: {

        }
    }

    return axiosInstance
        .post("live_telemetry/start_logging",options)
        .then(response => response.data)
        .catch(error => {
            console.error(error)
            throw error
        })
}
