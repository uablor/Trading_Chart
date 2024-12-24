<template>
  <div class="countdown">{{ nextCandlestickTime }}</div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const nextCandlestickTime = ref('Loading...');

// WebSocket connection URL (replace with your actual WebSocket URL)
const socketUrl = 'ws://127.0.0.1:9000/ws/candlestick/';

// WebSocket instance
let socket = null;

onMounted(() => {
  // Initialize the WebSocket connection
  socket = new WebSocket(socketUrl);

  // When the connection is established, send a request for the next candlestick time
  socket.onopen = () => {
    console.log('WebSocket connected');
    socket.send(JSON.stringify({ request_next_candlestick_time: true }));
  };

  // Handle incoming messages
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.next_candlestick_time) {
      nextCandlestickTime.value = data.next_candlestick_time;
      console.log("is button start", data.is_button_enter);
    }
  };

  // Handle WebSocket errors
  socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };

  // Handle WebSocket close
  socket.onclose = () => {
    console.log('WebSocket closed');
  };
});

onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<style scoped>
.countdown {
  width: 100%;
  height: 50px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  background-color: #333333;
  color: white;
  padding: 10px 8px 8px 8px;
  border-radius: 8px;
  font-weight: bold;
}
</style>
