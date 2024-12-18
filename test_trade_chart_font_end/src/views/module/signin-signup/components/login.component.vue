<template>
    <Homepage />
    <div class="relative">
      <!-- Offcanvas Component -->
      <div class="fixed top-0 right-0 w-[27rem] h-full bg-gray-800 text-white shadow-lg transform transition-transform duration-300 z-20"
        :class="isOffcanvasVisible ? 'translate-x-0' : 'translate-x-full'">
  
        <div class="flex items-center justify-between p-4 bg-gray-900">
          <div class="logo">
            <img src="@/assets/image/logo/R.png" alt="BX Trade" class="logo-img" />
            <span class="logo-text">Trade</span>
          </div>
  
          <!-- ปุ่มปิด -->
          <button class="text-white hover:text-gray-400" @click="toggleOffcanvas_off">
            ✕
          </button>
        </div>
  
        <div class="p-7">
          <form @submit.prevent="onLoginSubmit" class="space-y-4">
            <h1 class="text-[30px] mt-10 mb-5"> Log in to your account</h1>
            <div class="text-left">
              <input type="email" v-model="formData.email" id="email" placeholder="Enter email" required
                class="mt-1 block h-11 w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500" />
            </div>
            <div class="text-left mt-3">
              <input type="password" v-model="formData.password" id="password" placeholder="Enter password" required
                class="mt-1 h-11 block w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500" />
            </div>
            <div>
              <a href="# " class="text-blue-600/100"> Forgot your password?</a>
            </div>
            <button type="submit" :disabled="isLoading" class="w-full h-[50px] py-2 bg-purple-800 text-white font-semibold rounded hover:bg-purple-700 transition-all durations-600 flex items-center justify-center">
              <template v-if="isLoading">
                <svg aria-hidden="true" role="status"
                class="inline w-4 h-4 me-3 text-gray-200 animate-spin dark:text-gray-600" viewBox="0 0 100 101"
                fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                  fill="currentColor" />
                <path
                  d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                  fill="#1C64F2" />
              </svg>
              Loading...
              </template>
              <template v-else>
                Login
              </template>
            </button>
            <div class="flex flex-col items-center space-y-4 ">
  
              <!-- Horizontal Lines -->
              <div class="flex items-center w-full">
                <div class="flex-1 border-t border-gray-300 h-1"></div>
                <h1 class="text-lg text-gray-700 px-4">or continue with</h1>
                <div class="flex-1 border-t border-gray-300 h-1"></div>
              </div>
  
              <!-- Example buttons for different login methods -->
            </div>
            <div class="mt-7">
              <button
                class="w-full h-[50px] py-2 bg-sky-500 text-white font-semibold rounded hover:bg-blue-600 transition-all durations-300">
                Facebook
              </button>
              <button
                class="mt-7 h-[50px] w-full py-2 bg-red-700 text-white font-semibold rounded hover:bg-rose-600 transition-all durations-300">
                Google
              </button>
            </div>
          </form>
  
          <!-- Error Message -->
          <p v-if="errorMessage" class="mt-4 text-sm text-red-500">{{ errorMessage }}</p>
        </div>
      </div>
  
      <!-- Overlay ที่ไม่ทำการคลิกแล้วปิด offcanvas -->
      <div class="fixed inset-0 bg-black bg-opacity-50 z-10 transition-opacity duration-300" v-if="isOffcanvasVisible">
      </div>
    </div>
  </template>
  <script setup>

  import Homepage from '../views/index.vue';
  import { ref, reactive, onMounted } from 'vue';
  import axios from '@/services/axios';
  import router from '@/router';
  import { useAuthStore } from '@/stores/auth';

  const store = useAuthStore()
  const { login } = store
  const isLoading = ref(false); // Loading state
  // State for Offcanvas visibility 
  const isOffcanvasVisible = ref(false);
  // Function to toggle Offcanvas visibility
  const toggleOffcanvas = () => {
    isOffcanvasVisible.value = !isOffcanvasVisible.value;
    console.log("isOffcanvasVisible ", isOffcanvasVisible.value)
  };
  const toggleOffcanvas_off = () => {
  
    isOffcanvasVisible.value = !isOffcanvasVisible.value;
    router.push("/")
  };
  
  // Automatically open the offcanvas when the component is mounted
  onMounted(() => {
    toggleOffcanvas(); // This will open the offcanvas
  });
  
  // Form data
  const formData = reactive({
    email: '',
    password: '',
  });
  
  // Error message
  const errorMessage = ref('');
  
  // Login function
  const onLoginSubmit = async () => {
    try {
      isLoading.value = true; // Start loading
      errorMessage.value = '';
      // Call the login method from the store
      console.log("start send")
      await login(formData);
    } catch (err) {
      console.log(err)
      // If there's an error, display it
      errorMessage.value = 'Login failed. Please try again.';
    }
    finally {
      isLoading.value = false; // Stop loading
    }
  };
  </script>
  
  <style scoped>
  /* Optional: Add custom styles if needed */
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
  
    to {
      transform: rotate(360deg);
    }
  }
  
  /* Spin animation class */
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  /* Optional: Add custom styles if needed */
  .logo {
    display: flex;
    align-items: center;
  }
  
  .logo-img {
    height: 40px;
    margin-right: 10px;
  }
  
  .logo-text {
    font-size: 1.5rem;
    font-weight: bold;
  }
  </style>
  