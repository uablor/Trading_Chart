import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import { createPinia } from 'pinia';
import VueApexCharts from 'vue3-apexcharts';
import 'font-awesome/css/font-awesome.css';
import router from './router';
import 'reflect-metadata';
import Antd from 'ant-design-vue';
import { DatePicker } from 'ant-design-vue';
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import 'ant-design-vue/dist/reset.css';
// import 'ant-design-vue/dist/antd.css'; // You can use reset.css for a smaller bundle if preferred.

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
// Use Antd (this includes all necessary components, no need to use `DatePicker` separately)
app.use(Antd);
app.use(VueApexCharts);
app.use(router);
app.use(pinia);

app.mount('#app');
