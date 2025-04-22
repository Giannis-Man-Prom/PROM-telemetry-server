/* Εδώ καθορίζουμε τα paths του router */
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

/* Εδώ κάνουμε import τα views μας */
import Live_Values from "../views/Live_Values.vue"
import VD_View from "../views/VD_View.vue"
import CustomCharts from "../views/CustomCharts.vue";
import csvreceiver from "../views/csvreceiver.vue";
import Debug from "../views/Debug.vue";
import NotFound from "../views/NotFound.vue"


/* Εδώ έχουμε την αντιστοιχία των paths του site και των views/components, μόνο τα παρακάτω χρησιμοποιούνται */
const routes: Array<RouteRecordRaw> = [
	{
		path: "/", /* Το default path μας δίνει το live telemetry */
		name: "Live_Values",
		component: Live_Values,
	},
	{
		path: "/vd/telemetry",
		name: "VD_View",
		component: VD_View, /* Το component που φορτώνεται όταν είμαστε στο παραπάνω link, βρίσκεται στο VD_View.vue */
	},
    {
        path: "/charts",
        name: "Charts",
        component: CustomCharts,
    },
	{
		path: "/vd-csv",
		name: "CSVReceiver",
		component: csvreceiver,
	},
	{
		path: "/Debug",
		name: "Debug",
		component: Debug,
	},
	{ 
		path: "/:pathMatch(.*)*", 
		name: "NotFound", 
		component: NotFound,
	}
]

/* Εδώ δημιουργούμε router */
const router = createRouter({
	history: createWebHistory(), /* Έτσι μπορούμε να κάνουμε navigate χωρίς να κάνουμε reload τη σελίδα */
	routes, /* Με τα παραπάνω routes που ορίσαμε */
})

export default router
