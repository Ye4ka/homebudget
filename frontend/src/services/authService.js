import api from './api';

const authService = {
    async register(userData) {
        /**
         * Регистрирует нового пользователя.
         *
         * @param {Object} userData Данные пользователя
         * @param {string} userData.email Email пользователя
         * @param {string} userData.password Пароль
         * @param {string} userData.password Подтверждение Пароля
         * @param {string} userData.first_name Имя
         * @param {string} userData.last_name Фамилия
         * @returns {Promise<{success: boolean, data?: Object, error?: Object}>}
         */

        try {
            const response = await api.post('/users/register/', {
                email: userData.email,
                password: userData.password,
                password2: userData.password2,
                first_name: userData.first_name,
                last_name: userData.last_name,
            });

            return {
            success: true,
            data: response.data,
            message: 'Регистрация успешна! Теперь войдите в систему.',
            };
        } 
        catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка регистрации' },
            };
        }
    },
    
    /**
     * Авторизует пользователя, сохраняет JWT-токены и загружает профиль.
     *
     * @param {Object} credentials Данные для входа
     * @param {string} credentials.email Email пользователя
     * @param {string} credentials.password Пароль пользователя
     * @returns {Promise<{success: boolean, user?: Object, error?: Object}>}
     */
    async login(credentials) {
        try {
            const response = await api.post('/token/', {
                email: credentials.email,
                password: credentials.password,
            });

            const { access, refresh } = response.data;

            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            const user = await this.getProfile();

            return {
                success: true,
                user,
            };
        } 
        catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка входа' },
            };
        }
    },

    async getProfile() {
        try {
            const response = await api.get('/users/profile/');
            return response.data;
        } 
        catch (error) {
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    },

    getAccessToken() {
        return localStorage.getItem('access_token');
    },
};

export default authService;