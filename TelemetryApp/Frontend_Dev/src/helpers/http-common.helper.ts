//Αυτό το σημείο είναι υπεύθυνο για να μπορούμε να κάνουμε http requests με το backend
//Στο App.py αντίστοιχα έχουμε cors στο http://localhost:8081/api/v1

import axios, { AxiosInstance } from "axios"

const instance: AxiosInstance = axios.create({
	baseURL: "http://localhost:8081/api/v1",
	headers: {
		"Content-type": "application/json",
	}
})

instance.interceptors.response.use(
	response => response.data,
	error => {
		console.error(error)
		throw error
	}
)

export default instance
