<template>
  <div class="min-h-scree background-color text-white p-6">
    <!-- <div class=""> grid grid-cols-1 md:grid-cols-2 gap-6 -->
      <div class="flex justify-between mb-4">
      <!-- Profile Section -->
      <div class="bg-gray-800 rounded-lg p-6 w-[400px] mr-5 h-[500px]">
        <h2 class="text-xl font-semibold mb-4">My Profile</h2>
  
        <div class="flex flex-col items-center">
          <div class="w-24 h-24 bg-gray-700 rounded-full flex items-center justify-center">
            <img src="../../assets/image/Avatar/Aavatar.png" alt="">
          </div>
          <span class="font-semibold mt-2">admin</span>
          <button class="mt-4 bg-gray-700 hover:bg-gray-600 text-sm px-4 py-2 rounded">Edit Profile Picture</button>
        </div>
        <div class="mt-6">
          <p><strong>Email:</strong> admin@gmail.com</p>
          <p><strong>Username:</strong> admin</p>
          <!-- <p><strong>First Name:</strong> </p>
          <p><strong>Last Name:</strong> </p> -->
        </div>
      </div>

      <!-- Security Section -->
      <div class="bg-gray-800 rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">Account Verification and Security</h2>
        
        <!-- Identity Verification -->
        <div class="mb-4">
          <div class="flex items-center justify-between">
            <p>Identity Verification</p>
            <button class="bg-green-500 hover:bg-green-400 text-white px-4 py-2 rounded">Verify Now</button>
          </div>
          <p class="text-sm text-gray-400 mt-2">
            To ensure the security of your assets, we require identity verification. Please provide accurate information as it cannot be changed after verification.
          </p>
        </div>

        <!-- Change Password -->
        <div class="mb-4">
          <div class="flex items-center justify-between">
            <p>Password</p>
            <button class="bg-red-500 hover:bg-red-400 text-white px-4 py-2 rounded">Change</button>
          </div>
          <p class="text-sm text-gray-400 mt-2">
            To change your password, click the button below. 2FA must be enabled.
          </p>
        </div>

        <!-- 2FA -->
        <div class="mb-4">
          <div class="flex items-center justify-between">
            <p>2FA Code</p>
            <input type="checkbox" class="toggle-checkbox" checked />
          </div>
          <p class="text-sm text-gray-400 mt-2">
            Required for withdrawals and security updates.
          </p>
        </div>

        <!-- Transaction Password -->
        <div class="mb-4">
          <div class="flex items-center justify-between">
            <p>Transaction Password</p>
            <input type="checkbox" class="toggle-checkbox" />
          </div>
          <p class="text-sm text-gray-400 mt-2">
            Required for withdrawals, VIP membership registration, and secure trading.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue';


</script>



<style>

.background-color{
  background-color: #1f1f1f;
  /* border: 1px solid #ffffff; */
}
.toggle-checkbox {
  width: 2rem;
  height: 1rem;
  background-color: #374151;
  border-radius: 9999px;
  position: relative;
  outline: none;
  appearance: none;
  cursor: pointer;
}

.toggle-checkbox:checked {
  background-color: #22c55e;
}

.toggle-checkbox:checked::after {
  content: '';
  position: absolute;
  top: 0.125rem;
  left: 1rem;
  width: 0.75rem;
  height: 0.75rem;
  background-color: white;
  border-radius: 50%;
}

.toggle-checkbox::after {
  content: '';
  position: absolute;
  top: 0.125rem;
  left: 0.125rem;
  width: 0.75rem;
  height: 0.75rem;
  background-color: white;
  border-radius: 50%;
  transition: left 0.2s ease;
}
</style>