<template>
  <header class="header">
    <h1>MyAuth</h1>
    <ol class="menu">
      <li v-if="current"><button @click="signOut">Sign out</button></li>
      <template v-else>
        <li><router-link to="sign-in">Sign in</router-link></li>
        <li><router-link to="sign-up">Sign up</router-link></li>
      </template>
      <li v-if="current"><router-link to="add-client">Add client</router-link></li>
    </ol>
  </header>
</template>

<script>
import {authService} from "@/services/auth-service";
import {HTTP_NO_CONTENT} from "@/http-status";
import {useRouter} from "vue-router";

export default {
  name: "TheHeader",
  setup() {
    const router = useRouter();

    function signOut() {
      authService.signOut()
          .then(res => {
            switch (res.status) {
              case HTTP_NO_CONTENT:
                router.push("home");
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
      signOut
    }
  }
}
</script>

<style scoped>
  .header {
    color: #eee;
    background-color: #2c3e50;
    padding: 1rem;
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