import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token")
  );
  
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("user")));
  const [role, setRole] = useState(() => user?.role);

  const login = (userData, token) => {
    localStorage.setItem("user", JSON.stringify(userData));
    localStorage.setItem("token", token);
    setUser(userData);
    setRole(userData.role);  // Mengatur role di state
    setIsAuthenticated(true);

    
    
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("splashScreenShown");
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
  };

  const hasRole = (role) => {
    return user?.role === role;
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, role, login, logout, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
