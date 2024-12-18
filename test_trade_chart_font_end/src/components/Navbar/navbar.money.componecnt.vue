<template>
    <div class="">
      <div class="card-drop">
        <a class="toggle" @mousedown.prevent="toggleDropdown">
          <div>
            <div class="text-white absolute top-3">{{ selectedtypeWallet }}</div>
            <div class="font-bold mt-3"
              :style="{ color: selectedtypeWallet === 'บัญชีจริง' ? 'green' : selectedtypeWallet === 'บัญชีทดลอง' ? 'yellow' : 'inherit' }">
              <font-awesome-icon :icon="selectedIcon" />
              {{ selectedLabel }}
            </div>
          </div>
        </a>
        <ul>
          <li v-for="(account, index) in accounts" :key="index"
            :class="{ active: selectedIndex === index, closed: !dropdownActive }" :style="getListItemStyle(index)">
            <a href="#" :style="{ color: account.color }" @click.prevent="selectAccount(index)">
              <font-awesome-icon :icon="account.icon" class="mr-[8px]" />
              <span class="size-[1.1em]" :style="{ color: account.color }">
                {{ account.type }}
              </span>
              <span class="size-[1.1em] ml-[8px]" :style="{ marginLeft: '8px', color: account.color }">
                {{ account.value }}
              </span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { faWallet, faBolt } from '@fortawesome/free-solid-svg-icons';
  import { ref, reactive, onMounted, watch } from 'vue';
  import axios from '../../services/axios';
  
  library.add(faWallet, faBolt);
  
  const wallet = reactive({
    demo_balance: 0,
    real_balance: 0,
  });
  
  const accounts = reactive([
    {
      type: "บัญชีจริง",
      value: wallet.real_balance,
      icon: faWallet,
      color: "lightgreen",
    },
    {
      type: "บัญชีทดลอง",
      value: wallet.demo_balance,
      icon: faBolt,
      color: "yellow",
    },
  ]);
  
  const dropdownActive = ref(false);
  const selectedIndex = ref(0);
  const selectedLabel = ref(accounts[0].value);
  const selectedIcon = ref(faWallet);
  const selectedtypeWallet = ref(accounts[0].type);
  const socket = ref(null);
  
  const toggleDropdown = () => {
    dropdownActive.value = !dropdownActive.value;
  };
  
  const selectAccount = (index) => {
    selectedIndex.value = index;
    selectedLabel.value = accounts[index].value;
    selectedtypeWallet.value = accounts[index].type;
    selectedIcon.value = accounts[index].icon;
    dropdownActive.value = false;
  };
  
  const getListItemStyle = (index) => {
    if (!dropdownActive.value) {
      return {
        top: `${index * 2}px`,
        width: `calc(100% - ${index * 2}px)`,
        marginLeft: `${(index * 2) / 2}px`,
      };
    }
    return {
      top: `${60 * (index + 1)}px`,
      width: "100%",
      marginLeft: "0px",
    };
  };
  
  const connectWebSocket = () => {
    socket.value = new WebSocket('ws://127.0.0.1:9000/ws/wallet/');
  
    socket.value.onopen = () => {
  //  console.log('Connected to WebSocket');
   socket.value.send(JSON.stringify({ action: 'fetch_wallet' }));
};

socket.value.onmessage = (event) => {
  //  console.log("WebSocket message received:", event.data);
   const data = JSON.parse(event.data);
  //  console.log("Wallet data:", data.wallet);

   // Update accounts data
   accounts[0].value = data.wallet.real_balance;
   accounts[1].value = data.wallet.demo_balance;
   selectedLabel.value = accounts[0].value;
   selectedtypeWallet.value = accounts[0].type;
};
  
    socket.value.onclose = () => {
      console.log('Disconnected from WebSocket');
    };
  
    socket.value.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };
  };
  
  onMounted(async () => {
    connectWebSocket();
  });
  </script>
      <!-- // try {
        //   const response = await axios.get('wallet/');
        //   const data = response.data.results[0];
      
        //   accounts[0].value = data.real_balance;
        //   accounts[1].value = data.demo_balance;
          
        //   selectedLabel.value = accounts[0].value;
        //   selectedtypeWallet.value = accounts[0].type;
          
        //   console.log(data.demo_balance);
        // } catch (error) {
        //   console.error('Error fetching accounts:', error);
        // } -->
  
  <style scoped>
  body {
    background-color: #edeae3;
    font-family: helvetica, arial, sans-serif;
    padding-top: 40px;
  }
  
  .card-drop {
    z-index:1000;
    max-width: 250px;
    position: relative;
    margin: 0 auto;
    perspective: 800px;
    /* border: 2px solid red;? */
  }
  
  .card-drop a {
    display: block;
    width: 100%;
    background-color: rgb(162, 0, 255);
    padding: 20px 0 20px 20px;
    height: 60px;
    text-decoration: none;
    color: #1a0631;
    background-color: #1a0631;
    border-bottom: 1px solid #a200ff;
    transition: all 0.3s ease-out;
  }
  
  .card-drop a.toggle {
    cursor: pointer;
    position: relative;
    z-index: 300;
    backface-visibility: hidden;
    transform-style: preserve-3d;
    transform-origin: 50% 0%;
    transition: 0.1s linear;
    background-color: #3c0747;
  }
  
  .card-drop a.toggle:active {
    transform: rotateX(60deg);
  }
  
  .card-drop a.toggle.active:before {
    content: "\f0d8";
  }
  
  .card-drop a.toggle:before {
    font-family: 'FontAwesome';
    content: '\f0d7';
    font-size: 1.3em;
    color: #ebebeb;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.3);
    position: absolute;
    right: 0;
    top: 0;
    height: 59px;
    line-height: 60px;
    width: 60px;
    text-align: center;
    display: block;
    border-left: 1px solid #ffffff;
  }
  
  .card-drop ul {
    position: absolute;
    height: 100%;
    top: 0;
    display: block;
    width: 100%;
  }
  
  .card-drop ul li {
    margin: 0 auto;
    transition: all 0.3s ease-out;
    position: absolute;
    top: 0;
    z-index: 0;
    width: 100%;
  }
  
  .card-drop ul li.active a {
    color: #fff;
    cursor: default;
  }
  
  .card-drop ul li.closed a:hover {
    cursor: default;
    background-color: #1a0631;
  }
  
  .card-drop ul li a:hover {
    background-color: #3c0747;
  }
  </style>
  