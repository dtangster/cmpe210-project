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
    <button @click="clear">Clear</button>
  </div>
</template>

<script>
import socket from '../socket'

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
  mounted: function() {
    var appendData = this.appendData;
    let channel = socket.channel("room:lobby", {})
    channel.on('traffic', function(payload) {
	  appendData(payload.bytes_tx)
    })
  },
  data: function() {
    return {
      width: 2,
      radius: 10,
      padding: 8,
      lineCap: 'round',
      gradient: gradients[5],
      value: new Array(60).fill(0),
      gradientDirection: 'top',
      gradients,
      last_value: 0
    }
  },
  methods: {
    appendData: function(num) {
      if (num == null) {
        return
      }
      let bytes_tx = num - this.last_value
      if (bytes_tx < 0) {
        console.log("Bytes transferred: ", num)
        this.value.push(num)
	  } else {
        console.log("Bytes transferred: ", bytes_tx)
        this.value.push(bytes_tx)
	  }
      this.last_value = num
      this.value.push(bytes_tx)
      this.value.shift()
    },
    generateData: function() {
      let appendData = this.appendData;
      setInterval(function() {
        var randNum = Math.random(0, 10) * 10;
        appendData(randNum);
      }, 1000)
    },
    clear: function() {
      console.log("Clearing chart")
      this.value.fill(0)
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
