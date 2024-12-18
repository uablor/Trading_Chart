<template>
  <div class="bg-gray-800 rounded-lg p-6 w-[400px] mr-5 h-[500px]">
    <h2 class="text-xl font-semibold mb-4">My Profile</h2>

    <div class="flex flex-col items-center">
      <div class="w-24 h-24 bg-gray-700 rounded-full flex items-center justify-center">
        <img src="../../../../assets/image/Avatar/Aavatar.png" alt="Profile Avatar" class="rounded-full">
      </div>
      <span class="font-semibold mt-2">{{ profile.username }}</span>
      <button class="mt-4 bg-gray-700 hover:bg-gray-600 text-sm px-4 py-2 rounded">Edit Profile Picture</button>
    </div>
    <div class="mt-6">
      <p><strong>Email :</strong> {{ profile.email }}</p>
      <p><strong>Username :</strong> {{ profile.username }}</p>
      <p><strong>Verified :</strong> {{ profile.is_verify ? 'Yes' : 'No' }}</p>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import api from '@/services/axios';

const profile = ref({
  email: '',
  username: '',
  avatar: '',
  is_verify: false,
});

onMounted(async () => {
  try {
    const response = await api.get('/auth-me/');
    profile.value = response.data;
  } catch (error) {
    console.error('Error fetching profile data:', error);
  }
});

</script>
