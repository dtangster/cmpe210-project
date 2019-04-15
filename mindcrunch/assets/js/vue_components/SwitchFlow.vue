<template>
  <div class="switch-flow">
    <h3>Hello from Vue.js!</h3>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
export default {
  name: 'switch-flow',
  data() {
    return {
      msg: 'Simple example using Phoenix, Vue and Webpack.'
    }
  }
}
</script>

<style scoped>
.switch-flow {
  padding: 15px;
  background-color: #eaeaea;
}

p {
  margin-top: 40px;
}
</style>
