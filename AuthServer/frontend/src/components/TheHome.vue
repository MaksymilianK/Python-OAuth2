<template>
  <article>
    <h2>Home</h2>
    <p v-if="current" class="login-status">
      Status: zalogowany
    </p>
    <p v-else class="login-status">
      Status: niezalogowany
    </p>
  </article>
</template>

<script>
import {userService} from "@/services/user-service";

export default {
  name: 'TheHome',
  setup() {
    return {
      current: userService.current
    }
  }
}
</script>

<style scoped>
  .login-status {
    text-align: center;
  }
</style>
