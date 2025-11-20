const Transaction = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto">
    <h1 className="text-2xl font-bold mb-6 text-gray-800">Финансовые операции</h1>
    
    <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full table-auto">
        <thead className="bg-gray-50">
            <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                Название
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                Тип
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                Дата
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                Сумма
            </th>
            </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
            <tr className="hover:bg-gray-50 transition-colors">
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Политех
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                Стипендия
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                20.11.2025
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                3000 ₽
            </td>
            </tr>
            <tr className="hover:bg-gray-50 transition-colors">
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Политех
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                Стипендия
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                20.11.2025
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                3000 ₽
            </td>
            </tr>
            <tr className="hover:bg-gray-50 transition-colors">
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Политех
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                Стипендия
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                20.11.2025
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                3000 ₽
            </td>
            </tr>
            <tr className="hover:bg-gray-50 transition-colors">
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Политех
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                Стипендия
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                20.11.2025
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                3000 ₽
            </td>
            </tr>
        </tbody>
        </table>
    </div>

    <button className="px-5 py-3 bg-yellow-500 font-montserrat font-medium w-74 rounded-2xl text-white mt-10">Загрузить ещё</button>
    </div>
  );
};

export default Transaction;