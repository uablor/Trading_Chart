
import axios from 'axios'
// import { storeToRefs } from 'pinia'
import {useAuthStore} from '../stores/auth'
axios.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    config.headers.Authorization = `Bearer ${authStore.token}`;
    config.headers.Accept = "application/json";

    return config
})

axios.defaults.baseURL = import.meta.env.VITE_BASE_URL;

// axios.defaults.headers['Authorization'] = token.value ? token.value : ''

export default axios