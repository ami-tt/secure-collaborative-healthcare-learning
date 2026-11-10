import React, { createContext, useContext, useState, useEffect } from 'react';

import { authService } from '../services/api';



const AuthContext = createContext(null);



export const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null);

  const [loading, setLoading] = useState(true);



  useEffect(() => {

    // Check if token exists on load

    const storedUser = authService.getCurrentUser();

    if (storedUser) {

      setUser(storedUser);

      // Verify token freshness against /auth/me

      authService.getMe()

        .then((profile) => {

          setUser((prev) => ({ ...prev, ...profile }));

        })

        .catch(() => {

          authService.logout();

          setUser(null);

        })

        .finally(() => setLoading(false));

    } else {

      setLoading(false);

    }

  }, []);



  const login = async (email, password) => {

    setLoading(true);

    try {

      const data = await authService.login(email, password);

      setUser(data);

      return data;

    } finally {

      setLoading(false);

    }

  };



  const register = async (userData) => {

    return await authService.register(userData);

  };



  const logout = () => {

    authService.logout();

    setUser(null);

  };



  const hasRole = (allowedRoles) => {

    if (!user) return false;

    return allowedRoles.includes(user.role);

  };



  return (

    <AuthContext.Provider value={{ user, loading, login, register, logout, hasRole }}>

      {children}

    </AuthContext.Provider>

  );

};



export const useAuth = () => {

  const context = useContext(AuthContext);

  if (!context) {

    throw new Error('useAuth must be used within an AuthProvider');

  }

  return context;

};
