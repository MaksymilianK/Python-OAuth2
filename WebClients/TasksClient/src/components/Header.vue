<template>
  <header>
    <h1>{{ title }}</h1>
    <p v-if="current">{{ current }}</p>
    <ol class="menu">
      <li v-if="current"><Button @click="signOut" text="Sign out" color="black" background="white" /></li>
      <li v-else><a :href="authorizationUrl"><Button text="Sign in" color="black" background="white" /></a></li>
    </ol>
  </header>
</template>

<script>
import Button from "./Button";
import { authService } from "../services/auth-service";
import { HTTP_NO_CONTENT } from "../utils/http-status";
import { useRouter } from "vue-router";


export default {
  name: "Header",
  components: {
    Button
  },
  props: {
    title: String
  },
  setup() {
    const router = useRouter();

    const authorizationUrl = authService.getAuthUrl();

    function signOut() {
      authService.revokeToken()
          .then(res => {
            switch (res.status) {
              case HTTP_NO_CONTENT:
                router.push({name: "Home"});
                break;
              default:
                console.log("Unexpected status!", res.status);
                break;
            }
          })
          .catch(err => {
            console.log(err);
          });
    }

    return {
      current: authService.current,
      signOut,
      authorizationUrl
    }
  }
}
</script>

<style scoped>
header {
  color: #eee;
  background-color: #2e4868;
  padding: 1.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu {
  list-style: none;
  display: flex;
  gap: 1rem;
}
</style>