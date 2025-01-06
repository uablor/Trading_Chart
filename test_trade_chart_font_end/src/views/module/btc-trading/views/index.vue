<template>
    <div class="chart-container">
      <div ref="chart" id="chart" class="chart"></div>
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



  const initChart = async () => {

    await nextTick();
    chart.value = createChart(chart.value, {
      width: 950,
      height: 450,
      layout: {
        background: { color: '#1f1f1f' },
        textColor: '#fff',
      },
      grid: {
        vertLines: { color: 'rgb(102, 102, 102, 0.2)' },
        horzLines: { color: 'rgb(102, 102, 102, 0.2)' },
      },
      timeScale: {
            timeVisible: true,
            secondsVisible: false,
            rightOffset: 10, // This keeps some space on the right side
            fixLeftEdge: true, // Locks the left edge of the time scale
        },
      
      priceScale: {
            position: 'right',
            alignLabels: 'center',
            borderColor: '#333333', // Color of the price scale border
        },
    //   crosshair: {
    //     mode: 1,
    //     vertLine: {
    //         color: '#6A5ACD',
    //         width: 1,
    //         style: 0,
    //         visible: true,
    //         labelVisible: true,
    //     },
    //     horzLine: {
    //         color: '#6A5ACD',
    //         width: 1,
    //         style: 0,
    //         visible: true,
    //         labelVisible: true,
    //     },
    // },
    });
    candleSeries.value = chart.value.addCandlestickSeries({
        upColor: '#07C95B',      
        downColor: '#EE0B30',    
        borderUpColor: '#07C95B', 
        borderDownColor: '#EE0B30', 
        wickUpColor: '#07C95B',   
        wickDownColor: '#EE0B30',
    });

    const logicalRange = { from: 10, to: 80 };
    chart.value.timeScale().setVisibleLogicalRange(logicalRange);
  
    chart.value.timeScale().scrollToRealTime();
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
  .chart{
    cursor:crosshair;
  }
  
  </style>
  