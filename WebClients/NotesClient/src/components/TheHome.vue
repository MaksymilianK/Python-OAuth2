<template>
  <article>
    <p v-if="current" class="login-status">
      Status: zalogowany
    </p>
    <p v-else class="login-status">
      Status: niezalogowany
    </p>
  </article>
  <template v-if="current">
    <TheNote />
  </template>
</template>

<script>
import {authService} from "@/services/auth-service";
import TheNote from "./TheNote.vue"

export default {
  name: 'TheHome',
  setup() {
    return {
      current: authService.current
    }
  },
  components: {
    TheNote
  }
}
</script>

<style scoped>
  .login-status {
    text-align: center;
  }
</style>
