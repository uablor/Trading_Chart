<template>

<div class="tabs">
    <div
      v-for="(tab, index) in tabs"
      :key="index"
      :class="['tab', { active: index === activeTab }]"
      @click="navigateTab(index)"
    >
      <span class="tab-icon">{{ tab.icon }}</span>
      <span class="tab-info">
        <span class="tab-title">{{ tab.title }}</span>
        <span class="tab-category">{{ tab.category }}</span>
      </span>
      <button class="tab-close" @click.stop="removeTab(index)">✖</button>
    </div>
    <button class="add-tab" @click="addTab">+</button>
  </div>

  <div class="content">
    <div class="chart_trading">
      <!-- Dynamically Render the Active Component -->
      <component :is="activeComponent" />
    </div>
    <div class="buy_sell">

      <Buy_Sell/>

    </div>


  </div>

</template>

<script setup lang="js">
import { ref, computed } from "vue";
import BTC from "./module/btc-trading/views/index.vue";
// import ETHChart from "../components/ETHChart.vue";
import ETH from "./module/eht-trading/views/index.vue";
import Buy_Sell from "../components/MainBot_buy_sell/Buy_Sell.vue";

const tabs = ref([
  { icon: "🟠", title: "BTC/USDT", category: "Crypto", component: BTC },
  { icon: "⚪", title: "ETH/USDT", category: "Crypto", component: ETH },
]);

const activeTab = ref(0);

// Computed property to determine the active component
const activeComponent = computed(() => {
  return tabs.value[activeTab.value]?.component || BTC; // Default to BTC
});

// Methods
const navigateTab = (index) => {
  activeTab.value = index;
};

const addTab = () => {
  tabs.value.push({
    icon: "🟡",
    title: "NEW/PAIR",
    category: "Crypto",
    component: BTC, // Default component for new tabs
  });
};

const removeTab = (index) => {
  tabs.value.splice(index, 1);
  if (activeTab.value >= tabs.value.length) {
    activeTab.value = Math.max(tabs.value.length - 1, 0);
  }
};
</script>


<style scoped>
.content {
  display: flex;
  justify-content: space-between;
  /* align-items: center; */
  /* border: 1px solid red; */

  /* padding: 10px; */
  height: 85vh;
  background-color: #1f1f1f;
  width: calc(88% + 15px);
  z-index: 100;
  /* background-color: #eb0404; */

}

.chart_trading {
 margin-top: 20px;
 /* margin-left: 10px; */
  /* border: 2px solid red; */
  /* padding-right:-50px ; */
  /* border: 2px solid red; */

}

.buy_sell {
  /* border: 2px solid red; */
  /* border: 2px solid rgb(163, 31, 240); */
  height: 100%;
  width: 47vh; 
  background-color: rgb(102, 102, 102);
}

.sidebar {
  /* border: 2px solid red; */
  /* width: 20px; */
  height: 100vh;}


  .tabs {
  /* border-top: 1px solid rgb(163, 31, 240); */
  border-left: 1px solid rgb(163, 31, 240);
  border-right: 1px solid rgb(163, 31, 240);
  position: absolute;
  top: 0;
  left: 20%;
  display: flex;
  align-items: center;
  background-color: #1f1f1f;
  z-index: 0;
  overflow-x: auto;
  padding: 5px 10px 10px 10px;
  cursor: pointer;
}

.tab {
  display: flex;
  align-items: center;
  background-color: #333;
  color: #ccc;
  padding: 10px 15px;
  margin-right: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab:hover {
  background-color: #444;
}

.tab.active {
  background: linear-gradient(135deg, #ff6700, #ff3d00);
  color: white;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.tab-icon {
  margin-right: 10px;
}

.tab-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.tab-title {
  font-weight: bold;
  font-size: 14px;
}

.tab-category {
  font-size: 12px;
  color: #aaa;
}

.tab-close {
  background: none;
  border: none;
  color: #ccc;
  margin-left: 10px;
  cursor: pointer;
  font-size: 16px;
}

.tab-close:hover {
  color: white;
}

.add-tab {
  background-color: #ff6700;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-tab:hover {
  background-color: #e65c00;
}
</style>