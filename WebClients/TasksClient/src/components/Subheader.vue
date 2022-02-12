<template>
  <div class="subheader">
    <h2>{{ title }}</h2>
    <Button @click="$emit('toggle-add-task')" :text="showAddTask ? 'Close' : 'Add Task'" color="white" :background="showAddTask ? 'red' : 'green'" />
  </div>
</template>

<script>
import Button from "./Button";

export default {
  name: "Subheader",
  components: {
    Button
  },
  props: {
    title: String,
    showAddTask: Boolean
  }
}
</script>

<style scoped>
.subheader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  color: #2e4868;
  font-size: 1.5em;
}
</style>