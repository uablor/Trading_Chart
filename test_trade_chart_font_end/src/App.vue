<template>
  <!-- Only show Navbar and Sidebar if the current route is not '/' or '/login' or '/register' -->
  
  <div class="app">
  <div v-if="!isLoginOrRegister">
    <div class="navbar">
      <Navbar />
    </div>
    <div class="content">
      <div class="sidebar">
        <Sidebar />
      </div>
      <RouterView />
    </div>
  </div>


<!-- Show only the RouterView component when on the login or register route -->
   <div class="background_of_public_route"> 
  <RouterView v-if="isLoginOrRegister"/>
</div>
</div>

</template>

<script setup>
import { useRoute} from 'vue-router';
import { computed } from 'vue';
import Test_chart from "./components/Test_chart.vue";
import Buy_Sell from "./components/MainBot_buy_sell/Buy_Sell.vue";
import Navbar from "./components/Navbar/Navbar.vue";
import Sidebar from "./components/Sidebar/Sidebar.vue";
import testtest from './components/Sidebar/testtest.vue';
const route = useRoute();


const isLoginOrRegister = computed(() => {
  return ['/login', '/register', '/'].includes(route.path);
});
</script>

<style scoped>
.app{
height: 640px;
background-color: #1f1f1f;
/* border: 2px solid red; */
/* z-index: 999; */

}
.content {
  display: flex;
  justify-content: space-between;
}
.background_of_public_route{
  background-color: #1f1f1f;
}
.navbar{
}
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
  border-right: 2px solid rgb(125, 8, 172);
  margin-right: 10px;
  height: 550px;

}
.chart_trading, .buy_sell, .sidebar {
  overflow: hidden; /* Disable scrolling on specific elements */
}
</style>
