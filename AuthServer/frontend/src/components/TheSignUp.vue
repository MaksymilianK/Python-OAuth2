<template>
  <article>
    <h2 class="page-title">Sign up</h2>

    <form @submit="signUp" class="form">
      <BaseInput type="text" label="Nick" v-model="nick"></BaseInput>
      <BaseInput type="email" label="Email" v-model="email"></BaseInput>
      <BaseInput type="password" label="Password" v-model="password"></BaseInput>
      <BaseInput type="password" label="Repeat password" v-model="repeatPassword"></BaseInput>

      <BaseButton type="submit">Sign up</BaseButton>
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
import BaseButton from "@/components/base/BaseButton";
import BaseInput from "@/components/base/BaseInput";

export default {
  name: "TheSignUp",
  components: {BaseInput, BaseButton},
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