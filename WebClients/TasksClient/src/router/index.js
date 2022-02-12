import { createRouter, createWebHistory } from 'vue-router'
import Home from "../views/Home";
import Auth from "../views/Auth";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/authorization',
        name: 'Auth',
        component: Auth
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router