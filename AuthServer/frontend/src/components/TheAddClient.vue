<template>
  <article>
    <h2 class="page-title">Add client</h2>

    <form @submit="addClient" class="form">
      <BaseInput type="text" label="Name" placeholder="Example_name" v-model="name"></BaseInput>
      <BaseTextarea v-model="description" label="Description"></BaseTextarea>
      <BaseInput type="text" label="Redirect URL" placeholder="http://host/path" v-model="redirectUrl"></BaseInput>

      <BaseButton type="submit">Add client</BaseButton>
    </form>

    <p v-if="error" class="error">{{ error }}</p>

    <p v-if="clientId" class="client-id">Client ID: {{ clientId }}</p>
  </article>
</template>

<script>
import {ref} from "vue";
import {HTTP_CONFLICT, HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {ERROR_CLIENT_NAME_EXISTS, ERROR_CLIENT_REDIRECT_URL_EXISTS} from "@/utils/error-codes";
import {AddClientForm} from "@/models/add-client-form";
import {clientService} from "@/services/client-service";
import {clientValidators} from "@/utils/client-validators";
import BaseInput from "@/components/base/BaseInput";
import BaseTextarea from "@/components/base/BaseTextarea";
import BaseButton from "@/components/base/BaseButton";

export default {
  name: "TheAddClient",
  components: {BaseInput, BaseTextarea, BaseButton},
  setup() {
    const formModel = new AddClientForm();
    const error = ref("");

    const clientId = ref(null);

    const validators = clientValidators;

    function addClient(event) {
      event.preventDefault();

      error.value = validators.validateName(formModel.name.value);
      if (error.value) {
        return;
      }

      error.value = validators.validateDescription(formModel.description.value);
      if (error.value) {
        return;
      }

      error.value = validators.validateRedirectURL(formModel.redirectUrl.value);
      if (error.value) {
        return;
      }

      clientService.add(formModel)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                error.value = "";
                clientId.value = res.body.id
                break;
              case HTTP_UNAUTHORIZED:
                error.value = "Unauthorized! Sign in first!";
                break;
              case HTTP_CONFLICT:
                if (res.body.detail === ERROR_CLIENT_NAME_EXISTS) {
                  error.value = "Client name already exists!";
                } else if (res.body.detail === ERROR_CLIENT_REDIRECT_URL_EXISTS) {
                  error.value = "Client's redirect URL already exists!";
                } else {
                  error.value = "Unexpected error!";
                }
                break;
              default:
                error.value = "Unexpected code", res.body.detail;
                break;
            }
          })
          .catch(err => {
            console.log(err);
            error.value = "Connection error!";
          });
    }

    return {
      ...formModel,
      error,
      clientId,
      addClient
    }
  }
}
</script>

<style scoped>
  .client-id {
    text-align: center;
    font-size: 2rem;
    margin-top: 2rem;
  }
</style>