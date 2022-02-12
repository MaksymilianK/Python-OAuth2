<template>
  <article>
    <h2>Authorizing...</h2>
    <p v-if="error">{{ error }}</p>
  </article>
</template>

<script>
import { useRouter } from "vue-router";
import { HTTP_OK, HTTP_UNAUTHORIZED } from "../utils/http-status";
import { ref } from "vue";
import { authService } from "../services/auth-service";

export default {
  name: "Auth",

  setup() {
    const router = useRouter();
    const code = router.currentRoute.value.query["code"];
    const error = ref("");
    if (!code) {
      error.value = "Missing auth code!";
      return {error};
    }

    authService.get_token(code)
        .then(res => {
          switch (res.status) {
            case HTTP_OK:
              router.push({name: "Home"});
              break;
            case HTTP_UNAUTHORIZED:
              error.value = "Code expired!";
              break;
            default:
              console.log(res.status);
              error.value = "Unexpected HTTP status!";
              break;
          }
        })
        .catch(err => {
          console.log(err);
          error.value = "Connection error!";
        });

    return {
      error
    }
  }
}
</script>

<style scoped>
article {
  margin: 30px auto;
  padding: 30px;
}
</style>