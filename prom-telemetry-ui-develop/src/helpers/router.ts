import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

import Dashboard from "../views/Dashboard_vd.vue"
import Dash_LiveTelemetry from "../views/Dash_LiveTelemetry.vue"

import ShowCustomCharts from "../views/ShowCustomCharts.vue";
import csvreceiver from "../components/csvreceiver.vue";



const routes: Array<RouteRecordRaw> = [
	{
		path: "/vd/telemetry",
		name: "Dashboard",
		component: Dashboard,
	},
		{
		path: "/",
		name: "Dash_LiveTelemetry",
		component: Dash_LiveTelemetry,
	},
    {
        path: "/charts",
        name: "Charts",
        component: ShowCustomCharts,
    },
	{
		path: "/vd-csv",
		name: "CSVReceiver",
		component: csvreceiver,
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

export default router
