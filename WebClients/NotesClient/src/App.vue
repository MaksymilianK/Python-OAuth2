<template>
  <TheHeader></TheHeader>
  <main>
    <router-view/>
  </main>
</template>

<script>
import TheHeader from "@/components/TheHeader";

export default {
  components: {TheHeader}
}
</script>

<style scoped>
</style>
