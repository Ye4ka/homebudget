import { Button } from "./Button";

const TransactionTable = ({ loading, error, data, onEdit, onDelete }) => {
  if (loading) {
    return (
      <div className="p-5 text-center text-gray-500 bg-white rounded-xl shadow">
        Загрузка операций...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-5 text-center text-red-500 bg-white rounded-xl shadow">
        Ошибка загрузки операций
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto pr-3 sm:pr-4">
      <table className="w-full bg-white rounded-xl shadow overflow-hidden">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-3 text-left">Дата</th>
            <th className="p-3 text-left">Категория</th>
            <th className="p-3 text-left">Тип</th>
            <th className="p-3 text-left">Сумма</th>
            <th className="p-3 text-left">Описание</th>
            <th className="p-3 text-left">Действия</th>
          </tr>
        </thead>

        <tbody>
          {data.map((tx) => (
            <tr key={tx.id} className="border-t">
              <td className="p-3">{tx.date}</td>
              <td className="p-3">{tx.category}</td>

              <td className="p-3">
                {tx.type === "income" ? (
                  <span className="text-green-600 font-semibold">Доход</span>
                ) : (
                  <span className="text-red-500 font-semibold">Расход</span>
                )}
              </td>

              <td className="p-3 font-semibold">
                {tx.type === "income" ? (
                  <span className="text-green-600">+{tx.amount} ₽</span>
                ) : (
                  <span className="text-red-500">{tx.amount} ₽</span>
                )}
              </td>

              <td className="p-3 text-gray-700">{tx.description || "—"}</td>

              {/* Кнопки */}
              <td className="p-3">
                <div className="flex gap-2">
                  <Button
                    variant="primary"
                    className="w-auto px-3 py-1 text-sm"
                    onClick={() => onEdit(tx)}
                  >
                    Редактировать
                  </Button>

                  <Button
                    variant="danger"
                    className="w-auto px-3 py-1 text-sm"
                    onClick={() => onDelete(tx)}
                  >
                    Удалить
                  </Button>
                </div>
              </td>
            </tr>
          ))}

          {data.length === 0 && (
            <tr>
              <td colSpan="6" className="p-5 text-center text-gray-500">
                Нет операций по текущим фильтрам
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionTable;
