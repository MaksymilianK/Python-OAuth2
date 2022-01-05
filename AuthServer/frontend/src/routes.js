import TheHome from "@/components/TheHome";
import TheSignUp from "@/components/TheSignUp";
import TheSignIn from "@/components/TheSignIn";
import TheAddClient from "@/components/TheAddClient";

export const routes = [
  {
    path: '/',
    name: 'home',
    component: TheHome
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: TheSignUp
  },
  {
    path: '/sign-in',
    name: 'sign-in',
    component: TheSignIn
  },
  {
    path: '/add-client',
    name: 'add-client',
    component: TheAddClient
  }
]
