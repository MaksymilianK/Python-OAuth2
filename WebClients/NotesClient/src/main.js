import { createApp } from 'vue'
import App from './App.vue'
import {routes} from "./routes";
import {createRouter, createWebHistory} from "vue-router";
import {authService} from "./services/auth-service";

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

authService.check_auth()
    .then(() => createApp(App).use(router).mount('#app'))
    .catch((e) => console.error(e));
