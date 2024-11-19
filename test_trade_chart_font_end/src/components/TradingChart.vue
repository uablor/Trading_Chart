<template>
  <div class="chart-container">
    <div ref="chartRef" class="tvchart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { createChart } from 'lightweight-charts';
import { comma } from 'postcss/lib/list';

// Reactive references
const chartRef = ref(null);
const chart = ref(null);
const candleSeries = ref(null);
const socket = ref(null);

// Chart properties
const chartProperties = {
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

// Function to update chart dimensions
const updateChartDimensions = () => {
  if (chart.value && chartRef.value) {
    const container = chartRef.value;
    chart.value.applyOptions({
      width: container.clientWidth,
      height: container.clientHeight,
    });
  }
};

// Fetch initial candle data
let isFetchingData = false;

const fetchData = async () => {
  if (isFetchingData) return;  // Prevent multiple calls
  isFetchingData = true;  // Set flag to indicate data fetching is in progress

  try {
    const response = await fetch('http://127.0.0.1:8000/api/klines/');

    const data = await response.json()

    if (!Array.isArray(data)) {
      throw new Error('The data received is not an array');
    }
    console.log(":ddddddddddddddddddddddddddddddddddddddddd",data)
    // Process and format the data
    const formattedData = data.map(d => ({
      time: d[0] ? d[0] / 1000 : NaN, // Convert to seconds
      open: parseFloat(d[1]),
      high: parseFloat(d[2]),
      low: parseFloat(d[3]),
      close: parseFloat(d[4]),
    })).filter(d => !isNaN(d.time) && !isNaN(d.open) && !isNaN(d.high) && !isNaN(d.low) && !isNaN(d.close));;

    // Sort the data to ensure it's in ascending order
    formattedData.sort((a, b) => a.time - b.time);

    // ตั้งค่าข้อมูลลงในกราฟ
    if (candleSeries.value) {
      candleSeries.value.setData(formattedData);
    }
  
  } catch (err) {
    console.error('Error fetching historical data:', err);
  } finally {
    isFetchingData = false;  // Reset flag after fetching
  }
};


// Handle WebSocket data updates
const handleWebSocketData = (data) => {
  try {
    // Assuming 'data.klines' is an array of kline objects
    const klines = data.klines; // This should be an array of kline objects, not a single object
    if (!klines || !Array.isArray(klines) || !candleSeries.value) return;

    // Assuming each kline object has the structure { t, o, h, l, c }
    const klineData = klines.map(kline => ({
      time: kline.t / 1000,  // Convert milliseconds to seconds
      open: parseFloat(kline.o),
      high: parseFloat(kline.h),
      low: parseFloat(kline.l),
      close: parseFloat(kline.c),
    }));

    // Update the chart with the new data
    candleSeries.value.update(klineData[klineData.length - 1]); // Update with the latest kline data
  } catch (err) {
    console.error('Error processing WebSocket data:', err);
  }
};

// Setup WebSocket connection
const setupWebSocket = () => {
  socket.value = new WebSocket('ws://127.0.0.1:9000/ws/klines/');

  socket.value.onopen = () => {
    console.log('WebSocket connected');
  };

  socket.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log('WebSocket data received:', data);
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
    // Attempt to reconnect after 5 seconds
    setTimeout(setupWebSocket, 5000);
  };
};

// Component lifecycle hooks
onMounted(() => {
  // Initialize chart
  
  if (chartRef.value) {
    chart.value = createChart(chartRef.value, chartProperties);
    console.log("สร้างกราฟสำเร็จ:", chart.value);
    candleSeries.value = chart.value.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    // Set up resize handler
    window.addEventListener('resize', updateChartDimensions);

    // Initial size update
    updateChartDimensions();

    // Fetch initial data and setup WebSocket
    fetchData();
    setupWebSocket();
  }
});

onBeforeUnmount(() => {
  // Cleanup event listeners
  window.removeEventListener('resize', updateChartDimensions);

  // Close WebSocket connection
  if (socket.value) {
    socket.value.close();
  }
});

</script>

<style scoped>

.chart-container {
  width: 100vh;
  height: 600px;
  border: 1px solid red; /* เพื่อช่วยตรวจสอบการแสดงผล */
}
.tvchart {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>
