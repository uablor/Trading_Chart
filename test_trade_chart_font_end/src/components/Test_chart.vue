<template>
  <div class="chart-container">
    <!-- <p v-if="reconnectAttempts > 0 && reconnectAttempts <= maxReconnectAttempts">กำลังเชื่อมต่อใหม่... (พยายาม {{
      reconnectAttempts }}/{{ maxReconnectAttempts }})</p>

    <p v-if="reconnectAttempts === 0">WebSocket เชื่อมต่อแล้ว</p> -->
    <!-- <p v-if="secondsLeft > 0">เวลาที่เหลือจนถึงแท่งเทียนถัดไป: {{ secondsLeft }} วินาที</p> -->


    <div ref="chart" class="chart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { createChart } from 'lightweight-charts';

const chart = ref(null);
const candleSeries = ref(null);
const seriesData = ref([]); // Initial data for the chart
const reconnectAttempts = ref(0); // Track reconnection attempts
const maxReconnectAttempts = ref(10); // Limit reconnection attempts
// ประกาศตัวแปร secondsLeft ด้วย ref()


// const secondsLeft = ref(0);
// ฟังก์ชันคำนวณเวลาที่เหลือจนถึงแท่งเทียนถัดไป
// const calculateTimeUntilNextCandlestick = () => {
//   const currentTime = Math.floor(Date.now() / 1000); // เวลาปัจจุบันในหน่วยวินาที
//   const secondsInCurrentMinute = currentTime % 60; // วินาทีที่เหลือในนาทีนี้
//   secondsLeft.value = 60 - secondsInCurrentMinute; // เวลาที่เหลือจนถึงนาทีถัดไป
// };

// เรียกใช้ฟังก์ชันทุกๆ วินาทีเพื่ออัปเดตเวลานับถอยหลัง
// const updateCountdown = () => {
//   calculateTimeUntilNextCandlestick();
//   setInterval(calculateTimeUntilNextCandlestick, 1000); // อัปเดตทุกๆ วินาที
// };

// Initialize the chart after the component is mounted
const initChart = async () => {
  await nextTick();
  chart.value = createChart(chart.value, {
    width: 900,
    height: 500,
    layout: {
      background: { color: '#1f1f1f' },
      textColor: '#fff',
    },
    grid: {
      vertLines: { color: 'rgb(102, 102, 102)' },
      horzLines: { color: 'rgb(102, 102, 102)' },
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
    const klines = data.klines; // อ็อบเจกต์ที่มีข้อมูล kline
    if (!klines || !candleSeries.value) return;

    // ประมวลผลข้อมูล kline
    const klineData = [{
      time: klines.time ? klines.time : NaN, // ใช้ฟิลด์ `time` โดยตรง
      open: parseFloat(klines.open),
      high: parseFloat(klines.high),
      low: parseFloat(klines.low),
      close: parseFloat(klines.close),
    }].filter(d => !isNaN(d.time) && !isNaN(d.open) && !isNaN(d.high) && !isNaN(d.low) && !isNaN(d.close));

    // console.log("ข้อมูลจาก KlineDate ที่ได้รับ:", klineData);
    if (klineData.length > 0 && candleSeries.value) {
      klineData.forEach(kline => {
        candleSeries.value.update(kline); // ใช้ update แทน setData
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
      // console.log('ข้อมูลจาก WebSocket ที่ได้รับ:', data);
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


// Component mounted lifecycle hook
onMounted(async () => {
  await initChart(); // Initialize chart when the component is mounted
  fetchInitialData(); // Fetch initial data for the chart
  connectWebSocket(); // Connect WebSocket for real-time updates
  // updateCountdown();


});
</script>

<style scoped>
.chart-container {
  /* border: 2px solid red; */
  /* display: flex;
  flex-direction: column; */
  background-color: #1f1f1f;
  /* color: azure; */
}

.chart {
  /* flex-grow: 1;
  width: 100%;
  height: 100%; */
  /* background-color: black; */
  /* border: 3px solid red */
}
</style>
