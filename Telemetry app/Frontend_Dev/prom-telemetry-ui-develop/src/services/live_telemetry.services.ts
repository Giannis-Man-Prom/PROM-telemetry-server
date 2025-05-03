//Εδώ είναι η εντολή που δίνει το κουμπί του StartLogging για να κάνει Loggin το backend
import axiosInstance from "../helpers/http-common.helper.ts";

export function post_start_logging(): Promise<any> {

    const options = {
        data: {

        }
    }

    return axiosInstance
        //Το παρακάτω route βρίσκεται και στο app.py
        .post("live_telemetry/start_logging",options)
        .then(response => response.data)
        .catch(error => {
            console.error(error)
            throw error
        })
}
