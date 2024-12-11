<template>

  <!-- Header Section -->
  <header class="header">
    <div class="logo">
      <img src="../../assets/image/logo/R.png" alt="BX Trade" class="logo-img" />
      <span class="logo-text">Lucifer Trade</span>
    </div>
    <div class="header-buttons">
      <button class="btn btn-login" @click="triggerLogin">Login</button>
      <button class="btn btn-signup" @click="triggerRegister">Sign Up</button>
    </div>
  </header>
  <div class="app-container text-white">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Best-in-Class Binary Options Trading</h1>
        <p class="hero-description">
          We are ready to embark on building a successful trading career on this platform.
        </p>
        <button class="btn btn-trade" @click="triggerLogin">Trade Now</button>
      </div>
      <div class="hero-image">
        <img src="../../assets/image/logo/R.png" alt="Trading Illustration" />
      </div>
    </section>

    <!-- Crypto Ticker Section -->
    <section class="crypto-ticker text-white">

      <p class="ticker-title">
        <i class="fa fa-bullhorn text-white"></i> Join our platform to trade leading cryptocurrencies instantly.
      </p>

      <div class="crypto-cards-wrapper">
  <div class="crypto-cards">
    <div v-for="crypto in cryptos" :key="crypto.id" class="crypto-card">
      <span class="crypto-name">{{ crypto.name }}</span>
      <p class="crypto-price">{{ crypto.price }}</p>
      <span
        :class="['crypto-change', { positive: crypto.change > 0, negative: crypto.change < 0 }]">
        {{ crypto.change > 0 ? '+' : '' }}{{ crypto.change }}%
      </span>
    </div>
    <!-- Duplicate the cards for seamless loop -->
    <div v-for="crypto in cryptos" :key="'duplicate-' + crypto.id" class="crypto-card">
      <span class="crypto-name">{{ crypto.name }}</span>
      <p class="crypto-price">{{ crypto.price }}</p>
      <span
        :class="['crypto-change', { positive: crypto.change > 0, negative: crypto.change < 0 }]">
        {{ crypto.change > 0 ? '+' : '' }}{{ crypto.change }}%
      </span>
    </div>
  </div>
</div>
    </section>
    <!-- Offcanvas Login -->
    <!-- <Login ref="offcanvasLogin" />
       <Register ref="offcanvasRegisterRef" /> -->

    <div class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
      <div class="bg-gray-800 rounded-lg p-8 shadow-lg">
        <h1 class="text-2xl font-bold mb-4">Cryptocurrency Prices</h1>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div v-for="coin in coins" :key="coin.symbol" class="bg-gray-700 rounded-lg p-4">
            <h2 class="text-lg font-medium mb-2">{{ coin.symbol }}</h2>
            <p class="text-gray-400 mb-2">{{ coin.name }}</p>
            <p class="text-xl font-bold mb-2">${{ coin.price.toFixed(2) }}</p>
            <p :class="[coin.change24h > 0 ? 'text-green-500' : 'text-red-500']">
              {{ coin.change24h.toFixed(2) }}%
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
// import Login from "../Model_Login/Login.vue";
// import Register from '../Model_Login/Register.vue';
import router from '../../router';
// const offcanvasLogin = ref(null);  
// const offcanvasRegisterRef = ref(null); // Rename the ref to avoid conflict
import { useRoute, useRouter } from 'vue-router';

const route = useRoute(); // Correctly initialize the route object
// Function to toggle the login offcanvas
const triggerLogin = () => {
  router.push("/login")
  // offcanvasLogin.value.toggleOffcanvas();

};

// Function to toggle the register offcanvas
const triggerRegister = () => {
  router.push("/register")
  // offcanvasRegisterRef.value.toggleOffcanvas_register();
};


const cryptos = ref([
  { id: 1, name: 'BTC/USDT', price: '$28,500', change: 2.45 },
  { id: 2, name: 'ETH/USDT', price: '$1,750', change: -1.3 },
  { id: 3, name: 'SOL/USDT', price: '$30.12', change: 0.8 },
  { id: 4, name: 'ADA/USDT', price: '$0.40', change: -0.2 },
  { id: 5, name: 'DOC/USDT', price: '$0.40', change: 10.2 },
  { id: 6, name: 'ATOM/USDT', price: '$0.40', change: 1000.2 },
  { id: 7, name: 'THOX/USDT', price: '$0.40', change: -0.2 },
  { id: 8, name: 'SHI/USDT', price: '$0.40', change: -0.20 },
  { id: 9, name: 'GOUF/USDT', price: '$0.40', change: -1.22 },
  { id: 10, name: 'BK/USDT', price: '$0.40', change: -3.3 },
]);

const coins = ref([
  {
    symbol: 'BTC',
    name: 'Bitcoin',
    price: 95787.96,
    change24h: -0.28
  },
  {
    symbol: 'ETH',
    name: 'Ethereum',
    price: 3649.57,
    change24h: 0.16
  },
  {
    symbol: 'BNB',
    name: 'Binance Coin',
    price: 748.79,
    change24h: 14.74
  },
  {
    symbol: 'BCH',
    name: 'Bitcoin Cash',
    price: 565.4,
    change24h: 5.36
  },
  {
    symbol: 'SOL',
    name: 'Solana',
    price: 235.91,
    change24h: 3.35
  },
  {
    symbol: 'USDT',
    name: 'Tether',
    price: 1,
    change24h: 0
  }
]);
// watch(
//   () => route.query.form,
//   (newForm) => {
//     if (newForm === 'login') {
//       triggerLogin();
//     } else if (newForm === 'register') {
//       triggerRegister();
//     }
//   }
// );


// onMounted(() => {
//   if (route.query.form === 'login') {
//     triggerLogin();
//   } else if (route.query.form === 'register') {
//     triggerRegister();
//   }
//   console.log("login :",isOffcanvasVisible.value)
//   console.log("register :",isOffcanvasVisible_register.value)
// });


</script>

<style scoped>
/* General Styles */
body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  background-color: #101010;
  color: #ffffff;
}

.crypto-cards-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: hidden; /* Hide overflow for clean scrolling */
  width: 100%;
  max-width: 100%;
}

.crypto-cards {
  display: flex;
  flex-wrap: nowrap;
  animation: scroll-left-to-right 100s linear infinite;
  /* Updated animation for smooth scrolling from left to right */
}

.crypto-card {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px;
  margin: 5px;
  min-width: 200px;
  text-align: center;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.crypto-name {
  font-size: 16px;
  font-weight: bold;
}

.crypto-price {
  font-size: 14px;
  color: #555;
}

.crypto-change {
  font-size: 12px;
}

.crypto-change.positive {
  color: green;
}

.crypto-change.negative {
  color: red;
}

/* Keyframe animation for scrolling from left to right */
@keyframes scroll-left-to-right {
  0% {
    transform: translateX(0);
    /* Start from the default (left) position */
  }

  100% {
    transform: translateX(-50%);
    /* End at the left side off-screen (move half of the container width) */
  }
}

.app-container {
  max-width: 1200px;
  margin: auto;
  padding: 0 20px;
  padding-top: 50px;
}

/* Header Section */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  padding: 20px 35px;
  width: 1350px;
  top: 0;
  z-index: 1;
  background-color: #1f1f1f;
  ;
  color: #ffffff;
  /* z-index: 99; */
  /* border: 3px solid red */
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.header-buttons .btn {
  margin-left: 10px;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.btn-login {
  background: rgb(152, 26, 202);
  color: #ffffff;
  /* border: 2px solid #fa0000; */
}

.btn-signup {
  background-color: #0ddf30;
  color: #ffffff;
}

/* Hero Section */
.hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 50px;
}

.hero-content {
  max-width: 50%;
}

.hero-title {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.hero-description {
  font-size: 1rem;
  color: #b0b0b0;
  margin-bottom: 30px;
}

.btn-trade {
  padding: 10px 20px;
  background-color: #22db31;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.hero-image img {
  max-width: 100%;
  height: auto;
}

/* Crypto Ticker Section */
.crypto-ticker {
  margin-top: 50px;
  padding: 20px;
  background-color: #743a8f;
  border-radius: 10px;
}

.ticker-title {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.crypto-cards {
  display: flex;
  gap: 20px;
}

.crypto-card {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 150px;
}

.crypto-name {
  font-weight: bold;
  margin-bottom: 10px;
}

.crypto-price {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.crypto-change {
  font-size: 1rem;
}

.crypto-change.positive {
  color: #4caf50;
}

.crypto-change.negative {
  color: #f44336;
}
</style>