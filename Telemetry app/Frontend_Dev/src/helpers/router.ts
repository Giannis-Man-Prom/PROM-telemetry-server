/* Εδώ καθορίζουμε τα paths του router */
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

/* Εδώ κάνουμε import τα views μας */
import Live_Values from "../views/Live_Values.vue"
import VD_View from "../views/VD_View.vue"
import AccuView from "../views/AccuView.vue"
import InvView from "../views/InvView.vue"
import SensorsView from "../views/SensorsView.vue"
import VcuView from "../views/VcuView.vue"
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
		path: "/accuview", /* Το default path μας δίνει το live telemetry */
		name: "AccuView",
		component: AccuView,
	},
	{
		path: "/invview", /* Το default path μας δίνει το live telemetry */
		name: "iInvView",
		component: InvView,
	},
	{
		path: "/sensorsview", /* Το default path μας δίνει το live telemetry */
		name: "SensorsView",
		component: SensorsView,
	},
	{
		path: "/vcuview", /* Το default path μας δίνει το live telemetry */
		name: "VcuView",
		component: VcuView,
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
