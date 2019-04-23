<template>
  <div class="switch-flow">
    <h3>My future CMPE210 project</h3>
    <v-container fluid>
      <v-sparkline
        :value="value"
        :gradient="gradient"
        :smooth="radius || false"
        :padding="padding"
        :line-width="width"
        :stroke-linecap="lineCap"
        :gradient-direction="gradientDirection"
        auto-draw
      ></v-sparkline>
    </v-container>
    <button @click="generateData">Add</button>
  </div>
</template>

<script>
const gradients = [
  ['#222'],
  ['#42b3f4'],
  ['red', 'orange', 'yellow'],
  ['purple', 'violet'],
  ['#00c6ff', '#F0F', '#FF0'],
  ['#f72047', '#ffd200', '#1feaea']
]

export default {
  name: 'switch-flow',
  data: function() {
    return {
      width: 2,
      radius: 10,
      padding: 8,
      lineCap: 'round',
      gradient: gradients[5],
      value: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
      gradientDirection: 'top',
      gradients
    }
  },
  methods: {
    appendData: function(num) {
      this.value.push(num)
      this.value.shift()
    },
    generateData: function() {
      var func = this.appendData;
      setInterval(function() {
        var randNum = Math.random(0, 10) * 10;
        func(randNum);
      }, 1000)
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
