<template>
  <div class="chart-container">
    <p v-if="reconnectAttempts > 0 && reconnectAttempts <= maxReconnectAttempts">กำลังเชื่อมต่อใหม่... (พยายาม {{
      reconnectAttempts }}/{{ maxReconnectAttempts }})</p>
    <p v-if="reconnectAttempts === 0">WebSocket เชื่อมต่อแล้ว</p>
    <div class="toolbar">
      <button @click="setTimeRange('1D')">1D</button>
      <button @click="setTimeRange('1W')">1W</button>
      <button @click="setTimeRange('1M')">1M</button>
    </div>
    <div ref="chart" class="chart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { createChart } from 'lightweight-charts';

const chart = ref(null);
const candleSeries = ref(null);
const seriesData = ref([]); // Initial data for the chart
const timeRange = ref('1M'); // Default time range
const reconnectAttempts = ref(0); // Track reconnection attempts
const maxReconnectAttempts = ref(10); // Limit reconnection attempts

// Initialize the chart after the component is mounted
const initChart = async () => {
  await nextTick();
  chart.value = createChart(chart.value, {
    width: chart.value.clientWidth,
    height: 600,
    layout: {
      backgroundColor: '#000',
      textColor: '#333',
    },
    grid: {
      vertLines: { color: '#e1e3e6' },
      horzLines: { color: '#e1e3e6' },
    },
    timeScale: {
      timeVisible: true,
      secondsVisible: false,
    },
  });

  candleSeries.value = chart.value.addCandlestickSeries();
};

// Fetch initial data to populate the chart
const fetchInitialData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/klines/');
    const data = await response.json();

    seriesData.value = data.map(d => ({
      time: d.time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));
    candleSeries.value.setData(seriesData.value);
  } catch (error) {
    console.error("Error fetching initial data:", error);
  }
};

// Handle WebSocket data
const handleWebSocketData = (data) => {
  try {
    const klines = data.klines; // อาร์เรย์ของอ็อบเจกต์ kline
    if (!klines || !Array.isArray(klines) || !candleSeries.value) return;

    // ประมวลผลข้อมูล kline
    const klineData = klines.map(d => ({
      time: d[0] ? d[0] / 1000 : NaN,  // แปลงเวลาให้เป็นวินาทีจากมิลลิวินาที
      open: parseFloat(d[1]),
      high: parseFloat(d[2]),
      low: parseFloat(d[3]),
      close: parseFloat(d[4]),
    }))
    .filter(d => !isNaN(d.time) && !isNaN(d.open) && !isNaN(d.high) && !isNaN(d.low) && !isNaN(d.close));

    // เพิ่มข้อมูลใหม่ลงในกราฟที่มีอยู่
    if (klineData.length > 0 && candleSeries.value) {
      klineData.forEach(kline => {
        candleSeries.value.update(kline);  // ใช้ update แทน setData
      });
    }
  } catch (err) {
    console.error('เกิดข้อผิดพลาดในการประมวลผลข้อมูลจาก WebSocket:', err);
  }
};



// Connect WebSocket for real-time updates
const connectWebSocket = () => {
  const socket = new WebSocket('ws://127.0.0.1:9000/ws/klines/');

  socket.onopen = () => {
    console.log('WebSocket connected');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log('ข้อมูลจาก WebSocket ที่ได้รับ:', data);
      handleWebSocketData(data);
    } catch (err) {
      console.error('Error parsing WebSocket message:', err);
    }
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  socket.onclose = () => {
    console.log('WebSocket disconnected');
    // Attempt to reconnect after 5 seconds
    setTimeout(connectWebSocket, 5000);
  };
};

// Set visible time range for the chart
const setTimeRange = (range) => {
  const now = Date.now() / 1000;
  let startTime;

  if (range === '1D') startTime = now - 86400;
  else if (range === '1W') startTime = now - 604800;
  else if (range === '1M') startTime = now - 2592000;

  chart.value.timeScale().setVisibleRange({ from: startTime, to: now });
};

// Component mounted lifecycle hook
onMounted(async () => {
  await initChart(); // Initialize chart when the component is mounted
  fetchInitialData(); // Fetch initial data for the chart
  connectWebSocket(); // Connect WebSocket for real-time updates
});
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  width: 50vw;
  height: 50vh;
  background-color: #f4f4f8;
}

.toolbar {
  display: flex;
  gap: 10px;
  padding: 10px;
  z-index: 10;
}

.toolbar button {
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.toolbar button:hover {
  background-color: #45a049;
}

.chart {
  flex-grow: 1;
  width: 100%;
  height: 100%;
}
</style>
