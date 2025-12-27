import { useEffect, useState } from "react";
import budgetService from "../services/budgetService";
import Coin from "../assets/images/coin.png";

const Balance = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    loadBalanceData();
  }, []);

  const loadBalanceData = async () => {
    setLoading(true);
    setError(false);

    try {
      // Получаем бюджеты пользователя
      const budgetsResult = await budgetService.getBudgets();

      if (!budgetsResult.success || !budgetsResult.data.length) {
        // Если нет бюджетов - показываем 0
        setData({
          balance: 0,
          income: 0,
          expense: 0,
          savings: 0,
        });
        setLoading(false);
        return;
      }

      const firstBudget = budgetsResult.data[0];
      const budgetId = firstBudget.id;

      // Загружаем сводку за текущий месяц
      const summaryResult = await budgetService.getCurrentMonthSummary(budgetId);

      if (summaryResult.success) {
        const summary = summaryResult.data;

        setData({
          balance: parseFloat(summary.balance),
          income: parseFloat(summary.total_income),
          expense: parseFloat(summary.total_expense),
          savings: 0, // TODO: можно добавить логику накоплений
        });
      } else {
        setError(true);
      }
    } catch (err) {
      console.error('Error loading balance:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return (
      <div className="p-6 bg-white rounded-lg shadow-md text-center">
        <p className="animate-pulse text-gray-500">Загрузка баланса…</p>
      </div>
    );

  if (error) {
    return (
      <div className="p-6 bg-red-100 text-red-600 font-medium rounded-lg">
        <p>Ошибка загрузки баланса</p>
        <button
          onClick={loadBalanceData}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Повторить
        </button>
      </div>
    );
  }

  if (!data)
    return (
      <div className="p-6 text-center text-gray-500 bg-white rounded-lg">
        Нет данных о балансе
      </div>
    );

  return (
    <div className="flex flex-col gap-y-10 p-3 md:p-5 bg-linear-to-b from-[#FFFCF6] to-[#FFF0DB] rounded-lg">
      <div className="flex items-end gap-x-10 md:gap-x-20">
        <div className="flex flex-col gap-y-5">
          <p className="font-montserrat font-semibold text-xl md:text-2xl">Текущий баланс</p>
          <h1 className="font-montserrat font-semibold text-4xl md:text-5xl">
            {data.balance.toLocaleString('ru-RU')} ₽
          </h1>
        </div>
        <img src={Coin} alt="coin" className="w-32" />
      </div>

      <div className="flex gap-x-5 md:gap-x-10">
        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-xl md:text-2xl text-green-600">
            +{data.income.toLocaleString('ru-RU')} ₽
          </p>
          <h1 className="font-montserrat">доход</h1>
        </div>

        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-xl md:text-2xl text-red-600">
            -{data.expense.toLocaleString('ru-RU')} ₽
          </p>
          <h1 className="font-montserrat">расход</h1>
        </div>

        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-xl md:text-2xl">
            {data.savings.toLocaleString('ru-RU')} ₽
          </p>
          <h1 className="font-montserrat">накопления</h1>
        </div>
      </div>
    </div>
  );
};

export default Balance;