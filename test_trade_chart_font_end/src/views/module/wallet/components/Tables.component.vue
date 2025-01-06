<template>
    <div class=" text-white p-6 w-[100%]">
      <!-- Tabs Section -->
      <div class="flex space-x-8 border-b border-gray-700 mb-6">
        <button
          class="px-2 py-1 text-white border-b-2 border-orange-500"
          @click="activeTab = 'overview'"
          :class="activeTab === 'overview' ? 'border-orange-500' : ''"
        >
          Overview
        </button>
        <button
          class="px-2 py-1 text-gray-400"
          @click="activeTab = 'assets'"
        >
          My Assets
        </button>
        <button
          class="px-2 py-1 text-gray-400"
          @click="activeTab = 'history'"
        >
          Transaction History
        </button>
      </div>
  
      <!-- Content Section -->
      <div v-if="activeTab === 'overview'" class="text-center">
        <div class="text-gray-400 mb-4">Asset Allocation</div>
        <div class="flex justify-center items-center">
          <div class="text-4xl">⚖️</div>
        </div>
      </div>
  
      <!-- Date Filters -->
      <div class="flex justify-end space-x-4 mt-6">
        <button
          class="px-4 py-2 bg-orange-500 text-black rounded"
          @click="activeFilter = '7days'"
          :class="activeFilter === '7days' ? 'bg-orange-500 text-black' : 'bg-gray-500 text-white'"
        >
          Last 7 Days
        </button>
        <button
          class="px-4 py-2 bg-gray-500 text-white rounded"
          @click="activeFilter = '30days'"
          :class="activeFilter === '30days' ? 'bg-orange-500 text-black' : 'bg-gray-500 text-white'"
        >
          Last 30 Days
        </button>
        <button
          class="px-4 py-2 bg-gray-500 text-white rounded"
          @click="activeFilter = 'custom'"
        >
          Customize
        </button>
      </div>
    </div>
  </template>
  
  <script setup>

  </script>
  
  <style scoped>

  </style>
  