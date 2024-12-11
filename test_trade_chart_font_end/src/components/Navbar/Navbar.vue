<template>
    <div class="header">
      <!-- Logo Section -->
      <div class="logo">
        <img src="../../assets/image/logo/R.png" alt="BX Trade Logo" class="logo-icon" />
        <span class="logo-text">Trade</span>
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
  import { ref , onMounted, watch} from 'vue';
  import axios from '../../services/axios';
  const currentAccount = ref({
    type: 'Demo Account',
    balance: 1000,
  });
  
  const dropdownVisible = ref(false);
  
  const setActiveTab = (index) => {
    activeTab.value = index;
  };
  
  // Methods for dropdown and account switching
  const toggleDropdown = () => {
    dropdownVisible.value = !dropdownVisible.value;
  };
  

  const switchAccount = async (accountType) => {
  if (accountType === 'Real Account') {
    try {
      // เรียก API เพื่อดึงข้อมูลบัญชีจริง
      const response = await axios.get('wallet/'); // แก้ไข URL ให้ตรงกับ Backend ของคุณ
      const realAccountData = response.data

    if (realAccountData.results && realAccountData.results.length > 0) {
    const wallet = realAccountData.results[0]; // ดึงข้อมูลจาก array results
    currentAccount.value = {
      type: 'Real Account',
      balance: wallet.balance, // ดึงค่า balance จาก wallet
    };
   }} catch (error) {
      console.error('เกิดข้อผิดพลาดในการดึงข้อมูล Real Account:', error);
    }
  } else {
    // ตั้งค่าบัญชี Demo (ถ้าไม่จำเป็นต้องเรียก API)
    currentAccount.value = {
      type: 'Demo Account',
      balance: 1000,
    };
  }
  dropdownVisible.value = false; // ปิด Dropdown
};
onMounted(() => {
  const savedAccount = localStorage.getItem('currentAccount');
  if (savedAccount) {
    currentAccount.value = JSON.parse(savedAccount);
  }
});

watch(currentAccount, (newValue) => {
  localStorage.setItem('currentAccount', JSON.stringify(newValue));
});
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
    border-bottom: 2px solid #8811e9;
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
  