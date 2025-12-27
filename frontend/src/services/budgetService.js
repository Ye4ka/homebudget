import api from './api';

const budgetService = {
    /**
     * Получает список всех бюджетов пользователя.
     *
     * @returns {Promise<{success: boolean, data?: Object[], error?: Object}>}
     */
    async getBudgets() {
        try {
        const response = await api.get('/budgets/');
        return {
            success: true,
            data: response.data,
        };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка получения бюджетов' },
            };
        }
    },

    /**
     * Получает данные одного бюджета по id.
     *
     * @param {number|string} budgetId ID бюджета
     * @returns {Promise<{success: boolean, data?: Object, error?: Object}>}
     */
    async getBudget(budgetId) {
        try {
            const response = await api.get(`/budgets/${budgetId}/`);
            return {
                success: true,
                data: response.data,
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка получения бюджета' },
            };
        }
    },

    /**
     * Создаёт новый бюджет.
     *
     * @param {Object} budgetData
     * @param {string} budgetData.name Название бюджета
     * @param {string} budgetData.type Тип бюджета
     * @param {string} budgetData.currency Валюта
     */
    async createBudget(budgetData) {
        try {
            const response = await api.post('/budgets/', budgetData);
            return {
                success: true,
                data: response.data,
                message: 'Бюджет успешно создан',
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка создания бюджета' },
            };
        }
    },

    /**
     * Обновляет существующий бюджет.
     *
     * @param {number|string} budgetId
     * @param {Object} budgetData
     */
    async updateBudget(budgetId, budgetData) {
        try {
            const response = await api.patch(`/budgets/${budgetId}/`, budgetData);
            return {
                success: true,
                data: response.data,
                message: 'Бюджет успешно обновлён',
            };
        } catch (error) {
            return {
            success: false,
            error: error.response?.data || { message: 'Ошибка обновления бюджета' },
            };
        }
    },

    /**
     * Удаляет бюджет.
     *
     * @param {number|string} budgetId
     */
    async deleteBudget(budgetId) {
        try {
            await api.delete(`/budgets/${budgetId}/`);
            return {
                success: true,
                message: 'Бюджет успешно удалён',
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка удаления бюджета' },
            };
        }
    },

    /**
     * Получает сводку по бюджету за указанный период.
     *
     * @param {number|string} budgetId
     * @param {string|null} dateFrom YYYY-MM-DD
     * @param {string|null} dateTo YYYY-MM-DD
     */
    async getBudgetSummary(budgetId, dateFrom = null, dateTo = null) {
        try {
            const params = {};
            if (dateFrom) params.date_from = dateFrom;
            if (dateTo) params.date_to = dateTo;

            const response = await api.get(`/budgets/${budgetId}/summary/`, { params });

            return {
                success: true,
                data: response.data,
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data || { message: 'Ошибка получения сводки' },
            };
        }
    },
    
    /**
     * Получает сводку по бюджету за текущий месяц.
     *
     * @param {number|string} budgetId
     */
    async getCurrentMonthSummary(budgetId) {
        try {
            const now = new Date();
            const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
            const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);

            const dateFrom = firstDay.toISOString().split('T')[0];
            const dateTo = lastDay.toISOString().split('T')[0];

            return await this.getBudgetSummary(budgetId, dateFrom, dateTo);
        } catch (error) {
            return {
                success: false,
                error: { message: 'Ошибка получения сводки за месяц' },
            };
        }
    },
};

export default budgetService;