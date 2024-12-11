import { createRouter, createWebHistory } from "vue-router";
import Test_chart from "../components/Test_chart.vue";
import Sidebar from "../components/Sidebar/Sidebar.vue";
import Navbar from "../components/Navbar/Navbar.vue";
import Buy_Sell from "../components/MainBot_buy_sell/Buy_Sell.vue";

import Login from "../views/Model_Login/Login.vue";
import Register from "../views/Model_Login/Register.vue";
import Homepage from "../views/module/Homepage.vue";
import { useAuthStore } from "../stores/auth";
import chart_buy_sell from "../views/chart_buy_sell.vue";
import test_ from "../views/test_.vue";

import Profile from "../views/Profile/Profile.vue";

const routes = [
  {
    path: "/chart_trading",
    name: "chart",
    component: Test_chart,
  },
  {
    path: "/profile",
    name: "profile",
    component: Profile,
  },
  {
    path: "/chart_buy_sell",
    name: "chart_buy_sell",
    component: chart_buy_sell,
  },
  {
    path: "/test",
    name: "test",
    component: test_,
  },
  {
    path: "/",
    name: "homepage",
    component: Homepage,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },

  {
    path: "/sidebar",
    name: "sidebar",
    component: Sidebar,
  },

  {
    path: "/navbar",
    name: "navbar",
    component: Navbar,
  },

  // {
  //   path: "/buy_Sell",
  //   name: "buy_Sell",
  //   component: Buy_Sell,
  // },

];
const router = createRouter({
  history: createWebHistory(), //import.meta.env.BASE_URL
  routes,
});

// router.beforeEach(async (to) => {
//   // redirect to login page if not logged in and trying to access a restricted page
//   const publicPages = [
//     "/login",
//     "/register",
//     "/welcome",
//   ];
//   const authRequired = !publicPages.includes(to.path);
//   const store = useAuthStore();

//   const { isAuth } = store;

//   if (authRequired && !isAuth) {
//     // auth.returnUrl = to.fullPath;
//     return "/login";
//   } else if (isAuth && to.path === "/register") return "/register";
// });

export default router;
