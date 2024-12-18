<template>
    <Homepage/>
      <div class="relative">
        <!-- Offcanvas Component -->
        <div 
          class="fixed top-0 right-0 w-[27rem] h-full bg-gray-800 text-white shadow-lg transform transition-transform duration-300 z-20 overflow-y-auto"
          :class="isOffcanvasVisible_register ? 'translate-x-0' : 'translate-x-full'"
        >
          <div class="flex items-center justify-between p-4 bg-gray-900">
            <div class="logo">
              <img src="@/assets/image/logo/R.png" alt="BX Trade" class="logo-img" />
              <span class="logo-text">Trade</span>
            </div>
    
            <button class="text-white hover:text-gray-400" @click="toggleOffcanvas_register_close">
              ✕
            </button>
          </div>
    
          <div class="p-7">
            <form @submit.prevent="register_user" class="space-y-4">
              <h1 class="text-[30px] mt-10 mb-5"> Create your account</h1>
              <div class="text-left mt-3">
                <input 
                  type="text" 
                  v-model="formData.username" 
                  id="username" 
                  placeholder="Enter username"
                  required
                  class="mt-1 block h-11 w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500"
                />
              </div>
              <div class="text-left">
                <input 
                  type="email" 
                  v-model="formData.email" 
                  id="email" 
                  placeholder="Enter email" 
                  required
                  class="mt-1 block h-11 w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500"
                />
              </div>
              <div class="text-left mt-3">
                <input 
                  type="password" 
                  v-model="formData.password" 
                  id="password" 
                  placeholder="Enter password"
                  required
                  class="mt-1 block h-11 w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500"
                />
              </div>
              <div class="text-left mt-3">
                <input 
                  type="password" 
                  v-model="formData.password2" 
                  id="password2" 
                  placeholder="Enter password again"
                  required
                  class="mt-1 block h-11 w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500"
                />
              </div>
              <div class="text-left mt-3 \">
                <input 
                  type="text" 
                  v-model="formData.invite_code" 
                  id="invite_code" 
                  placeholder="Enter invite code"
                  required
                  class="mt-1 block h-11 cursor-pointer w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500"
                />
              </div>
    
  
                <!-- Checkbox for 18+ and Privacy Policy -->
        <div>
          <input
            type="checkbox"
            v-model="formData.isConfirmed"
            id="terms-checkbox"
          />
          <!-- Make the text clickable and associate it with the checkbox -->
          <label for="terms-checkbox" class="cursor-pointer">
            I confirm that I am 18 years old or older and accept the Privacy Policy.
          </label>
        </div>
  
        <!-- Display message when the checkbox is clicked and checked -->
        <div v-if="formData.isConfirmed" class="success-message">
          You have confirmed that you are 18+ and accept the policy.
        </div>
  
        <!-- Error message if checkbox is not checked -->
        <div v-if="!formData.isConfirmed" class="error-message">
          You must confirm that you are 18 years old or older and accept the Privacy Policy.
        </div>
  
        <!-- Submit button is disabled if the checkbox is not checked -->
                
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
              Sign up...
              </template>
              <template v-else>
                Sign up
              </template>
            </button>
    
              <div class="flex flex-col items-center space-y-4">
                <div class="flex items-center w-full">
                  <div class="flex-1 border-t border-gray-300 h-1"></div>
                  <h1 class="text-lg text-gray-700 px-4">or continue with</h1>
                  <div class="flex-1 border-t border-gray-300 h-1"></div>
                </div>
              </div>
    
              <div class="mt-7">
                <button
                  class="w-full h-[50px] py-2 bg-sky-500 text-white font-semibold rounded hover:bg-blue-600 transition-all duration-300"
                >
                  Facebook
                </button>
                <button
                  class="mt-7 h-[50px] w-full py-2 bg-red-700 text-white font-semibold rounded hover:bg-rose-600 transition-all duration-300"
                >
                  Google
                </button>
              </div>
            </form>
    
            <!-- Error Message -->
            <p v-if="errorMessage" class="mt-4 text-sm text-red-500">{{ errorMessage }}</p>
          </div>
        </div>
    
        <!-- Overlay -->
        <div 
          class="fixed inset-0 bg-black bg-opacity-50 z-10 transition-opacity duration-300" 
          v-if="isOffcanvasVisible_register"
        ></div>
      </div>
    </template>
    
    <script setup>
    import Homepage from '../views/index.vue';
    import { ref, reactive,onMounted } from 'vue';
    import router from '@/router';
    import axios from '@/services/axios';

  
    const isLoading = ref(false)
    // State for Offcanvas visibility
    const isOffcanvasVisible_register = ref(false);
    onMounted(() => {
      toggleOffcanvas_register() // toggleOffcanvasThis will open the offcanvas
  });
    // Function to toggle Offcanvas visibility
    const toggleOffcanvas_register = () => {
      isOffcanvasVisible_register.value = !isOffcanvasVisible_register.value;
    };

    const toggleOffcanvas_register_close = () => {
      isOffcanvasVisible_register.value = !isOffcanvasVisible_register.value;
      router.push("/")
    };

    // Form data
    const formData = ref({
      email: '',
      password: '',
      password2: '',
      username: '',
      invite_code: '',
      isConfirmed:false,
    });
    const register_user = async() =>{
      try{
        isLoading.value = true
      const response = await axios.post('user-register/', formData.value);
          console.log('Register successful:', response.data);
          // router.push("/login")
          // handle register success
      } catch (err) {
          console.error('Error registering:', err);
      }
      finally{
        isLoading.value = false
      }
    }
  
    </script>
    
    <style scoped>
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
    .success-message {
    color: green;
    font-size: 14px;
  }
  
  .error-message {
    color: red;
    font-size: 14px;
  }
  
  button:disabled {
    background-color: gray;
  }
    </style>
    