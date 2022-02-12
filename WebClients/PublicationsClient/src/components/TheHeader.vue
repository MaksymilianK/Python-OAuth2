<template>
  <header class="header">
    <h1>MyPublication</h1>
    <p v-if="current">{{ current }}</p>
    <ol class="menu">
      <li v-if="current"><button @click="signOut">Sign out</button></li>
      <li v-else><a :href="authorizationUrl">Sign in</a></li>
    </ol>
  </header>
</template>

<script>
import {authService} from "@/services/auth-service";
import {HTTP_NO_CONTENT} from "@/utils/http-status";
import {useRouter} from "vue-router";
import {authServerUrl, CLIENT_ID, REQUIRED_SCOPES} from "@/config";
import {Oauth2UrlBuilder} from "@/utils/oauth2-url-builder";

export default {
  name: "TheHeader",
  setup() {
    const router = useRouter();

    const authorizationUrl = (new Oauth2UrlBuilder())
        .addPathSegment(authServerUrl)
        .addPathSegment("authorization")
        .addClientIdParam(CLIENT_ID)
        .addScopeParam(REQUIRED_SCOPES)
        .build();

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
    background-color: #37682e;
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