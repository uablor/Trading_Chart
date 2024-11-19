<template>
  <div class="chart-container">
    <div ref="chartRef" class="tvchart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { createChart } from 'lightweight-charts';

const chartRef = ref(null);
const chart = ref(null);
const candleSeries = ref(null);
const socket = ref(null);

// Chart properties
const chartProperties = {
  width: 800,  // Set initial width
  height: 600, // Set initial height
  layout: {
    background: { color: '#ffffff' },
    textColor: '#333',
  },
  grid: {
    vertLines: { color: '#f0f0f0' },
    horzLines: { color: '#f0f0f0' },
  },
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
  },
};

// Update chart dimensions
const updateChartDimensions = () => {
  if (chart.value && chartRef.value) {
    const width = chartRef.value.clientWidth;
    const height = chartRef.value.clientHeight;
    chart.value.applyOptions({
      width,
      height,
    });
  }
};

// Fetch initial candle data
const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/klines/');
    const data = await response.json();
    
    const formattedData = data.map(d => ({
      time: Math.floor(d[0] / 1000), // Ensure time is an integer
      open: parseFloat(d[1]),
      high: parseFloat(d[2]),
      low: parseFloat(d[3]),
      close: parseFloat(d[4]),
    })).filter(d => !isNaN(d.time));

    if (candleSeries.value && formattedData.length > 0) {
      candleSeries.value.setData(formattedData);
    }
  } catch (err) {
    console.error('Error fetching data:', err);
  }
};

// Handle WebSocket data updates
const handleWebSocketData = (data) => {
  try {
    const klines = data.klines;
    if (Array.isArray(klines) && candleSeries.value) {
      const klineData = {
        time: Math.floor(klines[0].t / 1000), // Ensure time is an integer
        open: parseFloat(klines[0].o),
        high: parseFloat(klines[0].h),
        low: parseFloat(klines[0].l),
        close: parseFloat(klines[0].c),
      };
      candleSeries.value.update(klineData);
    }
  } catch (err) {
    console.error('Error processing WebSocket data:', err);
  }
};

// Setup WebSocket connection
const setupWebSocket = () => {
  socket.value = new WebSocket('ws://127.0.0.1:9000/ws/klines/');

  socket.value.onopen = () => console.log('WebSocket connected');
  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleWebSocketData(data);
  };
  socket.value.onerror = (error) => console.error('WebSocket error:', error);
  socket.value.onclose = () => setTimeout(setupWebSocket, 5000);
};

// Window resize handler
const handleResize = () => {
  updateChartDimensions();
};

onMounted(() => {
  if (chartRef.value) {
    // Create chart with initial properties
    chart.value = createChart(chartRef.value, chartProperties);
    candleSeries.value = chart.value.addCandlestickSeries();
    
    // Set up resize listener
    window.addEventListener('resize', handleResize);
    
    // Initial fetch and setup
    fetchData();
    setupWebSocket();
    
    // Initial dimensions update
    updateChartDimensions();
  }
});

onUnmounted(() => {
  // Clean up
  window.removeEventListener('resize', handleResize);
  if (socket.value) {
    socket.value.close();
  }
  if (chart.value) {
    chart.value.remove();
  }
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
  position: relative;
}

.tvchart {
  width: 100%;
  height: 100%;
}
</style>