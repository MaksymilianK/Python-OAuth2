import { createApp } from 'vue'
import App from './App.vue'
import {routes} from "./routes";
import {createRouter, createWebHistory} from "vue-router";

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

createApp(App).use(router).mount('#app');
