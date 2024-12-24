


<template>
    <!-- Include FontAwesome CSS from CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha384-...hash..." crossorigin="anonymous">
  
    <div class="h-screen flex items-center">
      <div 
        class="h-full pt-5 side-bar-background relative transition-all duration-300 ease-in-out w-[83px]"
      >
      <!-- <div :class="{'w-[80px]': activeIndex === null, 'w-[120px]': activeIndex !== null}"></div> -->
        <div class="flex flex-col items-center gap-5 ">
          <!-- Home -->
          <div
            class="relative cursor-pointer w-full"
            @click="toggleActive(0)"
          >
            <router-link  to="/chart_buy_sell" 
              class="relative flex items-center h-12 "
              :class="activeIndex === 0 ? 'justify-end px-6' : 'justify-center'"
            >
              <!-- Green background -->
              <div
                v-if="activeIndex === 0"
                class="absolute inset-0 text-color-define h-12"
              ></div>
              
              <!-- Icon with transition -->
              <div 
                class="relative z-10 transition-all duration-300 flex items-center"
                :class="{ 'translate-x-14': activeIndex === 0 }"
              >
              <i class="fas fa-chart-line text-2xl text-name-menus"></i>
                <!-- <i class="fas fa-home text-2xl text-name-menus"></i> -->
                <!-- Green circle background -->
                <div style="margin-top: -15px; margin-left: -18px;"
                  v-if="activeIndex === 0"
                  class="absolute inset-0 w-16 h-16 text-icon-define rounded-full -translate-x-1 -translate-y-1"
                ></div>
              </div>
              
              <!-- Label -->
              <span
                class="absolute left-2 text-name-menus whitespace-nowrap transition-all duration-300 px-2"
                :class="{ 'opacity-100': activeIndex === 0, 'opacity-0': activeIndex !== 0 }"
              >
                Trader
              </span>
            </router-link>
          </div>
  
          <!-- Dashboard -->
          <div
            class="relative cursor-pointer w-full"
            @click="toggleActive(1)"
          >
            <router-link  to="/wallet"
              class="relative flex items-center h-12"
              :class="activeIndex === 1 ? 'justify-end px-6' : 'justify-center'"
            >
              <div 
                v-if="activeIndex === 1"
                class="absolute inset-0 text-color-define h-12"
              ></div>
              <div 
                class="relative z-10 transition-all duration-300 flex items-center"
                :class="{ 'translate-x-14': activeIndex === 1 }"
              >
              <i class="fas fa-shopping-bag text-2xl text-name-menus"></i>
                <div style="margin-top: -15px; margin-left: -19px;"
                  v-if="activeIndex === 1"
                  class="absolute inset-0 w-16 h-16 text-icon-define rounded-full -translate-x-1 -translate-y-1"
                ></div>
              </div>
              <span
                class="absolute left-2 text-name-menus whitespace-nowrap transition-all duration-300 px-2"
                :class="{ 'opacity-100': activeIndex === 1, 'opacity-0': activeIndex !== 1 }"
              >
                Wallet
              </span>
            </router-link>
          </div>
  
          <!-- Trader -->
          <div
            class="relative cursor-pointer w-full"
            @click="toggleActive(2)"
          >
            <router-link to="/profile" 
              class="relative flex items-center h-12"
              :class="activeIndex === 2 ? 'justify-end px-6' : 'justify-center'"
            >
              <div 
                v-if="activeIndex === 2"
                class="absolute inset-0 text-color-define h-12"
              ></div>
              <div 
                class="relative z-10 transition-all duration-300 flex items-center"
                :class="{ 'translate-x-14': activeIndex === 2 }"
              >
                <i class="fas fa-user-circle text-2xl text-name-menus"></i>
                <div style="margin-top: -15px; margin-left: -18px;"
                  v-if="activeIndex === 2"
                  class="absolute inset-0 w-16 h-16 text-icon-define rounded-full -translate-x-1 -translate-y-1"
                ></div>
              </div>
              <span
                class="absolute left-2 text-name-menus whitespace-nowrap transition-all duration-300 px-2"
                :class="{ 'opacity-100': activeIndex === 2, 'opacity-0': activeIndex !== 2 }"
              >
                Profile
              </span>
            </router-link>
          </div>
  
          <!-- Products -->
          <!-- <div
            class="relative cursor-pointer w-full"
            @click="toggleActive(3)"
          >
            <div 
              class="relative flex items-center h-12"
              :class="activeIndex === 3 ? 'justify-end px-6' : 'justify-center'"
            >
              <div 
                v-if="activeIndex === 3"
                class="absolute inset-0 text-color-define h-12"
              ></div>
              <div 
                class="relative z-10 transition-all duration-300 flex items-center"
                :class="{ 'translate-x-14': activeIndex === 3 }"
              >
                <i class="fas fa-shopping-bag text-2xl text-name-menus"></i>
                <div style="margin-top: -15px; margin-left: -17px;"
                  v-if="activeIndex === 3"
                  class="absolute inset-0 w-16 h-16 text-icon-define rounded-full -translate-x-1 -translate-y-1"
                ></div>
              </div>
              <span
                class="absolute left-2 text-name-menus whitespace-nowrap transition-all duration-300 px-2"
                :class="{ 'opacity-100': activeIndex === 3, 'opacity-0': activeIndex !== 3 }"
              >
                Products
              </span>
            </div>
          </div> -->
  
          <!-- Category -->
          <div
            class="relative cursor-pointer w-full"
            @click="toggleActive(4)"
          >
            <div  @click="showModal"
              class="relative flex items-center h-12"
              :class="activeIndex === 4 ? 'justify-end px-6' : 'justify-center'"
            >
              <div 
                v-if="activeIndex === 4"
                class="absolute inset-0 text-color-define h-12"
              ></div>
              <div 
                class="relative z-10 transition-all duration-300 flex items-center"
                :class="{ 'translate-x-14': activeIndex === 4 }"
              >
                <i class="fas fa-sign-out-alt text-2xl text-name-menus"></i>
                <div style="margin-top: -15px; margin-left: -18px;"
                  v-if="activeIndex === 4"
                  class="absolute inset-0 w-16 h-16 text-icon-define rounded-full -translate-x-1 -translate-y-1"
                ></div>
              </div>
              <span
                class="absolute left-2 text-name-menus whitespace-nowrap transition-all duration-300 px-2"
                :class="{ 'opacity-100': activeIndex === 4, 'opacity-0': activeIndex !== 4 }"
              >
              <!-- <button @click="showModal" > -->
                Logout
              <!-- </button> -->
                
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  
  
    <!-- modal -->
    <div v-if="isModalVisible" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75 z-[9999]">
          <div class="relative p-4 w-full max-w-md max-h-full">
              <div class="relative modal-background dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transform transition-all scale-95 ease-in-out duration-300">
                  <!-- Close Button -->
                  <button @click="hideModal" class="absolute top-3 right-3 text-gray-400 hover:text-gray-900 rounded-lg text-sm focus:outline-none">
                      <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M6 6l8 8m-8 0l8-8" />
                      </svg>
                      <span class="sr-only">Close modal</span>
                  </button>
                  
                  <!-- Modal Content -->
                  <div class="p-4 md:p-6 text-center">
                      <svg class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" aria-hidden="true"
                          xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                      </svg>
                      <h3 class="mb-5 text-lg font-medium text-for-logout">Are you sure you want to logout?</h3>
                      
                      <!-- Logout Button -->
                      <div style="display: flex; gap: 10px; justify-content: center;">
                        <button @click="logout_function"
                          class="buton-logout">
                          <i class="fas fa-sign-out-alt mr-2"></i> Logout
                      </button>
                      
                      <!-- Cancel Button -->
                      <button @click="hideModal"
                          class="buton-cancel-logout">
                          Cancel
                      </button>
                      </div>
                     
                  </div>
              </div>
          </div>
      </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useAuthStore } from '../../stores/auth';
  const activeIndex = ref(null);
  
  const toggleActive = (index) => {
    activeIndex.value = index;
  };
  
  
  const store = useAuthStore()
  const { logout } = store
  
  // Login function
  const logout_function = async () => {
      try {
          // Call the login method from the store
          await logout();
      } catch (err) {
          console.log(err)
          // If there's an error, display it
          errorMessage.value = 'Login failed. Please try again.';
      }
  };
  
  
  // Manage modal visibility state
  const isModalVisible = ref(false);
  
  // Functions to show and hide the modal
  const showModal = () => {
      isModalVisible.value = true;
  };
  

  const hideModal = () => {
      isModalVisible.value = false;
  };
  </script>
  
  <style scoped>
  
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  .text-color-define{
    background: rgb(125, 8, 172);

  
  }
  .text-icon-define{
    background: rgb(125, 8, 172);

  
    z-index: -99;
  
  }
  .text-name-menus{
    color:rgb(255, 255, 255);
  }
  /* .text-name-menus:hover{
    color:white;
  } */
  .side-bar-background{
    /* background: rgb(16, 16, 16); */
    /* border: 2px solid rgb(125, 8, 172); */
    border-right: 2px solid rgb(125, 8, 172);
  
  }
  .modal-background{
    background: rgb(118, 9, 118);
  }
  .text-for-logout{
    color:aliceblue;
  }
  .buton-logout{
    background: rgb(193, 12, 12);
    width: 130px;
    height: 40px;
    margin-top: 20px;
    color:#ffff;
    border-radius: 10px;
    transition: all 0.3s ease;
  }
  .buton-logout:hover{
    background: rgb(123, 15, 15)
  }
  .buton-cancel-logout{
    background:white;
    width: 130px;
    height: 40px;
    margin-top: 20px;
    border-radius: 10px;
    transition: all 0.3s ease;
  }
  .buton-cancel-logout:hover{
    background:rgb(191, 187, 187);
  
  }
  </style>