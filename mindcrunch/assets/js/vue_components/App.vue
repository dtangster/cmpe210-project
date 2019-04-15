<template>
  <div id="app">
    <header>
      <h1>Mindcrunch</h1>
    </header>
    <main>
      <switch-flow></switch-flow>
    </main>
  </div>
</template>

<script>
import SwitchFlow from './SwitchFlow.vue'

export default {
    name: 'app',
    components: {
        SwitchFlow
    }
}
</script>

<style>
#app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      color: #2c3e50;
}
main {
    margin-top: 60px;
}
</style>
