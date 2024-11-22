<template>
  <p v-if="secondsLeft > 0">เวลาที่เหลือจนถึงแท่งเทียนถัดไป: {{ secondsLeft }} วินาที</p>

  <!-- <div>
    <Test_chart />
  </div> -->

  <div class="form-buy-sell">
    <h1>การซื้อขาย</h1>
    <div>
      <label>
        ปริมาณ:
        <input type="number" class="aoumnt" v-model="quantity" min="1" />
      </label>
    </div>
    <button class="btn-buy" @click="queueTrade('buy', 'BTCUSDT')">ซื้อ</button>
    <button class="btn-sell" @click="queueTrade('sell', 'BTCUSDT')">ขาย</button>
  </div>
</template>


<script setup>
// import Test_chart from './components/Test_chart.vue';
import { ref, onMounted } from 'vue';

const is_trading = Boolean(false);

// State variables
const quantity = ref(0);
const tradeResult = ref(null);
const isWaitingForNextCandle = ref(false);
const secondsLeft = ref(0);

// ตัวแปรชั่วคราวเก็บข้อมูลการซื้อ/ขาย
const pendingTrade = ref(null);

// ฟังก์ชันดึงข้อมูลเวลาแท่งเทียนถัดไป
const fetchTimeUntilNextCandlestick = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/time_until_next_candlestick/');
    const data = await response.json();
    secondsLeft.value = data.seconds_left;
  } catch (error) {
    console.error('เกิดข้อผิดพลาดในการดึงข้อมูล:', error);
  }
};

// ฟังก์ชันบันทึกคำขอซื้อ/ขาย
function queueTrade(action, symbol) {
  if (quantity.value <= 0) {
    alert("ปริมาณต้องมากกว่าศูนย์");
    return;
  }

  if (pendingTrade.value) {
    alert("คุณมีคำขอที่ยังไม่ได้ดำเนินการ กรุณารอแท่งเทียนใหม่");
    return;
  }

  // บันทึกข้อมูลคำขอในตัวแปร `pendingTrade`
  pendingTrade.value = { action, symbol, quantity: quantity.value };
  alert(`คุณได้บันทึกคำขอ ${action === 'buy' ? 'ซื้อ' : 'ขาย'}\nSymbol: ${symbol}\nQuantity: ${quantity.value}`);
}

// ฟังก์ชันส่งข้อมูลไปยัง Backend
async function sendPendingTrade() {
  if (!pendingTrade.value) return;
  alert(`ส่งคำขอสำเลัด`);
  is_trading = false;

  const { action, symbol, quantity } = pendingTrade.value;

  try {
    const response = await fetch('http://localhost:8000/api/trade/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
    console.log(`secondsLeft: ${secondsLeft.value}, pendingTrade:`, pendingTrade.value);
    if(secondsLeft.value === 59){
      is_trading = true
    }

    if (secondsLeft.value === 1 && pendingTrade.value && is_trading) {
      // ส่งคำขอเมื่อถึงแท่งเทียนถัดไป
      await sendPendingTrade();
  
    }
  }, 1000);
});
</script>

<style>
.form-buy-sell {
  position: absolute;
  right: 100px;
  top: 220px;
  border: 2px solid red;
  background-color: aqua;
  padding: 50px 90px;
  border-radius: 10px;
}

.btn-buy,
.btn-sell {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
