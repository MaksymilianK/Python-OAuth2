import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import { authService } from "./services/auth-service";

authService.check_auth()
    .then(() => createApp(App).use(router).mount('#app'))
    .catch((e) => console.error(e));
