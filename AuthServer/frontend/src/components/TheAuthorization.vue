<template>
  <article>
    <h2>Authorize</h2>

    <p v-if="error">{{ error }}</p>

    <section>
      <h3>Client {{ name }}</h3>
      <p>{{ description }}</p>
    </section>
    <section>
      <h3>Requested permissions</h3>
      <ul>
        <li v-for="scope of requestedScopes" :key="scope">{{ scopesDescriptions[scope] }}</li>
      </ul>
    </section>

    <button v-if="!error" @click="authorize">Authorize</button>
  </article>
</template>

<script>
import {ClientResponse} from "@/responses/client-response";
import {useRouter} from "vue-router";
import {HTTP_NOT_FOUND, HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {scopesDescriptions} from "@/utils/scopes-descriptions";
import {ref} from "vue";
import {clientService} from "@/services/client-service";
import {authService} from "@/services/auth-service";
import {AuthorizationRequest} from "@/requests/authorization-request";
import {userService} from "@/services/user-service";

export default {
  name: "TheAuthorization",
  setup() {
    const router = useRouter();
    const query = router.currentRoute.value.query;

    if (!userService.current.value) {
      router.push({name: "sign-in", query: query});
      return;
    }

    let client = new ClientResponse();

    const error = ref("");
    if (!query["client_id"]) {
      error.value = "Client id is empty!";
      return {error};
    } else if (!query["scope"]) {
      error.value = "Scope list is empty!";
      return {error};
    }

    const requestedScopes = query["scope"].split(",");

    clientService.get_client(query["client_id"])
        .then(res => {
          switch (res.status) {
            case HTTP_OK:
              client.setResponse(res.body);
              break;
            case HTTP_NOT_FOUND:
              error.value = "Client not found!";
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

    function authorize() {
      authService.authorize(new AuthorizationRequest(client.id.value, requestedScopes))
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                authService.redirectToClient(res.body.redirectUrl, res.body.code);
                break;
              case HTTP_NOT_FOUND:
                error.value = "Client not found!";
                break;
              case HTTP_UNAUTHORIZED:
                router.push({name: "sign-in"})
                break;
              default:
                console.log(res.status);
                error.value = "Unexpected HTTP status!";
                break;
            }
          })
    }

    return {
      ...client,
      requestedScopes,
      scopesDescriptions,
      error,
      authorize
    }
  }
}
</script>

<style scoped>

</style>