<template>
  <article>
    <h2 class="page-title">Home</h2>
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
    font-size: 1.5rem;
    text-align: center;
  }
</style>
