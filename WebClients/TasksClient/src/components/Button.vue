<template>
  <button :style="{ background: background, color: color }" class="btn">{{ text }}</button>
</template>

<script>
export default {
  name: "Button",
  props: {
    text: String,
    color: String,
    background: String
  }
}
</script>

<style scoped>

</style>