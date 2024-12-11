// import { roleGuard } from './../../../../common/guards/roles.guard';

import { roleGuard } from "@/common/guards/roles.guard";
import type { RouteRecordRaw } from "vue-router";

export const userRoute: RouteRecordRaw[] = [
    {
        path: "users",
        name: "users",
        component: () => import("../views/index.vue"),
        meta: {
            requiredRoles: ["companyadmin", "companyuser"],
            
        },
        beforeEnter: roleGuard,

    },
];