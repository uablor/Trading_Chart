<template>

<button
        class="buy-button"
        :class="{ disabled: is_button_enter }"
        :disabled="is_button_enter"
        @click="queueTrade('buy', 'BTCUSDT')"
      >
        BUY
      </button>

    <div class="countdown">{{ nextCandlestickTime }}</div>

   <button
        class="sell-button"
        :class="{ disabled: is_button_enter }"
        :disabled="is_button_enter"
        @click="queueTrade('sell', 'BTCUSDT')"
      >
        SELL
      </button>
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
      console.log('Received data:', data.is_button_enter);
      if (data.next_candlestick_time) {
        nextCandlestickTime.value = data.next_candlestick_time;
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
    background-color: #333333;
    color: white;
    padding: 14px 8px 8px 8px;
    border-radius: 8px;
    font-weight: bold;
  }
  .buy-button,
.sell-button {
  width: 100%;
  padding: 12px 0;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.3s ease;
}

.buy-button {
  background-color: #2ecc71;
  border: none;
  color: white;
}

.buy-button:hover {
  background-color: #27ae60;
  transform: scale(1.02);
}

.sell-button {
  background-color: #e74c3c;
  border: none;
  color: white;
}


.sell-button:hover {
  background-color: #c0392b;
  transform: scale(1.02);
}

.buy-button.disabled,
.sell-button.disabled {
  background-color: #95a5a6 !important;
  /* Grey color when disabled */
  cursor: not-allowed;
}
  </style>
  