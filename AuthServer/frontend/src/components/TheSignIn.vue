<template>
  <article>
    <h2 class="page-title">Sign in</h2>

    <form @submit="signIn" class="form">
      <BaseInput type="email" label="Email" placeholder="example@example.com" v-model="email"></BaseInput>
      <BaseInput type="password" label="Password" v-model="password"></BaseInput>

      <BaseButton type="submit">Sign in</BaseButton>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
  </article>
</template>

<script>
import {SignInForm} from "@/models/sign-in-form";
import {ref} from "vue";
import {userService} from "@/services/user-service";
import {HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {useRouter} from "vue-router";
import {userValidators} from "@/utils/user-validators";
import {ERROR_EMAIL_NOT_EXIST, ERROR_WRONG_PASSWORD} from "@/utils/error-codes";
import BaseInput from "@/components/base/BaseInput";
import BaseButton from "@/components/base/BaseButton";

export default {
  name: "TheSignIn",
  components: {BaseInput, BaseButton},
  setup() {
    const router = useRouter();
    if (userService.current.value) {
      router.push({name: "home"});
      return;
    }

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

      userService.signIn(formModel)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                if (router.currentRoute.value.query.client_id) {
                  router.go(-1);
                } else {
                  router.push({name: "home"});
                }
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