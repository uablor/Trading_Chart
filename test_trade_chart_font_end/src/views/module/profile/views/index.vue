<template>
<div class="min-h-scree background-color text-white p-6">
    <div class="flex justify-between mb-4">
        <profileComponent/>
        <accountVerifyComponent/>
    </div>

</div>
</template>

<script setup>
import profileComponent from '../components/profile.component.vue';
import accountVerifyComponent from '../components/account.verify.component.vue';
</script>

<style scoped>
</style>
