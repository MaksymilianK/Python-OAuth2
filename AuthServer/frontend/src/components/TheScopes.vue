<template>
  <article>
    <h2 class="page-title">Authorize</h2>

    <section class="section" v-for="sc of scopesAndClients" :key="sc[1].name">
      <h3 class="section-title">Client {{ sc[1].name }}</h3>
      <ul class="section-text">
        <li v-for="scope of sc[0].scope" :key="scope">{{ scopesDescriptions[scope] }}</li>
      </ul>
      <BaseButton @click="revokeScope(sc[1].id)"></BaseButton>
    </section>
  </article>
</template>

<script>
import {scopeService} from "@/services/scope-service";
import {HTTP_NO_CONTENT, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {useRouter} from "vue-router";
import BaseButton from "@/components/base/BaseButton";

export default {
  name: "TheScopes",
  components: {BaseButton},
  async setup() {
    const router = useRouter();

    const scopesAndClients = await scopeService.get_all();

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
      revokeScope
    }
  }
}
</script>

<style scoped>

</style>
