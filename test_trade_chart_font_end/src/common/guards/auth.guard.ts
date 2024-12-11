import type { Router } from "vue-router";

export function authGuard(router: Router) {
  router.beforeEach(async (to, from, next) => {
    // console.log(from);
    const token = localStorage.getItem("access_token");
    const roles = localStorage.getItem("roles");
    const parsedRoles = roles ? JSON.parse(roles) : [];

    if (to.meta.skipAuthCheck) {
      next();
    }
    else {
      if (token) {
        if (to.name === "login") {
          if (
            Array.isArray(parsedRoles) &&
            parsedRoles.some((role: any) => ["companyadmin"].includes(role))
          ) {
            next({ name: "users" });
          } else {
            next({ name: "test1" });
          }
        } else {
          next();
        }
      } else {
        if (to.name !== "login") {
          next({ name: "login" });
        } else {
          next();
        }
      }
    }
  });
}