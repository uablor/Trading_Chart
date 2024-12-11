<template>
    
    <div class="container">
    <div class="trade-container">
      <!-- Amount Section -->
      <div class="amount-section">
        <button class="adjust-button" @click="decreaseAmount">-</button>
        <input class="amount-input" type="number" min="0" step="any"  v-model="price" />
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
  <span class="profit-value" :class="{ high: calculatedProfit > 0, low: calculatedProfit < 0 }">{{ profitPercentage }}%</span>
  <span class="profit-amount" :class="{ positive: calculatedProfit > 0, negative: calculatedProfit < 0 }">+${{ calculatedProfit.toFixed(2) }}</span>
      </div>
  
      <!-- Buy/Sell Buttons -->
      <button class="buy-button" :class="{'disabled': is_button_enter}"  :disabled="is_button_enter"  @click="queueTrade('buy', 'BTCUSDT')">BUY</button>
      <div class="countdown">{{ secondsLeft }}s</div>
      <button class="sell-button" :class="{'disabled': is_button_enter}"  :disabled="is_button_enter"  @click="queueTrade('sell', 'BTCUSDT')">SELL</button>
    </div>
</div>
  </template>
  

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "../../services/axios";

// const is_trading = Boolean(false);

// State variables
const price = ref(0);
const tradeResult = ref(null);
const isWaitingForNextCandle = ref(false); // ตรวจสอบให้แน่ใจว่าไม่คอมเมนต์ผิด
const secondsLeft = ref(0);
const is_button_enter = ref(false);

// ตัวแปรชั่วคราวเก็บข้อมูลการซื้อ/ขาย
const pendingTrade = ref(null);

// Reactive variable to manage button state
const isDisabled = ref(false);
// localStorage.getItem(isDisabled);
// Function to handle button clicks

// ฟังก์ชันดึงข้อมูลเวลาแท่งเทียนถัดไป
const fetchTimeUntilNextCandlestick = async () => {
    try {
        const response = await axios.get("time_until_next_candlestick/");
        const data = response.data; // Axios parses JSON automatically
        secondsLeft.value = data.seconds_left;
        // console.log("secondsLeft = ", secondsLeft.value);
        is_button_enter.value = data.is_button_enter;
        console.log("btttuot = ", is_button_enter.value)
        // console.log(`Received data: secondsLeft=${secondsLeft.value}, is_button_enter=${is_button_enter.value}`);
    } catch (error) {
        console.error("Error fetching time until next candlestick:", error);
    }
};

// ฟังก์ชันบันทึกคำขอซื้อ/ขาย
function queueTrade(order_type, symbol) {
    if (price.value <= 0) {
        alert("ปริมาณต้องมากกว่าศูนย์");
        return;
    }

    // if (pendingTrade.value) {
    //   alert("คุณมีคำขอที่ยังไม่ได้ดำเนินการ กรุณารอแท่งเทียนใหม่");
    //   return;
    // }

    // บันทึกข้อมูลคำขอในตัวแปร `pendingTrade`
    if (
        pendingTrade.value &&
        pendingTrade.value.order_type === order_type &&
        pendingTrade.value.symbol === symbol
    ){
        pendingTrade.value.price += price.value;
    } else {
        // ถ้ายังไม่มีคำขอ ให้สร้างคำขอใหม่
        pendingTrade.value = { order_type, symbol, price: price.value };
        //   pendingTrade.value = { order_type, symbol, price: price.value };
        //   alert(`คุณได้บันทึกคำขอ ${order_type === 'buy' ? 'ซื้อ' : 'ขาย'}\nSymbol: ${symbol}\nprice: ${price.value}`);
    }

    alert(
        `คุณได้บันทึกคำขอ ${order_type === "buy" ? "ซื้อ" : "ขาย"
        }\nSymbol: ${symbol}\nprice: ${price.value}`
    );
}

// ฟังก์ชันส่งข้อมูลไปยัง Backend
async function sendPendingTrade() {
    if (!pendingTrade.value) return;
    alert(`ส่งคำขอสำเลัด`);
    // is_trading = false;

    // const { order_type, symbol, price } = pendingTrade.value;
    try {
        const response = await axios.post("trading/", pendingTrade.value);

        const data = response.data;
        if (response.status === 200) {
            tradeResult.value = `การซื้อขายสำเร็จ!\norder_type: ${data.order_type}\nSymbol: ${data.symbol}\nprice: ${data.price}\n\nผลลัพธ์: ${data.win_or_loss}`;
            alert(tradeResult.value);
        } else {
            tradeResult.value = data.message || "ข้อผิดพลาดในการทำการซื้อขาย";
            alert(tradeResult.value);
        }
    } catch (error) {
        console.error("ข้อผิดพลาดในการส่งคำขอซื้อขาย:", error);
        alert("ข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์");
    } finally {
        // ล้างค่าหลังส่งข้อมูลสำเร็จ
        pendingTrade.value = null;
    }
}

// ตรวจสอบเวลาแท่งเทียนใหม่
onMounted(() => {
    fetchTimeUntilNextCandlestick();
    setInterval(async () => {
        await fetchTimeUntilNextCandlestick();
        console.log(
            `secondsLeft: ${secondsLeft.value}, pendingTrade:`,
            pendingTrade.value
        );
        // จัดการสถานะปุ่มเปิด/ปิด

        // if (secondsLeft.value === 60){
        //   isDisabled.value = !isDisabled.value;

        // }
        console.log("status button = ", is_button_enter.value);
        if (pendingTrade.value) {
            console.log(" Update price = ", pendingTrade.value.price);
        }

        if (
            secondsLeft.value === 60 &&
            pendingTrade.value &&
            is_button_enter.value
        ) {
            // ส่งคำขอเมื่อถึงแท่งเทียนถัดไป
            await sendPendingTrade();
        }
    }, 1000);
});


// Reactive state variables
const amount = ref(10);
const quickAmounts = [5, 10, 20, 50, 100];
const profit = ref(19.5);
const profitPercentage = ref(95);


// Computed property for profit calculation
const calculatedProfit = computed(() => {
price.value = parseInt(price.value)
  return ((profitPercentage.value / 100) * price.value) + price.value;
});
// Methods for amount adjustments
const decreaseAmount = () => {
    price.value = parseInt(price.value)
  if (price.value > 0) price.value -= 1;
};

const increaseAmount = () => {
price.value = parseInt(price.value)
  price.value += 1;
};

const setAmount = (value) => {
  if (value === 'all') {
    // Logic to set the max available amount can be implemented here
  } else {
    price.value += value;
  }
};

</script>

<style>

@font-face {
    font-family: "Phetsarath_OT", "Press Start 2P", sans-serif;
    /* Pixelated font */
    src: url("../../assets/font/Phetsarath OT.ttf") format("truetype");
    font-weight: normal;
    font-style: normal;
}

* {
    font-family: "Phetsarath OT", sans-serif;
}
@font-face {
    font-family: "Phetsarath_OT", "Press Start 2P", sans-serif;
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

/* body {
    background-color: #121212;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
} */

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


.buy-button, .sell-button {
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
    background-color: #95a5a6 !important; /* Grey color when disabled */
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
    padding: 10px 8px 8px 8px ;
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

    .buy-button, .sell-button {
        font-size: 16px;
    }
}

.amount-input::-webkit-outer-spin-button,
.amount-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

</style>