<template>
  <article>
    <h2>Sign in</h2>

    <form @submit="signIn">
      <label>
        Email
        <input type="email" v-model="email">
      </label>

      <label>
        Password
        <input type="password" v-model="password">
      </label>

      <button type="submit">Sign in</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </article>
</template>

<script>
import {SignInForm} from "@/models/sign-in-form";
import {ref} from "vue";
import {authService} from "@/services/auth-service";
import {HTTP_OK, HTTP_UNAUTHORIZED} from "@/http-status";
import {useRouter} from "vue-router";
import {userValidators} from "@/utils/user-validators";
import {ERROR_EMAIL_NOT_EXIST, ERROR_WRONG_PASSWORD} from "@/error-codes";

export default {
  name: "TheSignIn",
  setup() {
    const router = useRouter();

    const formModel = new SignInForm();
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

      authService.signIn(formModel)
          .then(res => {
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