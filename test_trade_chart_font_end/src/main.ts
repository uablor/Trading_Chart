import { createApp } from 'vue'
import './style.css'
import App from './App.vue';
import VueApexCharts from 'vue3-apexcharts';
import 'font-awesome/css/font-awesome.css';

const app = createApp(App);
app.use(VueApexCharts);
app.mount('#app');
