<template>
  <article>
    <h2>Sign up</h2>

    <form @submit="signUp">
      <label>
        Nick
        <input type="text" v-model="nick">
      </label>

      <label>
        Email
        <input type="email" v-model="email">
      </label>

      <label>
        Password
        <input type="password" v-model="password">
      </label>

      <label>
        Repeat password
        <input type="password" v-model="repeatPassword">
      </label>

      <button type="submit">Sign up</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </article>
</template>

<script>
import {ref} from "vue";
import {userService} from "@/services/user-service";
import {HTTP_CONFLICT, HTTP_OK} from "@/utils/http-status";
import {useRouter} from "vue-router";
import {SignUpForm} from "@/models/sign-up-form";
import {userValidators} from "@/utils/user-validators";
import {ERROR_EMAIL_EXISTS, ERROR_NICK_EXISTS} from "@/utils/error-codes";

export default {
  name: "TheSignUp",
  setup() {
    const router = useRouter();
    if (userService.current.value) {
      router.push({name: "home"});
      return;
    }

    const formModel = new SignUpForm();
    const error = ref("");

    const validators = userValidators;

    function signUp(event) {
      event.preventDefault();

      error.value = validators.validateNick(formModel.nick.value);
      if (error.value) {
        return;
      }

      error.value = validators.validateEmail(formModel.email.value);
      if (error.value) {
        return;
      }

      error.value = validators.validatePassword(formModel.password.value);
      if (error.value) {
        return;
      }

      error.value = validators.validatePasswordsMatch(formModel.password.value, formModel.repeatPassword.value);
      if (error.value) {
        return;
      }

      userService.signUp(formModel)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                if (router.currentRoute.value.query["client_id"]) {
                  router.go(-1);
                } else {
                  router.push({name: "home"});
                }
                break;
              case HTTP_CONFLICT:
                if (res.body.detail === ERROR_EMAIL_EXISTS) {
                  error.value = "Email already exists!";
                } else if (res.body.detail === ERROR_NICK_EXISTS) {
                  error.value = "Nick already exists!";
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
      signUp
    }
  }
}
</script>

<style scoped>

</style>