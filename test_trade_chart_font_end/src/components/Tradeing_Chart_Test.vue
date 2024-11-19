<template>
    <div class="chart-container">
      <p v-if="reconnectAttempts > 0 && reconnectAttempts <= maxReconnectAttempts">
        กำลังเชื่อมต่อใหม่... (พยายาม {{ reconnectAttempts }}/{{ maxReconnectAttempts }})
      </p>
      <p v-if="reconnectAttempts === 0">WebSocket เชื่อมต่อแล้ว</p>
      <div class="toolbar">
        <button @click="setTimeRange('1D')">1D</button>
        <button @click="setTimeRange('1W')">1W</button>
        <button @click="setTimeRange('1M')">1M</button>
      </div>
      <div ref="chartRef" class="chart"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { createChart } from 'lightweight-charts';
  
  const chartRef = ref(null);
  const chart = ref(null);
  const candleSeries = ref(null);
  const socket = ref(null);
  const reconnectAttempts = ref(0);
  const maxReconnectAttempts = 10;
  let isFetchingData = false;
  
  // Initialize the chart
  const initChart = async () => {
  
    chart.value = createChart(chartRef.value, {
      width: chartRef.value.clientWidth,
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
  
  // Fetch initial data
  const fetchInitialData = async () => {
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/klines/');
      const data = await response.json();
  
      if (!Array.isArray(data)) {
        throw new Error('The data received is not an array');
      }
  
      const formattedData = data
        .map(d => ({
          time: d[0] ? d[0] / 1000 : NaN,
          open: parseFloat(d[1]),
          high: parseFloat(d[2]),
          low: parseFloat(d[3]),
          close: parseFloat(d[4]),
        }))
        .filter(d => !isNaN(d.time) && !isNaN(d.open) && !isNaN(d.high) && !isNaN(d.low) && !isNaN(d.close));
  
      formattedData.sort((a, b) => a.time - b.time);
  
      if (candleSeries.value) {
        candleSeries.value.setData(formattedData);
      }
    } catch (err) {
      console.error('Error fetching historical data:', err);
    } finally {
      isFetchingData = false;
    }
  };
  
  // Handle incoming WebSocket data
  const handleWebSocketData = (data) => {
    try {
      const klines = data.klines;
  
      if (!klines || !Array.isArray(klines) || !candleSeries.value) return;
  
      const klineData = klines.map(kline => ({
        time: kline.t / 1000,
        open: parseFloat(kline.o),
        high: parseFloat(kline.h),
        low: parseFloat(kline.l),
        close: parseFloat(kline.c),
      }));
  
      candleSeries.value.update(klineData[klineData.length - 1]);
    } catch (err) {
      console.error('Error processing WebSocket data:', err);
    }
  };
  
  // Set up WebSocket connection with reconnect logic
  const setupWebSocket = () => {
    if (reconnectAttempts.value >= maxReconnectAttempts) {
      console.error('Max reconnection attempts reached.');
      return;
    }
  
    socket.value = new WebSocket('ws://127.0.0.1:9000/ws/klines/');
  
    socket.value.onopen = () => {
      console.log('WebSocket connected');
      reconnectAttempts.value = 0;
    };
  
    socket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleWebSocketData(data);
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };
  
    socket.value.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  
    socket.value.onclose = () => {
      console.log('WebSocket disconnected');
      reconnectAttempts.value++;
      setTimeout(setupWebSocket, 5000);
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
  
  // Mount lifecycle hook
  onMounted(async () => {
    await initChart();
    fetchInitialData();
    setupWebSocket();
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
  