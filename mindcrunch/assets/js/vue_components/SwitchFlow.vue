<template>
  <div class="switch-flow">
    <h3>My future CMPE210 project</h3>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
export default {
  name: 'switch-flow',
  data() {
    return {
      msg: 'This will eventually show my Switch OpenFlows'
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
