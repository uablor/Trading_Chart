<template>
    <div class="header">
      <!-- Logo Section -->
      <div class="logo">
        <img src="../../assets/image/logo/R.png" alt="BX Trade Logo" class="logo-icon" />
        <span class="logo-text">Trade</span>
      </div>
  
      <!-- Tabs Section -->
      <div class="tabs">
        <div
          v-for="(tab, index) in tabs"
          :key="index"
          :class="['tab', { active: index === activeTab }]"
          @click="setActiveTab(index)"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-title">{{ tab.title }}</span>
          <span class="tab-category">{{ tab.category }}</span>
          <button class="tab-close" @click.stop="removeTab(index)">✖</button>
        </div>
        <button class="add-tab" @click="addTab">+</button>
      </div>
  
      <!-- User Section -->
      <div class="user-section">
        <div class="user-avatar">
          <img src="../../assets/image/Avatar/Aavatar.png" alt="User Avatar" />
        </div>
        <div class="account-info">
          <span class="account-type" @click="toggleDropdown">
            {{ currentAccount.type }}
          </span>
          <h2 class="account-balance">${{ currentAccount.balance }}</h2>
        </div>
        <div v-if="dropdownVisible" class="dropdown">
          <div
            class="dropdown-item"
            :class="{ active: currentAccount.type === 'Real Account' }"
            @click="switchAccount('Real Account')"
          >
            Real Account
          </div>
          <div
            class="dropdown-item"
            :class="{ active: currentAccount.type === 'Demo Account' }"
            @click="switchAccount('Demo Account')"
          >
            Demo Account
          </div>
        </div>
        <div class="icons">
          <button class="icon-button">⚙️</button>
          <button class="icon-button">🔔</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const tabs = [
    { icon: '🟠', title: 'BTC/USDT', category: 'Crypto' },
    { icon: '⚪', title: 'ETH/USDT', category: 'Crypto' },
    { icon: '⚫', title: 'XRP/USDT', category: 'Crypto' },
  ];
  
  const activeTab = ref(0);
  
  const currentAccount = ref({
    type: 'Demo Account',
    balance: 0,
  });
  
  const dropdownVisible = ref(false);
  
  // Methods for tabs
  const addTab = () => {
    tabs.push({ icon: '🟡', title: 'NEW/PAIR', category: 'Crypto' });
  };
  
  const removeTab = (index) => {
    tabs.splice(index, 1);
    if (activeTab.value >= tabs.length) {
      activeTab.value = Math.max(tabs.length - 1, 0);
    }
  };
  
  const setActiveTab = (index) => {
    activeTab.value = index;
  };
  
  // Methods for dropdown and account switching
  const toggleDropdown = () => {
    dropdownVisible.value = !dropdownVisible.value;
  };
  
  const switchAccount = (accountType) => {
    if (accountType === 'Real Account') {
      currentAccount.value = { type: 'Real Account', balance: 1000 }; // Example real balance
    } else {
      currentAccount.value = { type: 'Demo Account', balance: 0 }; // Example demo balance
    }
    dropdownVisible.value = false;
  };
  </script>
  
  <style scoped>
  /* Header Styles */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1f1f1f;
    padding: 10px 20px;
    color: antiquewhite;
    border-bottom: 2px solid #ff6700;
  }
  
  /* Logo */
  .logo {
    display: flex;
    align-items: center;
  }
  
  .logo-icon {
    height: 30px;
    margin-right: 10px;
  }
  
  .logo-text {
    font-size: 25px;
    font-weight: bold;
    color: #ffffff;
  }
  
  /* Tabs */
  .tabs {
    display: flex;
    align-items: center;
    flex-grow: 1;
    margin-left: 20px;
  }
  
  .tab {
    display: flex;
    align-items: center;
    background-color: #2a2a2a;
    padding: 8px 12px;
    margin-right: 8px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .tab.active {
    background-color: #7f3aec;
    color: white;
  }
  
  .tab-icon {
    margin-right: 5px;
  }
  
  .tab-title {
    font-weight: bold;
    margin-right: 5px;
  }
  
  .tab-category {
    font-size: 12px;
    color: #cccccc;
  }
  
  .tab-close {
    background: none;
    border: none;
    color: #cccccc;
    font-size: 14px;
    cursor: pointer;
    margin-left: 8px;
  }
  
  .tab-close:hover {
    color: white;
  }
  
  .add-tab {
    background-color: #ff6700;
    color: white;
    border: none;
    font-size: 18px;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .add-tab:hover {
    background-color: #e65c00;
  }
  
  /* User Section */
  .user-section {
    display: flex;
    align-items: center;
  }
  
  .user-avatar img {
    height: 40px;
    width: 40px;
    border-radius: 50%;
    margin-right: 10px;
    border: 2px solid #ff6700;
  }
  
  .account-info {
    margin-right: 20px;
    background-color: #3f3f3f;
    border-radius: 10px;
    height: 50px;
    padding: 0px 10px;
    width: 150px;
  }
  
  .account-type {
    font-size: 12px;
    color: #fafafa;
    cursor: pointer;
    
  }
  
  .account-balance {
    font-size: 16px;
    font-weight: bold;
    color: #ff6700;
    text-align: center;
  }
  
  .dropdown {
    /* position: absolute; */
    background-color: #a7a2a2;
    padding: 10px;
    border-radius: 6px;
    margin-top: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  }
  
  .dropdown-item {
    padding: 5px 10px;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;

  }
  
  .dropdown-item:hover {
    background-color: #ff6700;
  }
  
  .dropdown-item.active {
    background-color: #7f3aec;
  }
  
  .icons {
    display: flex;
    gap: 10px;
  }
  
  .icon-button {
    background: none;
    border: none;
    color: #cccccc;
    font-size: 20px;
    cursor: pointer;
    transition: color 0.3s ease;
  }
  
  .icon-button:hover {
    color: white;
  }
  </style>
  