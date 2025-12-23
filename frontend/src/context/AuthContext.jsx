import { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [appLoading, setAppLoading] = useState(true);
    const [authLoading, setAuthLoading] = useState(false);
    const [error, setError] = useState(null);

  // Проверяем авторизацию при загрузке
    useEffect(() => {
        const initAuth = async () => {
            if (authService.isAuthenticated()) {
                try {
                    const userData = await authService.getProfile();
                    setUser(userData);
                } 
                catch (err) {
                    console.error('Failed to get profile:', err);
                    authService.logout();
                }
            }
            setAppLoading(false);
        };
        initAuth();
    }, []);

    // Функция входа
    const login = async (credentials) => {
        setError(null);
        setAuthLoading(true);
        try {
            const result = await authService.login(credentials);
            if (result.success) {
                setUser(result.user);
                return { success: true };
            } else {
                setError(result.error.message || 'Ошибка входа');
                return { success: false, error: result.error };
            }
        } 
        catch (err) {
            const errorMessage = 'Неизвестная ошибка входа';
            setError(errorMessage);
            return { success: false, error: { message: errorMessage } };
        } 
        finally {
            setAuthLoading(false);
        }
    };

    // Функция регистрации
    const register = async (userData) => {
        setError(null);
        setAuthLoading(true);
        try {
            const result = await authService.register(userData);
            if (result.success) {
                return { success: true, message: result.message };
            } else {
                setError(result.error.message || 'Ошибка регистрации');
                return { success: false, error: result.error };
            }
        } 
        catch (err) {
            const errorMessage = 'Неизвестная ошибка регистрации';
            setError(errorMessage);
            return { success: false, error: { message: errorMessage } };
        } 
        finally {
            setAuthLoading(false)
        }
    };

    // Функция выхода
    const logout = () => {
        authService.logout();
        setUser(null);
    };

    const value = {
        user,
        appLoading,
        authLoading,
        error,
        login,
        register,
        logout,
        isAuthenticated: !!user,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}