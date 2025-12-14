import axios from 'axios';

/**
 * Глобальный HTTP-клиент приложения на базе axios.
 *
 * Автоматически:
 * - подставляет access token в Authorization заголовок
 * - обновляет access token при 401 ошибке
 * - перенаправляет на /login при невалидном refresh token
 *
 * Используется во всех сервисах для работы с API.
 */

const API_URL = 'http://localhost:8000/api';

// базовый экземпляр axios
const api = axios.create({
    baseURL: API_URL,
    headers: {
    'Content-Type': 'application/json',
    },
});

/**
 * Request interceptor.
 * Добавляет Authorization заголовок с access token, если пользователь авторизован.
 */
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

/**
 * Response interceptor.
 * При 401 ошибке пытается обновить access token и повторить оригинальный запрос.
 */
api.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Если 401 и это не повторный запрос
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
            
                if (!refreshToken) {
                    throw new Error('No refresh token');
                }

                // Пытаемся обновить токен
                const response = await axios.post(
                    'http://localhost:8000/api/token/refresh/',
                    { refresh: refreshToken }
                );

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                // Повторяем оригинальный запрос с новым токеном
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            }

            catch (refreshError) {
                // Если обновление токена не удалось - выходим
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default api;