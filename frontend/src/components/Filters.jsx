import { Button } from "./Button";

const Filters = ({ filters, setFilters, resetFilters }) => {
  return (
    <div className="flex flex-wrap gap-3 items-end bg-white p-4 rounded-xl shadow w-full">

      {/* Поиск */}
      <div className="flex flex-col min-w-[140px] flex-1 sm:flex-none">
        <label className="text-sm font-medium">Поиск</label>
        <input
          type="text"
          className="border rounded-xl px-3 py-2 text-sm"
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          placeholder="Введите описание"
        />
      </div>

      {/* Тип */}
      <div className="flex flex-col min-w-[120px] flex-1 sm:flex-none">
        <label className="text-sm font-medium">Тип</label>
        <select
          className="border rounded-xl px-3 py-2 text-sm"
          value={filters.type}
          onChange={(e) => setFilters({ ...filters, type: e.target.value })}
        >
          <option value="">Все</option>
          <option value="income">Доход</option>
          <option value="expense">Расход</option>
        </select>
      </div>

      {/* Категория */}
      <div className="flex flex-col min-w-[120px] flex-1 sm:flex-none">
        <label className="text-sm font-medium">Категория</label>
        <select
          className="border rounded-xl px-3 py-2 text-sm"
          value={filters.category}
          onChange={(e) => setFilters({ ...filters, category: e.target.value })}
        >
          <option value="">Все</option>
          {["Еда","Транспорт","Зарплата","Покупки","Развлечения","Путешествия"].map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {/* Дата ОТ */}
      <div className="flex flex-col min-w-[140px] flex-1 sm:flex-none">
        <label className="text-sm font-medium">Дата от</label>
        <input
          type="date"
          className="border rounded-xl px-3 py-2 text-sm"
          value={filters.dateFrom}
          onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
        />
      </div>

      {/* Дата ДО */}
      <div className="flex flex-col min-w-[140px] flex-1 sm:flex-none">
        <label className="text-sm font-medium">Дата до</label>
        <input
          type="date"
          className="border rounded-xl px-3 py-2 text-sm"
          value={filters.dateTo}
          onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
        />
      </div>

      {/* Кнопка сброса всегда справа */}
      <div className="w-full sm:w-auto sm:ml-auto">
        <Button
          variant="primary"
          onClick={resetFilters}
          className="w-full sm:w-auto px-4 py-2 text-sm"
        >
          Сбросить
        </Button>
      </div>

    </div>
  );
};

export default Filters;
