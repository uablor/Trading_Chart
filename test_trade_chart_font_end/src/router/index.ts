import { createRouter, createWebHistory } from "vue-router";
import main_page from "../views/module/Homepage.vue";
import BTC_chart from "../views/module/btc-trading/views/index.vue";
import Sidebar from "../components/Sidebar/Sidebar.vue";
import Navbar from "../components/Navbar/Navbar.vue";
import Buy_Sell from "../components/MainBot_buy_sell/Buy_Sell.vue";
import Wallet from "../views/module/wallet/views/index.vue";
// import Login from "../views/Model_Login/Login.vue";
// import Register from "../views/Model_Login/Register.vue";
import loginComponent from "../views/module/signin-signup/components/login.component.vue";
import registerComponent from "../views/module/signin-signup/components/register.component.vue";

import { useAuthStore } from "../stores/auth";
import chart_buy_sell from "../views/chart_buy_sell.vue";
// import index from "../views/module/wallet/views/index.vue";
import Profile from "../views/module/profile/views/index.vue";
import Footer from "../components/Footer/Footer.vue";

const routes = [
  {
    path: "/admin",
    children: [],
  },
  {
    path: "/",
    children: [
      {
        path: "/",
        name: "homepage",
        component: main_page,
      },
      {
        path: "/chart_trading",
        name: "chart",
        component: BTC_chart,
      },
      {
        path: "/footer",
        name: "footer",
        component: Footer,
      },
      // {
      //   path: "/index",
      //   name: "index",
      //   component: index,
      // },
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
        path: "/login",
        name: "login",
        component: loginComponent,
      },
      {
        path: "/register",
        name: "register",
        component: registerComponent,
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
      {
        path: "/wallet",
        name: "wallet",
        component: Wallet,
      },

      // {
      //   path: "/buy_Sell",
      //   name: "buy_Sell",
      //   component: Buy_Sell,
      // },
    ],
  },
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
