import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from "vue-router";
import {routes} from "./routes";
import {userService} from "@/services/user-service";

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

userService.get_current()
    .then(() => createApp(App).use(router).mount('#app'))
    .catch((e) => console.error(e));