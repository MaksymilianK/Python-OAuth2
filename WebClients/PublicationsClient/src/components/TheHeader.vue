<template>
  <header class="header">
    <h1>MyPublications</h1>
    <p v-if="current">{{ current }}</p>
    <ol class="menu">
      <li v-if="current"><BaseButton @click="signOut">Sign out</BaseButton></li>
      <li v-else><BaseButton :href="authorizationUrl">Sign in</BaseButton></li>
    </ol>
  </header>
</template>

<script>
import {authService} from "@/services/auth-service";
import {HTTP_NO_CONTENT} from "@/utils/http-status";
import {useRouter} from "vue-router";
import BaseButton from "@/components/BaseButton";

export default {
  name: "TheHeader",
  components: {BaseButton},
  setup() {
    const router = useRouter();

    const authorizationUrl = authService.getAuthUrl();

    function signOut() {
      authService.revokeToken()
          .then(res => {
            switch (res.status) {
              case HTTP_NO_CONTENT:
                router.push({name: "home"});
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
  .header {
    color: #eee;
    background-color: #a62828;
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