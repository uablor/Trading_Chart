<template>
    <div class="sidebar">
        <ul class="side-login">
            <li>
                <router-link to="/chart_buy_sell" class="trade-login back">
                    <img src="../../assets/image/Chart/6353961.png" class="logo-icon" />
                    <div class="menu-text">Trade</div>
                </router-link>
            </li>
            <li>
                <router-link to="/profile" class="profile back">
                    <img src="../../assets/image/Avatar/Aavatar.png" class="logo-icon" />
                    <div class="menu-text">Profile</div>
                </router-link>
            </li>

            <button @click="showModal" class="button-logout" type="button">

                <img src="../../assets/image/logout-1024.webp" class="logo-icon" />
                <div class="menu-text">Log out</div>
            </button>

        </ul>


    </div> <!-- Modal -->
    <div v-if="isModalVisible" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-[999]">
        <div class="relative p-4 w-full max-w-md max-h-full">
            <div class="relative bg-violet-700 rounded-lg shadow dark:bg-gray-700">
                <button @click="hideModal"
                    class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
                <div class="p-4 md:p-5 text-center">
                    <svg class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
                        Are you want to logout?
                    </h3>
                    <button @click="logout_function"
                        class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center">
                        Logout
                    </button>
                    <button @click="hideModal"
                        class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
                        cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

import { ref } from "vue";

import { useAuthStore } from '../../stores/auth';

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
.sidebar {
    width: 90px;
    /* Adjusted width for a better balance */
    padding: 0px 5px;
    height: 100%;
    background-color: #1f1f1f;
    color: rgb(0, 0, 0);
    display: flex;
    flex-direction: column;

    justify-content: flex-start;
    font-size: 14px;
    /* Adjusted font size for readability */
    /* border-right: 2px solid #8811e9; */
    /* Slight border for a cleaner look */
}

.logo-icon {
    height: 35px;
    /* Slightly reduced the size for a more balanced design */
    width: 35px;
    margin-right: 10px;
    transition: transform 0.3s ease;
    /* Icon scale effect */
}

.side-login li {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgb(241, 241, 241);
    margin-top: 10px;
    text-align: center;
    padding: 12px;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 8px;
    text-transform: uppercase;
    margin-right: 7px;
    /* Uppercase text for uniformity */
}

.button-logout {
    width: 90%;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
    background-color: rgb(241, 241, 241);
    margin-top: 10px;
    text-align: center;
    padding: 12px;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 8px;
    text-transform: uppercase;
    /* Uppercase text for uniformity */
}

.side-login li:hover {
    background-color: rgb(136, 56, 182);
    /* Applies a purple background color */
    transform: scale(1.05);
    /* Slightly enlarges the element on hover */
}

.button-logout:hover {
    background-color: rgb(136, 56, 182);
    /* Applies a purple background color */
    transform: scale(1.05);
    /* Slightly enlarges the element on hover */
}

.side-login li:hover .logo-icon {
    transform: scale(1.2);
    /* Larger icon on hover */
}

.menu-text {
    /* display: inline-block; */
    color: rgb(0, 0, 0);
    font-size: 10px;
    /* Increased font size for better readability */
    /* margin-left: 10px; */
    opacity: 1;
    transition: opacity 0.3s ease;
}

.side-login li:hover .menu-text {
    opacity: 1;
}
</style>