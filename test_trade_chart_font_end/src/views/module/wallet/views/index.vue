<template>
  <div class="text-white p-6 w-[100%]">
    <!-- Header Section -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <div class="text-lg font-semibold">Total Balance (USDT)</div>
        <div class="text-3xl color font-bold pt-3 pb-3">${{ Price }}</div>
        <div class="text-sm text-gray-400">Today's PnL ${{ PnL }} ({{ PnLPercent }}%)</div>
      </div>
      <div>
        <div class="text-sm">Last 30 Days</div>
        <div class="text-red-500">PnL ${{ PnL }}</div>
        <div class="w-32 h-1 bg-red-500 mt-2"></div>
      </div>
    </div>

    <!-- Buttons Section -->
    <!-- <div class="flex space-x-4 mb-6"> -->
      <div class="flex space-x-4 mb-6">
      <DepositComponent />
      <WithdrawComponent/>
      <TransferComponent />
      </div>
    <!-- </div> -->

    <TableComponent />
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DepositComponent from '../components/Deposit.component.vue';
import WithdrawComponent from '../components/Withdraw.component.vue';
import TransferComponent from '../components/Transfer.component.vue';
import TableComponent from '../components/Tables.component.vue';
import axios from '../../../../services/axios';

const Price = ref(0);
const PnL = ref(0);
const PnLPercent = ref(0);

const GetPrice = async () => {
  try {
    const response = await axios.get('wallet/');
    // console.log('Wallet Price:', response.data);
    if (response.data?.results?.length) {
      Price.value = response.data.results[0].real_balance; // Extracting real_balance from the first result
    } else {
      Price.value = 0; // Default to 0 if no results are returned
    }
  } catch (error) {
    console.error('Error fetching wallet price:', error);
    Price.value = 0; // Fallback value
  }
};

// Call GetPrice when the component is mounted
onMounted(() => {
  GetPrice();
});
</script>

<style scoped>
.color{
  color: rgb(10, 194, 10);

}
/* Add any custom styles here */
</style>
