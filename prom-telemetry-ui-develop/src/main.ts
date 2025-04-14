/* Το create app ξεκινάει την εφαρμογή μας, αργότερα κάνουμε το createApp(App) */
import { createApp } from 'vue'
/* Κάνουμε import το style της css */
import './style.css'
/* Κάνουμε import το component για να το χτίσουμε παρακάτω */
import App from './App.vue'

import '@themesberg/flowbite';
import router from "./helpers/router"

/* Κάνουμε import random πραγματάκια */
import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"

import {
    faGithub,
    faInstagram,
    faLinkedin,
    faTwitter,
    faYoutube
} from "@fortawesome/free-brands-svg-icons"

import {
    faChevronUp,
    faChevronDown,
    faGauge
} from "@fortawesome/free-solid-svg-icons"

library.add(
    faGithub,
    faInstagram,
    faLinkedin,
    faTwitter,
    faYoutube,
    faChevronDown,
    faChevronUp,
    faGauge
)

createApp(App)
    .component("font-awesome-icon", FontAwesomeIcon) /* Προσθέτουμε τα icons για να χρησιμοποιηθούν */
    .use(router) /* Προσθέτουμε Vue router στην εφαρμογή από το router.ts */
    .mount('#app') /* Το στέλνουμε στο index.html για να εγκατασταθεί */
