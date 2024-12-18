<template>
  <!-- Header Section -->
  <header class="header">
    <div class="logo">
      <img src="@/assets/image/logo/R.png" alt="BX Trade" class="logo-img" />
      <span class="logo-text">Lucifer Trade</span>
    </div>
    <div class="header-buttons">
      <button class="btn btn-login" @click="triggerLogin">Login</button>
      <button class="btn btn-signup" @click="triggerRegister">Sign Up</button>
    </div>
  </header>
  <div class="app-container text-white">
    <!-- Hero Section -->
    <mainComponent />
    <tablevalueComponent />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import mainComponent from "../components/main.component.vue";
import tablevalueComponent from "../components/tablevalue.component.vue";
// import Login from "../Model_Login/Login.vue";
// import Register from '../Model_Login/Register.vue';
import router from "@/router";
// const offcanvasLogin = ref(null);
// const offcanvasRegisterRef = ref(null); // Rename the ref to avoid conflict
import { useRoute, useRouter } from "vue-router";

const route = useRoute(); 
const triggerLogin = () => {
  router.push("/login");
};
const triggerRegister = () => {
  router.push("/register");
};
</script>

<style scoped>
/* General Styles */
body {
  margin: 0;
  font-family: "Poppins", sans-serif;
  background-color: #101010;
  color: #ffffff;
}

.app-container {
  max-width: 1200px;
  margin: auto;
  padding: 0 20px;
  padding-top: 50px;
}

/* Header Section */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  padding: 20px 35px;
  width: 1350px;
  top: 0;
  z-index: 1;
  background-color: #1f1f1f;
  color: #ffffff;
  /* z-index: 99; */
  /* border: 3px solid red */
}

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

.header-buttons .btn {
  margin-left: 10px;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.btn-login {
  background: rgb(152, 26, 202);
  color: #ffffff;
  /* border: 2px solid #fa0000; */
}

.btn-signup {
  background-color: #0ddf30;
  color: #ffffff;
}
</style>
