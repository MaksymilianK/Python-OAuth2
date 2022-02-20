<template>
  <article>
    <h2 class="page-title">Authorized clients</h2>

    <div class="main">
      <section class="section" v-for="sc of scopesAndClients" :key="sc[1].name">
        <h3 class="section-title">Client {{ sc[1].name }}</h3>
        <ul v-if="sc[0].scope.length > 0" class="section-text">
          <li v-for="scope of sc[0].scope" :key="scope">{{ scopesDescriptions[scope] }}</li>
        </ul>
        <BaseButton v-if="sc[0].scope.length > 0" @click="revokeScope(sc[1].id)">Unauthorize</BaseButton>
        <p v-else>No granted permissions</p>
      </section>
    </div>
  </article>
</template>

<script>
import {scopeService} from "@/services/scope-service";
import {HTTP_NO_CONTENT, HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {useRouter} from "vue-router";
import BaseButton from "@/components/base/BaseButton";
import {reactive} from "vue";
import {scopesDescriptions} from "@/utils/scopes-descriptions";

export default {
  name: "TheScopes",
  components: {BaseButton},
  setup() {
    const router = useRouter();

    const scopesAndClients = reactive([]);
    scopeService.get_all()
        .then(res => {
          switch (res.status) {
            case HTTP_OK:
              res.body.scopes.forEach(sc => {
                scopesAndClients.push(sc);
              })
              break;
            case HTTP_UNAUTHORIZED:
              router.push({name: "sign-in"})
              break;
            default:
              console.log("Unknown status " + res.status);
              break;
          }
        });

    function revokeScope(clientId) {
      scopeService.revoke_for_client(clientId)
        .then(res => {
          switch (res.status) {
            case HTTP_NO_CONTENT:
              removeClient(clientId);
              break;
            case HTTP_UNAUTHORIZED:
              router.push({name: "sign-in"})
              break;
            default:
              console.log("Unknown status: " + res.status);
          }
        });
    }

    function removeClient(clientId) {
      const index = scopesAndClients.findIndex(sc => sc[1].id === clientId);
      scopesAndClients.splice(index, 1);
    }

    return {
      scopesAndClients,
      revokeScope,
      scopesDescriptions
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

.section {
  display: flex;
  flex-flow: column;
  align-items: center;
}
</style>
