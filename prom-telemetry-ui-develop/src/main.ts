import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import '@themesberg/flowbite';
import router from "./helpers/router"

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
    .component("font-awesome-icon", FontAwesomeIcon)
    .use(router)
    .mount('#app')
