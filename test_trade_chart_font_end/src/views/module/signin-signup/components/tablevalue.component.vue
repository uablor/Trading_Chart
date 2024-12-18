<template>
  <div class="bg-gray-900 text-white p-6 rounded-md mt-[70px]">
    <!-- Tabs -->
    <div class="flex space-x-6 border-b border-gray-700 pb-2 mb-4">
      <button
        class="text-orange-500 font-semibold border-b-2 border-orange-500"
      >
        ราคาสูงสุด
      </button>
      <button class="text-gray-400">กำไรสูงสุด</button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-gray-700">
            <th class="p-2">ชื่อ</th>
            <th class="p-2">ราคาสุดท้าย</th>
            <th class="p-2">เปลี่ยนแปลง 24h</th>
            <th class="p-2">แผนภูมิ</th>
            <th class="p-2 text-center">ซื้อขาย</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in data"
            :key="index"
            class="border-b border-gray-800"
          >
            <td class="p-2 flex items-center space-x-2  mt-5">
              <img :src="item.icon" alt="crypto" class="w-6 h-6" />
              <span>{{ item.name }}</span>
            </td>
            <td class="p-2">{{ item.price }}</td>
            <td
              class="p-2"
              :class="item.change24h > 0 ? 'text-green-400' : 'text-red-400'"
            >
              {{ item.change24h > 0 ? '+' : '' }}{{ item.change24h }}%
            </td>
            <td class="p-2">
              <div class="h-10 w-24">
                <!-- Simulate a small chart -->
                <div
                  :class="item.change24h > 0 ? 'bg-green-400' : 'bg-red-400'"
                  class="h-full w-full rounded"
                ></div>
              </div>
            </td>
            <td class="p-2 text-center">
              <button class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-1 rounded-md">
                Trade
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>

const data = [
  {
    name: "BTC/USDT",
    icon: "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
    price: "$100,284.35",
    change24h: -0.63,
  },
  {
    name: "ETH/USDT",
    icon: "https://cryptologos.cc/logos/ethereum-eth-logo.png",
    price: "$3,924.47",
    change24h: -0.44,
  },
  {
    name: "BNB/USDT",
    icon: "https://cryptologos.cc/logos/binance-coin-bnb-logo.png",
    price: "$717.11",
    change24h: 0.45,
  },
  {
    name: "BCH/USDT",
    icon: "https://cryptologos.cc/logos/bitcoin-cash-bch-logo.png",
    price: "$532.80",
    change24h: -2.73,
  },
  {
    name: "SOL/USDT",
    icon: "https://cryptologos.cc/logos/solana-sol-logo.png",
    price: "$223.55",
    change24h: -2.76,
  },
];
</script>

<style scoped></style>