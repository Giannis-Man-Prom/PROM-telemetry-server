import axiosInstance from "../helpers/http-common.helper"
import {two_col_data} from "../types/vd-dash.types.ts";


export function get_two_collumns(): Promise<two_col_data []> {

	return axiosInstance
		.get("/")
		.then(response => response.data as two_col_data [])
		.catch(error => {
			console.error(error)
			throw error
		})
}
