<template>
    <a-button type="primary" @click="showModal">create new</a-button>
    <AddComponents :visible="state.visible" @update:visible="state.visible = $event" />
    <div>
        <a-table :dataSource="state.users" :columns="state.columns">
            <template #bodyCell="{ column, record }">
                <p v-if="column.key === 'status'" :class="record.status === 'active' ? 'open' : 'close'">
                    {{ record.status === 'active' ? 'open' : 'close' }}
                </p>
            </template>
        </a-table>
    </div>
</template>

<script setup lang="ts">
import AddComponents from '../components/AddComponents.vue';
import { UserStore } from '../store';
const { state, showModal } = UserStore()
</script>

<style scoped>
.open {
    color: green;
}

.close {
    color: red;
}
</style>
