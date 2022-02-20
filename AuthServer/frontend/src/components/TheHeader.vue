<template>
  <header class="header">
    <h1><router-link to="/">MyAuth</router-link></h1>
    <div v-if="current" class="user-container">
      <img alt="" src="@/assets/user.svg" class="user-img">
      <p v-if="current" class="user-text">{{ current }}</p>
    </div>
    <ol class="menu">
      <li v-if="current"><BaseButton @click="signOut">Sign out</BaseButton></li>
      <template v-else>
        <li><BaseButton to="sign-in">Sign in</BaseButton></li>
        <li><BaseButton to="sign-up">Sign up</BaseButton></li>
      </template>
      <li v-if="current"><BaseButton to="add-client">Add client</BaseButton></li>
      <li v-if="current"><BaseButton to="scopes">Authorized clients</BaseButton></li>
    </ol>
  </header>
</template>

<script>
import {userService} from "@/services/user-service";
import {HTTP_NO_CONTENT} from "@/utils/http-status";
import {useRouter} from "vue-router";
import BaseButton from "@/components/base/BaseButton";

export default {
  name: "TheHeader",
  components: {BaseButton},
  setup() {
    const router = useRouter();

    function signOut() {
      userService.signOut()
          .then(res => {
            switch (res.status) {
              case HTTP_NO_CONTENT:
                router.push({name: "home"});
                break;
              default:
                console.log("Unexpected status!", res.status);
                break;
            }
          })
          .catch(err => {
            console.log(err);
          });
    }

    return {
      current: userService.current,
      signOut
    }
  }
}
</script>

<style scoped>
  .user-container {
    display: flex;
    gap: 1rem;
    font-size: 1.4rem;
  }

  .header {
    color: #eee;
    background-color: #472c50;
    padding: 0.5rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .menu {
    list-style: none;
    display: flex;
    gap: 1rem;
  }
</style>
