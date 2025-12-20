const Filters = ({ filters, setFilters, resetFilters }) => {
  const categories = ["Зарплата", "Еда", "Фриланс"];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 sm:gap-5 bg-white p-4 sm:p-5 rounded-xl shadow">


      {/* поиск */}
      <input
        type="text"
        placeholder="Поиск по описанию..."
        className="border p-2 rounded-lg"
        value={filters.search}
        onChange={(e) => setFilters({ ...filters, search: e.target.value })}
      />

      {/* тип */}
      <select
        className="border p-2 rounded-lg"
        value={filters.type}
        onChange={(e) => setFilters({ ...filters, type: e.target.value })}
      >
        <option value="">Тип</option>
        <option value="income">Доход</option>
        <option value="expense">Расход</option>
      </select>

      {/* категория */}
      <select
        className="border p-2 rounded-lg"
        value={filters.category}
        onChange={(e) => setFilters({ ...filters, category: e.target.value })}
      >
        <option value="">Категория</option>
        {categories.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>

      {/* от */}
      <input
        type="date"
        className="border p-2 rounded-lg"
        value={filters.dateFrom}
        onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
      />

      {/* до */}
      <input
        type="date"
        className="border p-2 rounded-lg"
        value={filters.dateTo}
        onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
      />

      {/* кнопка сброс */}
      <button
        className="sm:col-span-5 bg-gray-200 p-3 rounded-lg hover:bg-gray-300 transition"
        onClick={resetFilters}
      >
        Сбросить фильтры
      </button>

    </div>
  );
};

export default Filters;
