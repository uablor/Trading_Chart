<template>
    <div class="relative">
        <!-- Button to Open the Offcanvas -->
        <button class="px-4 py-2 bg-blue-500 text-white rounded" @click="toggleOffcanvas">
            Open Offcanvas
        </button>

        <!-- Offcanvas Component -->
        <div class="fixed top-0 right-0 w-[30rem] h-full bg-gray-800 text-white shadow-lg transform transition-transform duration-300 z-20"
            :class="isOffcanvasVisible ? 'translate-x-0' : 'translate-x-full'">

            <div class="flex items-center justify-between p-4 bg-gray-900">
                <div class="logo">
                    <img src="../assets/image/logo/R.png" alt="BX Trade" class="logo-img" />
                    <span class="logo-text">Trade</span>
                </div>

                <button class="text-white hover:text-gray-400" @click="toggleOffcanvas">
                    ✕
                </button>
            </div>

            <div class="p-4">

                <form @submit.prevent="login" class="space-y-4">
                    <h1 class="text-[30px] mt-10 mb-5"> Log in to your account</h1>
                    <div class="text-left">
                        <!-- <label for="email" class="block text-sm font-medium text-gray-400">Email:</label> -->
                        <input type="email" v-model="formData.email" id="email" placeholder="Enter email" required
                            class="mt-1 block w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500" />
                    </div>
                    <div class="text-left mt-3">
                        <!-- <label for="password" class="block text-sm font-medium text-gray-400">Password:</label> -->
                        <input type="password" v-model="formData.password" id="password" placeholder="Enter password"
                            required
                            class="mt-1 block w-full p-2 border border-gray-600 bg-gray-700 rounded focus:ring focus:ring-blue-500" />
                    </div>
                    <div>
                        <a href="# " class="text-blue-600/100"> Forgot your password?</a>
                    </div>
                    <button type="submit"
                        class="w-full h-[50px] py-2 bg-purple-800 text-white font-semibold rounded hover:bg-purple-700 transition-all durations-600">
                        Login
                    </button>

                    <div class="flex flex-col items-center space-y-4 ">

                        <!-- Horizontal Lines -->
                        <div class="flex items-center w-full">
                            <div class="flex-1 border-t border-gray-300 h-1"></div>
                            <h1 class="text-lg text-gray-700 px-4">or continue with</h1>
                            <div class="flex-1 border-t border-gray-300 h-1"></div>
                        </div>

                        <!-- Example buttons for different login methods -->
                        <!-- Login buttons (Facebook and Google changed to Login) -->

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

        <!-- Overlay -->
        <div class="fixed inset-0 bg-black bg-opacity-50 z-10 transition-opacity duration-300" v-if="isOffcanvasVisible"
            @click="toggleOffcanvas"></div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';

// State for Offcanvas visibility
const isOffcanvasVisible = ref(false);

// Function to toggle Offcanvas visibility
const toggleOffcanvas = () => {
    isOffcanvasVisible.value = !isOffcanvasVisible.value;
};

// Form data
const formData = reactive({
    email: '',
    password: '',
});

// Error message
const errorMessage = ref('');

// Login function
const login = async () => {
    try {
        const response = await axios.post('/api/login/', {
            email: formData.email,
            password: formData.password,
        });
        console.log('Login successful:', response.data);
        localStorage.setItem('token', response.data.token); // Save JWT token
        // Clear form and close Offcanvas
        formData.email = '';
        formData.password = '';
        errorMessage.value = '';
        toggleOffcanvas();
    } catch (error) {
        errorMessage.value =
            error.response?.data?.message || 'Login failed. Please try again.';
    }
};
</script>

<style scoped>
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
