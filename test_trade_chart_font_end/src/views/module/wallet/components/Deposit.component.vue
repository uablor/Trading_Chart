<template>

    <button
      class="px-4 py-2 bg-purple-50 rounded text-black hover:bg-purple-950 hover:text-white transition-all duration-300"
      @click="openModal"
    >
      Deposit
    </button>
    
  <div
    v-if="showModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <!-- Modal Content -->
    <div
      class="bg-gray-900 p-6 rounded-lg w-[500px] max-h-[630px] h-[650px] overflow-y-auto scrollbar-hidden"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <div class="text-lg text-white font-semibold">Deposit Crypto</div>
        <button @click="closeModal" class="text-gray-400 hover:text-white">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div class="text-gray-400 mb-4 text-[13px]">Choose Network</div>

      <!-- Tabs -->
      <div class="flex border-b border-gray-600 mb-4">
        <button
          class="flex-1 text-center py-2"
          :class="{
            'text-purple-700 border-b-2 border-purple-500':
              activeTab === 'internal',
            'text-gray-400': activeTab !== 'internal',
          }"
          @click="activeTab = 'internal'"
        >
          Internal Network
        </button>
        <button
          class="flex-1 text-center py-2"
          :class="{
            'text-purple-700 border-b-2 border-purple-500':
              activeTab === 'crypto',
            'text-gray-400': activeTab !== 'crypto',
          }"
          @click="activeTab = 'crypto'"
        >
          Crypto Network
        </button>
      </div>

      <div class="py-2 px-14">
        <!-- Conditional Content -->
        <div v-if="activeTab === 'internal'">
          <!-- Content for Internal Network -->
          <div class="text-gray-400 text-sm mb-4">
            <div class="mb-2">Username</div>
            <div class="flex items-center bg-gray-800 p-2 rounded mb-4">
              <span class="text-white">@thegod</span>
              <button class="ml-auto text-purple-700" @click="copyUsername">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 16h8M8 12h8m-6 8h2a2 2 0 002-2V4a2 2 0 00-2-2H8a2 2 0 00-2 2v16a2 2 0 002 2z"
                  />
                </svg>
              </button>
            </div>
            <div class="text-center">
              <img
                src="https://th.bing.com/th/id/OIP.ZFt9Ib6ypFgdYK14UxUAhwHaHa?w=204&h=204&c=7&r=0&o=5&pid=1.7"
                alt="QR Code"
                class="w-[300px] mx-auto"
              />
            </div>
          </div>
          <!-- Footer -->
          <div class="text-purple-400 text-sm text-center">
            Lucifer Trade Wallet<br />
            This QR Code is used for transferring funds within the BXTrade.net
            system.
          </div>
        </div>

        <div v-if="activeTab === 'crypto'">
          <!-- Content for Crypto Network -->
          <div class="text-gray-400 text-sm mb-4 space-y-6">
            <div class="mb-4">
              <label for="crypto" class="block text-gray-300 text-lg mb-2"
                >Select Crypto</label
              >
              <div class="relative">
                <select
                  id="countries"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                >
                  <option selected>Choose a country</option>
                  <option value="US">United States</option>
                  <!-- <option value="CA">Canada</option> -->
                </select>
              </div>
            </div>

            <div class="mb-4">
              <label for="network" class="block text-gray-300 text-lg mb-2"
                >Select Network</label
              >
              <div class="relative">
                <select
                  id="countries"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                >
                  <option selected>Choose a country</option>
                  <option value="US">United States</option>
                  <!-- <option value="CA">Canada</option> -->
                </select>
              </div>
            </div>
            <div class="mb-4">
              <label
                for="deposit-address"
                class="block text-gray-300 text-lg mb-2"
                >Deposit Address</label
              >
              <div class="bg-gray-800 text-white rounded-lg p-3">
                <div class="flex justify-between items-center">
                  <span>Scan or copy the address to deposit payment</span>
                  <button
                    class="text-orange-500 hover:text-orange-400 text-sm focus:outline-none"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M8 16h8M8 12h8m-6 8h2a2 2 0 002-2V4a2 2 0 00-2-2H8a2 2 0 00-2 2v16a2 2 0 002 2z"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="text-purple-400 text-sm text-center mt-6">
            Crypto Trade Wallet<br />
            This QR Code is used for transferring funds within the Crypto
            Network.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
//   import qrCodeImage from './qr-code.png';
const showModal = ref(false); // Controls the visibility of the modal
const activeTab = ref("internal"); // Tracks the active tab

const closeModal = () => {
  showModal.value = false;
};

const copyUsername = () => {
  navigator.clipboard.writeText("@thegod").then(() => {
    alert("Copied to clipboard!");
  });
};

const openModal = () => {
  console.log("Opening Modal...");
  showModal.value = true;
};
</script>

<style scoped>
/* Hide scrollbar while allowing scroll */
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}

.scrollbar-hidden {
  -ms-overflow-style: none; /* for Internet Explorer and Edge */
  scrollbar-width: none; /* for Firefox */
}
</style>
