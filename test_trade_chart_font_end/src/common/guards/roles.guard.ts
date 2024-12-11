export const roleGuard = (to: any, from: any, next: any) => {
  const userRolesString = localStorage.getItem("roles");

  const requiredRoles = to.meta.requiredRoles;

  let userRoles: string[] = [];
  if (userRolesString !== null) {
    try {
      userRoles = JSON.parse(userRolesString);
    } catch (error) {
      console.error("Error parsing user roles:", error);
    }
  }

  if (hasRequiredRole(userRoles, requiredRoles)) {
    next();
  } else {
    next({ name: "test" }); //is false go to default path
  }
};

export const hasRequiredRole = (
  userRoles: string[],
  requiredRoles: string[]
) => {
  return requiredRoles.some((role: string) => userRoles.includes(role));
};

