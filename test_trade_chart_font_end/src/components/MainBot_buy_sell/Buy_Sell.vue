<template>
    <div class="container">
    <div class="trade-container">
      <!-- Amount Section -->
      <div class="amount-section">
        <button class="adjust-button" @click="decreaseAmount">-</button>
        <input class="amount-input" type="number" min="0" step="any"  v-model="quantity" />
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
      <button class="buy-button" @click="queueTrade('buy')">BUY</button>
      <div class="countdown">{{ secondsLeft }}s</div>
      <button class="sell-button" @click="queueTrade('sell')">SELL</button>
    </div>
</div>
  </template>
  

<script setup>
import { ref, onMounted, computed } from "vue";

// const is_trading = Boolean(false);

// State variables
const quantity = ref(0);
const tradeResult = ref(null);
const isWaitingForNextCandle = ref(false);
const secondsLeft = ref(0);
const is_button_enter = ref();

// ตัวแปรชั่วคราวเก็บข้อมูลการซื้อ/ขาย
const pendingTrade = ref(null);

// Reactive variable to manage button state
const isDisabled = ref(false);
localStorage.getItem(isDisabled);
// Function to handle button clicks

// ฟังก์ชันดึงข้อมูลเวลาแท่งเทียนถัดไป
const fetchTimeUntilNextCandlestick = async () => {
    try {
        const response = await fetch(
            "http://localhost:8000/api/time_until_next_candlestick/"
        );
        const data = await response.json();
        secondsLeft.value = data.seconds_left;
        is_button_enter.value = data.is_button_enter;
        // console.log(`ได้รับข้อมูล: secondsLeft=${secondsLeft.value}, is_button_enter=${is_button_enter.value}`);
    } catch (error) {
        console.error("เกิดข้อผิดพลาดในการดึงข้อมูล:", error);
    }
};

// ฟังก์ชันบันทึกคำขอซื้อ/ขาย
function queueTrade(action, symbol) {
    if (quantity.value <= 0) {
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
        pendingTrade.value.action === action &&
        pendingTrade.value.symbol === symbol
    ) {
        pendingTrade.value.quantity += quantity.value;
    } else {
        // ถ้ายังไม่มีคำขอ ให้สร้างคำขอใหม่
        pendingTrade.value = { action, symbol, quantity: quantity.value };
        //   pendingTrade.value = { action, symbol, quantity: quantity.value };
        //   alert(`คุณได้บันทึกคำขอ ${action === 'buy' ? 'ซื้อ' : 'ขาย'}\nSymbol: ${symbol}\nQuantity: ${quantity.value}`);
    }

    alert(
        `คุณได้บันทึกคำขอ ${action === "buy" ? "ซื้อ" : "ขาย"
        }\nSymbol: ${symbol}\nQuantity: ${quantity.value}`
    );
}

// ฟังก์ชันส่งข้อมูลไปยัง Backend
async function sendPendingTrade() {
    if (!pendingTrade.value) return;
    alert(`ส่งคำขอสำเลัด`);
    // is_trading = false;

    const { action, symbol, quantity } = pendingTrade.value;

    try {
        const response = await fetch("http://localhost:8000/api/trade/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action, symbol, quantity }),
        });

        const data = await response.json();
        if (response.status === 200) {
            tradeResult.value = `การซื้อขายสำเร็จ!\nAction: ${data.action}\nSymbol: ${data.symbol}\nQuantity: ${data.quantity}\nPrice: ${data.price}\nผลลัพธ์: ${data.win_or_loss}`;
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
            console.log(" Update quantity = ", pendingTrade.value.quantity);
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
quantity.value = parseInt(quantity.value)
  return ((profitPercentage.value / 100) * quantity.value) + quantity.value;
});
// Methods for amount adjustments
const decreaseAmount = () => {
    quantity.value = parseInt(quantity.value)
  if (quantity.value > 0) quantity.value -= 1;
};

const increaseAmount = () => {
quantity.value = parseInt(quantity.value)
  quantity.value += 1;
};

const setAmount = (value) => {
  if (value === 'all') {
    // Logic to set the max available amount can be implemented here
  } else {
    quantity.value += value;
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

    height: 100vh;
    width: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #ff6700;
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