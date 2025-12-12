import { useState, useEffect } from "react";
import Spinner from "./Spinner";
import ErrorMessage from "./ErrorMessage";
import { Button } from "./Button";

const Transaction = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    setTimeout(() => {
      try {
        const data = [
          {
            name: "Политех",
            type: "Стипендия",
            date: "20.11.2025",
            amount: 3000,
          },
        ];

        setTransactions(data);

        setLoading(false);
      } catch (e) {
        setError("Ошибка загрузки транзакций");
        setLoading(false);
      }
    }, 800);
  }, []);

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;

  if (transactions.length === 0) {
    return (
      <div className="p-6 bg-white rounded-xl shadow text-gray-500">
        Транзакций пока нет
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Финансовые операции</h1>

      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full table-auto">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase border-b">
                Название
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase border-b">
                Тип
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase border-b">
                Дата
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase border-b">
                Сумма
              </th>
            </tr>
          </thead>

          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((t, index) => (
              <tr key={index} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 text-sm font-medium">{t.name}</td>
                <td className="px-6 py-4 text-sm text-gray-500">{t.type}</td>
                <td className="px-6 py-4 text-sm text-gray-500">{t.date}</td>
                <td className="px-6 py-4 text-sm font-semibold text-green-600">
                  {t.amount} ₽
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Button variant="yellow" className="mt-5">Добавить доход</Button>
    </div>
  );
};

export default Transaction;
