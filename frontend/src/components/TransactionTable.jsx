const TransactionTable = ({ data }) => {
  return (
    <table className="w-full bg-white rounded-xl shadow overflow-hidden">
      <thead className="bg-gray-100">
        <tr>
          <th className="p-3 text-left">Дата</th>
          <th className="p-3 text-left">Категория</th>
          <th className="p-3 text-left">Тип</th>
          <th className="p-3 text-left">Сумма</th>
          <th className="p-3 text-left">Описание</th>
        </tr>
      </thead>

      <tbody>
        {data.map((t) => (
          <tr key={t.id} className="border-t">
            <td className="p-3">{t.date}</td>

            <td className="p-3">{t.category}</td>

            <td className="p-3">
              {t.type === "income" ? (
                <span className="text-green-600 font-semibold">Доход</span>
              ) : (
                <span className="text-red-500 font-semibold">Расход</span>
              )}
            </td>

            <td className="p-3 font-semibold">
              {t.type === "income" ? (
                <span className="text-green-600">+{t.amount} ₽</span>
              ) : (
                <span className="text-red-500">-{t.amount} ₽</span>
              )}
            </td>

            <td className="p-3 text-gray-700">{t.description}</td>
          </tr>
        ))}

        {data.length === 0 && (
          <tr>
            <td colSpan="5" className="p-5 text-center text-gray-500">
              Нет операций по текущим фильтрам
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
};

export default TransactionTable;
