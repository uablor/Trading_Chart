<template>
  <footer class="bg-gray-900 text-white py-8 px-6">
    <!-- Top Section -->
    <div class="flex flex-wrap justify-between items-center border-b border-gray-700 pb-6 mb-6">
      <!-- Logo and Contact -->
      <div>
        <div class="flex items-center space-x-2">
          <img src="../../assets/image/logo/R.png" class="h-14" />
          <span class="text-lg font-bold">Lucifer Trade</span>
        </div>
        <p class="text-gray-400 text-sm mt-2">&copy; 2024 Lucifer Trade. All rights reserved.</p>
        <p class="text-sm mt-1">
          Email:
          <a href="#" class="text-orange-500 hover:underline">
            Lucifer@gmail.com
          </a>
        </p>
      </div>

      <!-- License Info -->
      <div class="text-sm text-gray-400">
        <p>Licensed and operated by Finance LLC</p>
        <p>Registered since Year 2023</p>
        <p>Address: 3rd Floor, Bank of Saint Lucia Limited, Bridge Street, Castries, Saint Lucia.</p>
      </div>

      <!-- Help and Options -->
      <div class="text-right space-y-2">
        <ul class="text-sm text-gray-400">
          <li><a href="#" class="hover:text-white">Help</a></li>
          <li><a href="#" class="hover:text-white">Terms of Use</a></li>
          <li><a href="#" class="hover:text-white">Privacy Policy</a></li>
          <li><a href="#" class="hover:text-white">About Us</a></li>
          <li><a href="#" class="hover:text-white">How to Register with Lucifer Trade</a></li>
        </ul>
        <div class="flex items-center space-x-4 mt-4">
          <!-- Language Selector -->
          <div class="flex items-center space-x-2">
            <span>English</span>
            <select class="bg-gray-800 text-gray-400 rounded p-1">
              <option>English</option>
              <option>ไทย</option>
            </select>
          </div>
          <!-- Dark Mode Toggle -->
          <div class="flex items-center space-x-2">
            <span>🌙</span>
            <select class="bg-gray-800 text-gray-400 rounded p-1">
              <option>Dark</option>
              <option>Light</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Disclaimer -->
    <div class="text-gray-500 text-xs text-center leading-6">
      <p>
        Risk Warning: Trading tools on this platform carry a high level of risk and may result in the loss of all your
        funds.
        Therefore, they may not be suitable for all investors...
      </p>
      <p>
        Lucifer Trade is not responsible for any losses or damages arising from the use of our services...
      </p>
    </div>
  </footer>
</template>

<script setup>
// Placeholder for the footer content
</script>

<style scoped>
/* Custom styles if needed */
</style>