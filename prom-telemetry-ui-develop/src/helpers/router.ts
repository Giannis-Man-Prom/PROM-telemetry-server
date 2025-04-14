/* Εδώ καθορίζουμε τα paths του router */
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

/* Εδώ κάνουμε import τα views μας */
import Dashboard from "../views/Dashboard_vd.vue"
import Dash_LiveTelemetry from "../views/Dash_LiveTelemetry.vue"

import ShowCustomCharts from "../views/ShowCustomCharts.vue";
import csvreceiver from "../components/csvreceiver.vue";


/* Εδώ έχουμε την αντιστοιχία των paths του site και των views */
const routes: Array<RouteRecordRaw> = [
	{
		path: "/vd/telemetry",
		name: "Dashboard",
		component: Dashboard, /* Το component που φορτώνεται όταν είμαστε στο παραπάνω link */
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

/* Εδώ δημιουργούμε router */
const router = createRouter({
	history: createWebHistory(), /* Έτσι μπορούμε να κάνουμε navigate χωρίς να κάνουμε reload τη σελίδα */
	routes, /* Με τα παραπάνω routes που ορίσαμε */
})

export default router
