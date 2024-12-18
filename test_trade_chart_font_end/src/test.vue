<template>
    <div>
      <h2>ข้อมูลแท่งเทียนถัดไป</h2>
      <p v-if="nextCandlestickTime">เวลาแท่งเทียนถัดไป: {{ formatTimeToMinutes(nextCandlestickTime) }} (ใน {{ minutesRemaining }} นาที)</p>
      <p v-else>กำลังรอข้อมูล...</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const nextCandlestickTime = ref(null);
  const minutesRemaining = ref(0);
  
  // ฟังก์ชันแปลงเวลาที่ได้รับมาเป็นนาทีจากเวลาปัจจุบัน
  const formatTimeToMinutes = (time) => {
    if (!time) return '';
    const nextTime = new Date(time);
    return nextTime.toLocaleString();  // ใช้รูปแบบเวลาที่เหมาะสม
  };
  
  // สร้างตัวแปรสำหรับจัดการ WebSocket
  let socket = null;
  
  onMounted(() => {
    // เมื่อ component ถูก mount เชื่อมต่อกับ WebSocket
    connectWebSocket();
  });
  
  // ฟังก์ชันสำหรับเชื่อมต่อ WebSocket
  const connectWebSocket = () => {
    // ฟังก์ชันใน Vue.js สำหรับเชื่อมต่อ WebSocket
const socket = new WebSocket('ws://localhost:9000/ws/candlestick/');

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);

  if (data.next_candlestick_time) {
    console.log("Next Candlestick Time:", data.next_candlestick_time);
    console.log("Minutes Remaining:", data.minutes_remaining);
  }

  if (data.error) {
    console.error("Error:", data.error);
  }
};

socket.onopen = function(event) {
  // ส่งคำขอให้ดึงข้อมูลแท่งเทียนถัดไป
  socket.send(JSON.stringify({ request_next_candlestick_time: true }));
};
  };
  </script>
  