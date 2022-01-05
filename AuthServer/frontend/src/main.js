import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from "vue-router";
import {routes} from "./routes";

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

createApp(App).use(router).mount('#app')
