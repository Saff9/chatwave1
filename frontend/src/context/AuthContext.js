import React, { createContext, useContext, useEffect } from 'react';
import { useAuthStore } from '../stores/authStore';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const { checkAuth, isAuthenticated, user, isLoading } = useAuthStore();

  useEffect(() => {
    const initializeAuth = async () => {
      await checkAuth();
    };
    initializeAuth();
  }, [checkAuth]);

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      isLoading,
      checkAuth,
    }}>
      {children}
    </AuthContext.Provider>
  );
};
