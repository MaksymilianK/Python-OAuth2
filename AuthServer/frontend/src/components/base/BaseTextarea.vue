<template>
  <div class="container">
    <label class="input-container">
      <span class="label">{{ label }}</span>
      <textarea
          v-bind="$attrs"
          ref="input"
          class="input"
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
      ></textarea>
    </label>
  </div>
</template>

<script>
export default {
  name: 'BaseInput',
  props: {
    modelValue: {},
    label: String
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-flow: column;
  align-items: center;
}

.input-container {
  display: block;
}

.label {
  display: block;
  margin-left: 0.4rem;
  font-size: 0.9rem;
}

.input {
  min-width: 15rem;
  font-size: 1rem;
  background-color: inherit;
  border-radius: 0.4rem;
  padding: 0.72rem;
  border: 0.1rem solid #000;
  margin: 0.2rem 0 0 0;
  outline: none;
  position: relative;
  z-index: 1 !important;
}

.input:disabled {
  border-color: #4b4b4b;
  color: #4b4b4b;
}

.input:focus {
  border-color: #c04659;
}

.input:invalid {
  outline: none;
  box-shadow: none;
  border-color: #dd0000;
}
</style>