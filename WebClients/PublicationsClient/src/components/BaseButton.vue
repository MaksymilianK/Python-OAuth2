<template>
  <router-link v-if="to" :to="to" class="button">
    <span v-if="icon" class="material-icons icon">{{ icon }}</span>
    <slot></slot>
  </router-link>
  <a v-else-if="href" :href="href" class="button">
    <span v-if="icon" class="material-icons icon">{{ icon }}</span>
    <slot></slot>
  </a>
  <button v-else class="button">
    <span v-if="icon" class="material-icons icon">{{ icon }}</span>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "BaseButton",
  props: {
    to: {
      type: String,
      default: ''
    },
    href: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.button {
  white-space: nowrap;
  width: min-content;
  text-transform: uppercase;
  color: #e2e2e2;
  display: block;
  padding: 1.1rem 1.5rem;
  background-color: #525252;
  border-radius: 0.5rem;
  box-shadow: 0 0 5px 2px rgba(0,0,0,0.75);
  transition-duration: 0.3s;
  text-decoration: none;
  outline: none;
  border: none;
  cursor: pointer;
  font-size: inherit;
  line-height: 1rem;
}

.button:disabled {
  background-color: #d07c8c;
  cursor: inherit;
}

.button:not(:disabled):hover, .button:not(:disabled):focus, .button:not(:disabled):active {
  background-color: #383838;
  box-shadow: 0 0 5px 1px rgba(0,0,0,0.75);
}

.icon {
  height: 0;
  transform: translate(-0.1em, -0.53em);
  font-size: 1.7em;
  vertical-align: middle;
}
</style>
