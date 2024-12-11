import { createApp } from 'vue'
import './style.css'
import App from './App.vue';
import { createPinia } from 'pinia';
import VueApexCharts from 'vue3-apexcharts';
import 'font-awesome/css/font-awesome.css';
import router from './router';


const app = createApp(App);
app.use(VueApexCharts);
app.use(router)
app.use(createPinia())
app.mount('#app');
