import router from "../router";
import { defineStore } from "pinia";
import { computed, reactive, ref } from "vue";
import axios from "../services/axios";
import Cookies from "js-cookie";


export const useAuthStore = defineStore("auth", () => {
  //   const tokenFromCookie = Cookies.get("access") || "";
  const tokenFromLocalStorage = localStorage.getItem("access") || "";
  const tokenFromCookie = Cookies.get("token") || "";

  const token = ref(tokenFromLocalStorage || tokenFromCookie);
  const user = reactive<any>({});

  const isAuth = computed(() => token.value !== "");

  const login = async (form: any) => {
    try {
      console.log("start send2")
      const res = await axios.post("user-login/", form);
      const tokenData = res.data.access;
      console.log("start send3")
      token.value = tokenData;
      localStorage.setItem("access", token.value);
      Cookies.set("token", token.value, { expires: 7 });

      // นำทางหลังจากโทเค็นถูกจัดเก็บไว้อย่างปลอดภัย
      console.log("start send4")
      router.push({ name: "chart_buy_sell" });
    } catch (err: any) {
      console.error("Login error:", err);
      if (err.response) {
        alert(err.response.data.non_field_errors);
      }
    }
  };

  const logout = () => {
    token.value = "";
    Cookies.remove("token");
    localStorage.removeItem("access");
    router.push({ name: "homepage"});
  };

  

  return {
    token,
    isAuth,
    user,
    login,
    logout,
  };
});
