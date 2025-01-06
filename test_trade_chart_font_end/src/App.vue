<template>

  <div class="app">
    <div v-if="!isLoginOrRegister">
      <div class="navbar">
        <Navbar />
      </div>
      <div class="content">
        <div class="sidebar">
          <Sidebar />
        </div>
        <div class=" ml-[100px] w-full">
          <RouterView />
        </div>

      </div>
    </div>
    
    <!-- Show only the RouterView component when on the login or register route -->
    <div class="background_of_public_route" v-if="isLoginOrRegister">
      <RouterView />

      <div class="footer mt-[150px]">
        <Footer />
      </div>
    </div>
  </div>
  <!-- <Homepage/> -->
  <!-- <test/> -->
  <!-- <navbarMoneyComponecnt/> -->
  <!-- <Navbar/> -->
    <!-- <Buy_Sell/>  -->
     <!-- <btc_Tradings/> -->
</template>

<script setup>
import navbarMoneyComponecnt from './components/Navbar/navbar.money.componecnt.vue';
import Footer from './components/Footer/Footer.vue';
import test from './test.vue';
import testest from './testest.vue';
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import Buy_Sell from "./components/MainBot_buy_sell/Buy_Sell.vue";
import Navbar from "./components/Navbar/Navbar.vue";
import Sidebar from "./components/Sidebar/Sidebar.vue";
import btc_Tradings from "./views/module/btc-trading/views/index.vue";
const route = useRoute();

const isLoginOrRegister = computed(() => {
  return ['/login', '/register', '/'].includes(route.path);
});
</script>

<style scoped>
.app {
  height: 640px;
  background-color: #1f1f1f;
  /* border: 2px solid red; */
  /* z-index: 999; */

}

.content {
  display: flex;
  justify-content: space-between;
}

.background_of_public_route {
  background-color: #1f1f1f;
}

.navbar {}

.chart_trading {
  /* border: 2px solid red; */

}

.buy_sell {
  /* border: 2px solid red; */
  height: 100%;
  width: 45vh;
  background-color: rgb(102, 102, 102);
}

.sidebar {
  /* border-right: 2px solid rgb(125, 8, 172); */
  margin-right: 10px;
  height: 550px;
  position: fixed;
  width: 150px;
  z-index: 10000;

}

.chart_trading,
.buy_sell,
.sidebar {
  overflow: hidden;
  /* Disable scrolling on specific elements */
}
</style>
