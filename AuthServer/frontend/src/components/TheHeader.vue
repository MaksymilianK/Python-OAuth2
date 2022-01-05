<template>
  <header class="header">
    <h1>MyAuth</h1>
    <ol class="menu">
      <li v-if="current"><button>Sign out</button></li>
      <li v-else><router-link to="/sign-in">Sign in</router-link></li>
      <li v-if="current"><router-link to="/add-client">Add client</router-link></li>
    </ol>
  </header>
</template>

<script>
import {authService} from "@/services/auth-service";

export default {
  name: "TheHeader",
  setup() {
    return {
      current: authService.current
    }
  }
}
</script>

<style scoped>
  .header {
    color: #eee;
    background-color: #2c3e50;
    padding: 1rem;
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