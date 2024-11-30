<template>
    <div class="sidebar">
        <ul class="side-login">
            <li>
                <router-link to="/" class="trade-login">
                    <img src="../../assets/image/Chart/6353961.png" class="logo-icon" />
                    <div class="menu-text">Trade</div>
                </router-link>
            </li>
            <li>
                <router-link to="/about" class="profile">
                    <img src="../../assets/image/Avatar/Aavatar.png" class="logo-icon" />
                    <div class="menu-text">Profile</div>
                </router-link>
            </li>
            <li>
                <router-link to="/contact" class="log-out">
                    <img src="../../assets/image/logout and login/logout-1024.webp" class="logo-icon" />
                    <div class="menu-text">Log out</div>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script setup>
</script>

<style scoped>
.sidebar {
    width: 90px;
    /* Adjusted width for a better balance */
    padding: 0px 5px;
    height: 100vh;
    background-color: #1f1f1f;
    color: rgb(0, 0, 0);
    display: flex;
    flex-direction: column;

    justify-content: flex-start;
    font-size: 14px;
    /* Adjusted font size for readability */
    border-right: 2px solid #ff6700;
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
    /* Uppercase text for uniformity */
}

.side-login li:hover {
    background-color: rgb(136, 56, 182);
    transform: scale(1.05);
    /* Slight scaling on hover */
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