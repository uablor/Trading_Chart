<template>
  <div class="navbar">
    <Navbar />
  </div>

  <div class="content">

    <div class="sidebar">

      <Sidebar />
      
    </div>
    <div class="chart_trading">

      <Test_chart />

    </div>
    <div class="buy_sell">

      <Buy_Sell />

    </div>

  </div>

</template>

<script setup lang="js">
import Test_chart from "./components/Test_chart.vue";
import Buy_Sell from "./components/MainBot_buy_sell/Buy_Sell.vue";
import Navbar from "./components/Navbar/Navbar.vue";
import Sidebar from "./components/Sidebar/Sidebar.vue";
</script>

<style>
.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* border: 1px solid #000000; */
  /* padding: 10px; */
  height: 100vh;
  background-color: #1f1f1f;

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
  /* border: 2px solid red; */
  /* width: 20px; */
  height: 100vh;
  /* height: 100vh; */
}
</style>
