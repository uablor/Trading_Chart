<template>
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">Best-in-Class Binary Options Trading</h1>
        <p class="hero-description">
          We are ready to embark on building a successful trading career on this platform.
        </p>
        <button class="btn btn-trade" @click="triggerLogin">Trade Now</button>
      </div>
      <div class="hero-image">
        <img src="@/assets/image/logo/R.png" alt="Trading Illustration" />
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
            <img :src="crypto.icon" :alt="crypto.name" class="crypto-icon" />
            <span class="crypto-name">{{ crypto.name }}</span>
            <p class="crypto-price">{{ getPrice(crypto.symbol) }}</p>
            <span
              :class="[
                'crypto-change',
                { positive: getChange24h(crypto.symbol) > 0, negative: getChange24h(crypto.symbol) < 0 },
              ]"
            >
              {{ getChange24h(crypto.symbol) > 0 ? "+" : "" }}{{ getChange24h(crypto.symbol) }}%
            </span>
          </div>
  
          <!-- Duplicate the cards for seamless loop -->
          <div
            v-for="crypto in cryptos"
            :key="'duplicate-' + crypto.id"
            class="crypto-card"
          >
            <img :src="crypto.icon" :alt="crypto.name" class="crypto-icon" />
            <span class="crypto-name">{{ crypto.name }}</span>
            <p class="crypto-price">{{ getPrice(crypto.symbol) }}</p>
            <span
              :class="[
                'crypto-change',
                { positive: getChange24h(crypto.symbol) > 0, negative: getChange24h(crypto.symbol) < 0 },
              ]"
            >
              {{ getChange24h(crypto.symbol) > 0 ? "+" : "" }}{{ getChange24h(crypto.symbol) }}%
            </span>
          </div>
        </div>
      </div>
    </section>
  </template>
  <script setup>
  import { ref } from 'vue';
  
  const cryptos = ref([
    
    { id: 1, name: "BTC/USDT", icon: "https://cryptologos.cc/logos/bitcoin-btc-logo.png", symbol: "BTC" },
    { id: 2, name: "ETH/USDT", icon: "https://cryptologos.cc/logos/ethereum-eth-logo.png", symbol: "ETH" },
    { id: 3, name: "SOL/USDT", icon: "https://cryptologos.cc/logos/solana-sol-logo.png", symbol: "SOL" },
    { id: 4, name: "ADA/USDT", icon: "https://cryptologos.cc/logos/cardano-ada-logo.png", symbol: "ADA" },
    { id: 5, name: "DOGE/USDT", icon: "https://cryptologos.cc/logos/dogecoin-doge-logo.png", symbol: "DOGE" },
    // { id: 6, name: "ATOM/USDT", icon: "https://cryptologos.cc/logos/atom-atom-logo.png", symbol: "ATOM" },
    { id: 8, name: "SHIBA/USDT", icon: "https://cryptologos.cc/logos/shiba-inu-shib-logo.png", symbol: "SHIBA" },
    { id: 9, name: "BNB/USDT", icon: "https://cryptologos.cc/logos/binance-coin-bnb-logo.png", symbol: "BNB" },
    { id: 10, name: "BCH/USDT", icon: "https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png", symbol: "BCH" },
  
    { id: 1, name: "BTC/USDT", icon: "https://cryptologos.cc/logos/bitcoin-btc-logo.png", symbol: "BTC" },
    { id: 2, name: "ETH/USDT", icon: "https://cryptologos.cc/logos/ethereum-eth-logo.png", symbol: "ETH" },
    { id: 3, name: "SOL/USDT", icon: "https://cryptologos.cc/logos/solana-sol-logo.png", symbol: "SOL" },
    { id: 4, name: "ADA/USDT", icon: "https://cryptologos.cc/logos/cardano-ada-logo.png", symbol: "ADA" },
    { id: 5, name: "DOGE/USDT", icon: "https://cryptologos.cc/logos/dogecoin-doge-logo.png", symbol: "DOGE" },
    // { id: 6, name: "ATOM/USDT", icon: "https://cryptologos.cc/logos/atom-atom-logo.png", symbol: "ATOM" },
    { id: 8, name: "SHIBA/USDT", icon: "https://cryptologos.cc/logos/shiba-inu-shib-logo.png", symbol: "SHIBA" },
    { id: 9, name: "BNB/USDT", icon: "https://cryptologos.cc/logos/binance-coin-bnb-logo.png", symbol: "BNB" },
    { id: 10, name: "BCH/USDT", icon: "https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png", symbol: "BCH" },
  
]);
  
  const coins = ref([
    { symbol: "BTC", name: "Bitcoin", price: 95787.96, change24h: -0.28 },
    { symbol: "ETH", name: "Ethereum", price: 3649.57, change24h: 0.16 },
    { symbol: "BNB", name: "Binance Coin", price: 748.79, change24h: 14.74 },
    { symbol: "BCH", name: "Bitcoin Cash", price: 565.4, change24h: 5.36 },
    { symbol: "SOL", name: "Solana", price: 235.91, change24h: 3.35 },
    { symbol: "USDT", name: "Tether", price: 1, change24h: 0 },
  ]);
  
  // Function to get price for a crypto symbol
  const getPrice = (symbol) => {
    const coin = coins.value.find(coin => coin.symbol === symbol);
    return coin ? coin.price.toFixed(2) : 'N/A';
  };
  
  // Function to get 24h price change for a crypto symbol
  const getChange24h = (symbol) => {
    const coin = coins.value.find(coin => coin.symbol === symbol);
    return coin ? coin.change24h.toFixed(2) : 'N/A';
  };
  </script>
  
  <style scoped>
/* Smaller Crypto Card */
.crypto-card {
  background-color: #fff;
  border: 1px solid #ddd;
  margin: 5px;
  min-width: 230px !important; /* Decrease width */
  text-align: center;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 8px; /* Decrease padding */
}

/* Adjust the font size for smaller text */
.crypto-name {
  font-size: 14px; /* Decrease font size */
  font-weight: bold;
}

.crypto-price {
  font-size: 12px; /* Decrease font size */
  color: #555;
}

.crypto-change {
  font-size: 10px; /* Decrease font size */
}

.crypto-icon {
  width: 30px; /* Make icon smaller */
  height: 30px;
  margin-bottom: 10px;
  margin-left: 40%;
}

/* Updated Crypto Ticker Section styles */
.crypto-cards-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: hidden;
  width: 100%;
}

.crypto-cards {
  display: flex;
  flex-wrap: nowrap;
  animation: scroll-left-to-right 100s linear infinite;
}

/*  */

.crypto-name {
  font-weight: bold;
  margin-bottom: 8px;
}

.crypto-price {
  font-size: 1rem; /* Adjust font size */
  margin-bottom: 8px;
}

.crypto-change {
  font-size: 0.9rem; /* Adjust font size */
}

.crypto-change.positive {
  color: #4caf50;
}

.crypto-change.negative {
  color: #f44336;
}
  
  /* Keyframe animation for scrolling from left to right */
  @keyframes scroll-left-to-right {
    0% {
      transform: translateX(0);
    }
  
    100% {
      transform: translateX(-50%);
    }
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
    background-color: rgba(116, 58, 143); 
    border-radius: 4px;
    /* height: 100px; */
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
    border-radius: 3px;
    text-align: center;
    width: 150px !important;
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