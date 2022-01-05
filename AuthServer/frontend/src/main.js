import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from "vue-router";
import {routes} from "./routes";
import {authService} from "@/services/auth-service";

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

authService.get_current()
    .then(() => createApp(App).use(router).mount('#app'))
    .catch(() => document.write("Connection error!"));
