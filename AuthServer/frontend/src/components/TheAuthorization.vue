<template>
  <article>
    <h2 class="page-title">Authorize</h2>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="showPermissions" class="main">
      <section class="section">
        <h3 class="section-title">Client {{ name }}</h3>
        <p class="section-text">{{ description }}</p>
      </section>

      <section class="section" v-if="grantedPermissions.length !== 0">
        <h3 class="section-title">Already granted permissions</h3>
        <ul class="section-text">
          <li v-for="scope of grantedPermissions" :key="scope">{{ scopesDescriptions[scope] }}</li>
        </ul>
      </section>

      <section class="section">
        <h3 class="section-title">Requested permissions</h3>
        <ul class="section-text">
          <li v-for="scope of requestedPermissions" :key="scope">{{ scopesDescriptions[scope] }}</li>
        </ul>
      </section>

      <BaseButton v-if="!error" @click="authorize">Authorize</BaseButton>
      <BaseButton v-if="!error" @click="cancel" class="cancel-button">Cancel</BaseButton>
    </div>
  </article>
</template>

<script>
import {ClientResponse} from "@/responses/client-response";
import {useRouter} from "vue-router";
import {HTTP_NOT_FOUND, HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {scopesDescriptions} from "@/utils/scopes-descriptions";
import {reactive, ref} from "vue";
import {clientService} from "@/services/client-service";
import {authService} from "@/services/auth-service";
import {AuthorizationRequest} from "@/requests/authorization-request";
import {userService} from "@/services/user-service";
import BaseButton from "@/components/base/BaseButton";
import {scopeService} from "@/services/scope-service";

export default {
  name: "TheAuthorization",
  components: {BaseButton},
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

    const requestedPermissions = query["scope"].split(",");
    const grantedPermissions = reactive([]);

    const showPermissions = ref(false);

    scopeService.get_for_client(query["client_id"])
      .then(res => {
        switch (res.status) {
          case HTTP_OK:
            if (requestedPermissions.every(v => res.body.scope.includes(v))) {
              authorize();
              return;
            } else if (res.body.scope.length !== 0) {
              res.body.scope.forEach(s => grantedPermissions.push(s));
            }
            break
          default:
              console.log("Unexpected status: " + res.status);
        }
        showPermissions.value = true;
      });

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
      authService.authorize(new AuthorizationRequest(query["client_id"], requestedPermissions))
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
          });
    }

    function cancel() {
      authService.redirectToClient(client.redirectUrl.value, "");
    }

    return {
      ...client,
      requestedPermissions,
      scopesDescriptions,
      grantedPermissions,
      error,
      authorize,
      cancel,
      showPermissions
    }
  }
}
</script>

<style scoped>
  .main {
    display: flex;
    flex-flow: column;
    align-items: center;
    gap: 2rem;
  }

  .section-title {
    text-align: center;
    font-size: 1.5rem;
  }

  .section-text {
    font-size: 1.2rem;
    text-align: center;
  }

  .cancel-button {
    background-color: #4b4b4b;
  }

  .cancel-button:not(:disabled):hover, .cancel-button:not(:disabled):focus, .cancel-button:not(:disabled):active {
    background-color: #3a3a3a;
  }
</style>
