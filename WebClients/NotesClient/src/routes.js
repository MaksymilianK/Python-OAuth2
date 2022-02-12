import TheHome from "@/components/TheHome";
import TheAuthorization from "@/components/TheAuthorization";

export const routes = [
  {
    path: '/',
    name: 'home',
    component: TheHome
  },
  {
    path: '/authorization',
    name: 'auth',
    component: TheAuthorization
  },

]
