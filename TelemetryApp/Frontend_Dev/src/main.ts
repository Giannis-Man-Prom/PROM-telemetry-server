/* Το create app ξεκινάει την εφαρμογή μας, αργότερα κάνουμε το createApp(App) */
import { createApp } from 'vue'
/* Κάνουμε import το style της css */
import './style.css'
/* Κάνουμε import το component για να το χτίσουμε παρακάτω */
import App from './App.vue'

import router from "./helpers/router"

createApp(App)
    .use(router) /* Προσθέτουμε Vue router στην εφαρμογή από το router.ts */
    .mount('#app') /* Το στέλνουμε στο index.html για να εγκατασταθεί */
