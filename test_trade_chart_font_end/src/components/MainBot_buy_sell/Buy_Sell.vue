<template>
  <div class="container">
    <div class="trade-container">
      <!-- Amount Section -->
      <div class="amount-section">
        <button class="adjust-button" @click="decreaseAmount">-</button>
        <input class="amount-input" type="number" min="0" step="any" v-model="price" />
        <button class="adjust-button" @click="increaseAmount">+</button>
      </div>

      <!-- Quick Amount Buttons -->
      <div class="quick-amount-buttons">
        <button v-for="value in quickAmounts" :key="value" @click="setAmount(value)" class="quick-amount">
          +{{ value }}
        </button>
        <button @click="setAmount('all')" class="quick-amount">All</button>
      </div>

      <!-- Profit Section -->
      <div class="profit-section">
        <span class="profit-label">Profit</span>
        <span class="profit-value" :class="{ high: calculatedProfit > 0, low: calculatedProfit < 0 }">{{
          profitPercentage }}%</span>
        <span class="profit-amount" :class="{
          positive: calculatedProfit > 0,
          negative: calculatedProfit < 0,
        }">+${{ calculatedProfit.toFixed(2) }}</span>
      </div>

      <!-- Buy/Sell Buttons -->
      <button class="buy-button" :class="{ disabled: is_button_enter }" :disabled="is_button_enter"
        @click="queueTrade('buy', 'BTCUSDT')">
        BUY
      </button>
      <div class="countdown">{{ nextCandlestickTime }}</div>
      <button class="sell-button" :class="{ disabled: is_button_enter }" :disabled="is_button_enter"
        @click="queueTrade('sell', 'BTCUSDT')">
        SELL
      </button>
    </div>
  </div>
</template>

<script setup>
import nextCandlestickTimeComponecnt from "./nextCandlestickTime.componecnt.vue";
import { ref, onMounted, computed } from "vue";
import axios from "../../services/axios";

// const is_trading = Boolean(false);

// State variables
const showAlert = ref(false);
const price = ref(0);
const tradeResult = ref(null);
const tradewin = ref(null);
const tradelose = ref(null);
const isWaitingForNextCandle = ref(false); // ตรวจสอบให้แน่ใจว่าไม่คอมเมนต์ผิด
const secondsLeft = ref(0);
const is_button_enter = ref(false);
const showAlertzero = ref(false);
// ตัวแปรชั่วคราวเก็บข้อมูลการซื้อ/ขาย
const pendingTrade = ref(null);

// Reactive variable to manage button state
const isDisabled = ref(false);

import { useWalletStore } from '@/stores/walletStore';

const walletStore = useWalletStore();
const currentMode = ref(walletStore.selectedWalletMode);
const ModeTrading = ref(currentMode.value == 'real' ? false : true);

import { notification } from "ant-design-vue";
import { SmileOutlined, FrownOutlined } from "@ant-design/icons-vue";
import { h } from "vue";
import { height } from "@fortawesome/free-solid-svg-icons/fa0";
import { Modal, Button } from "ant-design-vue";
const openNotificationWithIcon = (title, type) => {
  const icon =
    type == "error"
      ? h(FrownOutlined, { class: "icon-error" })
      : h(SmileOutlined, { class: "icon-success" });
  notification[type]({
    message: title,
    class: "notification",
    icon: icon,
    closeIcon: h("span", { class: "custom-close-icon" }, "x"),
    style: {
      width: "250px",
      height: "60px",
      backgroundColor: type === "error" ? "#e74c3c" : "#2ecc71",
      borderRadius: "8px",
      fontSize: "16px",
      padding: "20px",
    },
  });
};


// ฟังก์ชันบันทึกคำขอซื้อ/ขาย
async function queueTrade(order_type, symbol) {
  if (price.value <= 0 || isNaN(price.value)) {
    openNotificationWithIcon("Warning ...", "error");
    return;
  }
  openNotificationWithIcon("Successful ...", "success");

  pendingTrade.value = { order_type, symbol, price: price.value, tradeMode: ModeTrading.value };
  console.log(pendingTrade.value.price_type)
  await sendPendingTrade();
}

async function sendPendingTrade() {
  if (!pendingTrade.value) return;

  try {
    console.log("send done ...");
    const response = await axios.post("trading/", pendingTrade.value);
    const data = response.data;

    if (response.status === 200) {
    } else {
      tradeResult.value = data.message || "ข้อผิดพลาดในการทำการซื้อขาย";
      countDown("ข้อผิดพลาดในการทำการซื้อขาย!", tradeResult.value);
      tradeResult.value = data.message || " ";
      countDown(" ", tradeResult.value);
    }
  } catch (error) {
    console.error("ข้อผิดพลาดในการส่งคำขอซื้อขาย:", error);
    alert("ข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์");
    console.error(" : ", error);
    alert(" ");
  } finally {
    pendingTrade.value = null;
  }
}

const socket = ref(null);

const amount = ref(10);
const quickAmounts = [5, 10, 20, 50, 100];
const profit = ref(19.5);
const profitPercentage = ref(95);


onMounted(() => {
  /////////////////////////////////////////////////////////////

  socket.value = new WebSocket("ws://127.0.0.1:9000/ws/trading/"); // Replace with your WebSocket URL

  socket.value.onopen = () => {
    console.log("Connected to WebSocket");
    socket.value.send(JSON.stringify({ action: "fetch_wallet" }));
  };

  socket.value.onmessage = (event) => {
    console.log("WebSocket message received:", event.data);
    const data = JSON.parse(event.data);
    console.log("Wallet data:", data);

    // เช็คว่าใดๆ ของค่าคือ null หรือว่างหรือไม่
    let tradeMessage = "";

    if (data.order_type && data.price && data.symbol && data.win_or_loss) {
      tradeMessage = `order_type : ${data.order_type} \nSymbol: ${data.symbol} \nPrice: ${data.price} \n\n ผลลัพธ์: ${data.win_or_loss}`;
    } else {
      // ถ้าค่ามี null หรือ ว่าง ไม่แสดงค่าเหล่านั้น
      if (data.order_type) {
        tradeMessage += `order_type : ${data.order_type}\n`;
      }
      if (data.symbol) {
        tradeMessage += `Symbol: ${data.symbol}\n`;
      }
      if (data.price) {
        tradeMessage += `Price: ${data.price}\n`;
      }
    }

    tradeResult.value = tradeMessage.trim(); // ลบช่องว่างเกินออก
    console.log("ssssssssssssss", data.win_or_loss.startsWith("win"))
    console.log(data.win_or_loss)
    if (tradeMessage && data.win_or_loss.startsWith("win")) {
      countDown("ການຊື້ຂາຍສຳເລັດ ", tradeResult.value);
    }
  };

  socket.value.onclose = () => {
    console.log("WebSocket disconnected");
  };
});

// Custom modal content component
const ModalContent = {
  props: ["content"],
  template: `
      <div class="modal-content">
        <span v-html="content"></span>
      </div>
    `,
};

const countDown = (title, content) => {
  let secondsToGo = 5;
  const formattedContent = content.replace(/\n/g, "<br/>");

  const modal = Modal.success({
    title: title,
    style: {
      textAlign: "center",
      borderRadius: "3px",
    },
    content: h(ModalContent, {
      content: `${formattedContent}<br/><br/><br/> ${secondsToGo} seconds.`,
    }),
    footer: [
      h(
        Button,
        {
          type: "primary",
          shape: "round", // Rounded button
          class: "custom-ok-btn w-[200px] h-[40px]",
          onClick: () => modal.destroy(),
        },
        "OK"
      ),
    ],
  });

  const interval = setInterval(() => {
    secondsToGo -= 1;
    modal.update({
      content: h(ModalContent, {
        content: `${formattedContent}<br/><br/><br/> ${secondsToGo} seconds.`,
      }),
    });
  }, 1000);

  setTimeout(() => {
    clearInterval(interval);
    modal.destroy();
  }, secondsToGo * 1000);
};

// Computed property for profit calculation
const calculatedProfit = computed(() => {
  price.value = parseInt(price.value);
  return (profitPercentage.value / 100) * price.value + price.value;
});
// Methods for amount adjustments
const decreaseAmount = () => {
  price.value = parseInt(price.value);
  if (price.value > 0) price.value -= 1;
};

const increaseAmount = () => {
  price.value = parseInt(price.value);
  price.value += 1;
};

const setAmount = (value) => {
  if (value === "all") {
    // Logic to set the max available amount can be implemented here
  } else {
    price.value += value;
  }
};


import { onBeforeUnmount } from 'vue';

const nextCandlestickTime = ref('Loading...');

// WebSocket connection URL (replace with your actual WebSocket URL)
const socketUrl = 'ws://127.0.0.1:9000/ws/candlestick/';

// WebSocket instance
let socket2 = null;

onMounted(() => {
  // Initialize the WebSocket connection
  socket2 = new WebSocket(socketUrl);

  // When the connection is established, send a request for the next candlestick time
  socket2.onopen = () => {
    console.log('WebSocket connected');
    socket2.send(JSON.stringify({ request_next_candlestick_time: true }));
  };

  // Handle incoming messages
  socket2.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received data:', data.is_button_enter);
    if (data.next_candlestick_time) {
      nextCandlestickTime.value = data.next_candlestick_time;
    }
    is_button_enter.value = data.is_button_enter;

    // console.log('is_button_enter value:', is_button_enter.value);

  };

  // Handle WebSocket errors
  socket2.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };

  // Handle WebSocket close
  socket2.onclose = () => {
    console.log('WebSocket closed');
  };



});

onBeforeUnmount(() => {
  if (socket2) {
    socket2.close();
  }
});
</script>

<style scoped>
@font-face {
  font-family: "Phetsarath_OT", "Press Start 2P", sans-serif;
  /* Pixelated font */
  src: url("../../assets/font/Phetsarath OT.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}

* {
  font-family: "Phetsarath OT", sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.custom-close-icon {
  color: white;
  /* Change this to any color you prefer */
}

.icon-error {
  color: rgb(255, 255, 255);
  font-size: 24px;
}

.icon-success {
  color: rgb(255, 255, 255);
  font-size: 24px;
}

.notification .ant-notification-notice-message {
  color: white !important;
  /* Force white font for error notifications */
}

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

.container {
  height: 100%;
  width: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 1px solid rgb(163, 31, 240);
  border-left: 1px solid rgb(163, 31, 240);
  border-right: 1px solid rgb(163, 31, 240);
  /* border-radius: 12px; */
  padding: 10px;
  background-color: #1f1f1f;
}

.trade-container {
  /* background-color: #212121; */
  color: white;
  padding: 20px;
  border-radius: 12px;
  font-family: Arial, sans-serif;
  /* border: 2px solid #ff4757; */
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.amount-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.adjust-button {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.adjust-button:hover {
  background-color: #fa5252;
}

.amount-input {
  width: 70px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 5px;
  background-color: #1f1f1f;
  color: white;
  font-size: 16px;
}

.quick-amount-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px;
}

.quick-amount {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.3s ease;
}

.quick-amount:hover {
  background-color: #5a5a5a;
  transform: scale(1.1);
}

.profit-section {
  text-align: center;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.profit-label {
  font-size: 16px;
  color: #f1c40f;
}

.profit-value {
  font-size: 18px;
  font-weight: bold;
  color: orange;
}

.profit-value.high {
  color: #2ecc71;
}

.profit-value.low {
  color: #e74c3c;
}

.profit-amount {
  font-size: 18px;
  font-weight: bold;
}

.profit-amount.positive {
  color: #2ecc71;
}

.profit-amount.negative {
  color: #e74c3c;
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

@media (max-width: 768px) {
  .trade-container {
    width: 100%;
    padding: 15px;
  }

  .quick-amount-buttons {
    gap: 5px;
  }

  .quick-amount {
    padding: 5px 10px;
    font-size: 12px;
  }

  .adjust-button {
    padding: 5px 8px;
    font-size: 16px;
  }

  .amount-input {
    width: 50px;
    font-size: 14px;
  }

  .buy-button,
  .sell-button {
    font-size: 16px;
  }
}

.amount-input::-webkit-outer-spin-button,
.amount-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
