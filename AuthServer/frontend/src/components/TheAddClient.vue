<template>
  <article>
    <h2>Add client</h2>

    <form @submit="addClient">
      <label>
        Name
        <input type="text" v-model="name">
      </label>

      <label>
        Description
        <input type="textarea" v-model="description">
      </label>

      <label>
        Redirect URL
        <input type="textarea" v-model="redirectURL">
      </label>

      <button type="submit">Add client</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </article>
</template>

<script>
import {ref} from "vue";
import {HTTP_OK, HTTP_UNAUTHORIZED} from "@/http-status";
import {useRouter} from "vue-router";
import {userValidators} from "@/utils/user-validators";
import {ERROR_EMAIL_NOT_EXIST, ERROR_WRONG_PASSWORD} from "@/error-codes";
import {AddClientForm} from "@/models/add-client-form";
import {clientService} from "@/services/client-service";

export default {
  name: "TheAddClient",
  setup() {
    const router = useRouter();

    const formModel = new AddClientForm();
    const error = ref("");

    const validators = userValidators;

    function signIn(event) {
      event.preventDefault();

      error.value = validators.validateEmail(formModel.email.value);
      if (error.value) {
        return;
      }

      error.value = validators.validatePassword(formModel.password.value);
      if (error.value) {
        return;
      }

      clientService.add(formModel)
          .then(res => {
            console.log(res);
            switch (res.status) {
              case HTTP_OK:
                router.push("home");
                break;
              case HTTP_UNAUTHORIZED:
                if (res.body.detail === ERROR_EMAIL_NOT_EXIST) {
                  error.value = "Email does not exist!";
                } else if (res.body.detail === ERROR_WRONG_PASSWORD) {
                  error.value = "Wrong password!";
                } else {
                  error.value = "Unexpected error!";
                }
                break;
              default:
                error.value = "Unexpected error!";
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
      signIn
    }
  }
}
</script>

<style scoped>

</style>