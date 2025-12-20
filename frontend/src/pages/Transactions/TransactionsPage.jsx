// TransactionsPage.jsx — объединённый финальный вариант
import { useState, useEffect, useMemo } from "react";
import Filters from "../../components/Filters";
import TransactionTable from "../../components/TransactionTable";
import TransactionForm from "../../components/forms/TransactionForm";
import DeleteConfirmModal from "../../components/DeleteConfirmModal";
import { Button } from "../../components/Button";

const TransactionsPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const [transactions, setTransactions] = useState([]);

  // ------------------ Фильтры ------------------
  const [filters, setFilters] = useState({
    type: "",
    category: "",
    search: "",
    dateFrom: "",
    dateTo: "",
  });

  const resetFilters = () => {
    setFilters({
      type: "",
      category: "",
      search: "",
      dateFrom: "",
      dateTo: "",
    });
  };

  // ------------------ CRUD модалки ------------------
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedTx, setSelectedTx] = useState(null);

  // ------------------ Имитируем загрузку ------------------
  useEffect(() => {
    setTimeout(() => {
      // setError(true); // тест ошибки

      setTransactions([
        {
          id: 1,
          date: "2025-01-01",
          category: "Зарплата",
          amount: 120000,
          type: "income",
          description: "Основная зарплата",
        },
        {
          id: 2,
          date: "2025-01-02",
          category: "Еда",
          amount: -3500,
          type: "expense",
          description: "Пятёрочка",
        },
        {
          id: 3,
          date: "2025-01-04",
          category: "Фриланс",
          amount: 28000,
          type: "income",
          description: "Проект от клиента",
        },
      ]);

      setLoading(false);
    }, 600);
  }, []);

  // ------------------ Фильтрация (фронтенд) ------------------
  const filteredTransactions = useMemo(() => {
    return transactions.filter((t) => {
      // тип
      if (filters.type && t.type !== filters.type) return false;

      // категория
      if (filters.category && t.category !== filters.category) return false;

      // поиск
      if (filters.search && !t.description.toLowerCase().includes(filters.search.toLowerCase()))
        return false;

      // даты
      if (filters.dateFrom && t.date < filters.dateFrom) return false;
      if (filters.dateTo && t.date > filters.dateTo) return false;

      return true;
    });
  }, [filters, transactions]);

  // ------------------ Создание / редактирование ------------------
  const handleSubmit = (data) => {
    if (selectedTx) {
      // edit
      setTransactions((prev) =>
        prev.map((tx) => (tx.id === selectedTx.id ? { ...tx, ...data } : tx))
      );
    } else {
      // create
      setTransactions((prev) => [
        ...prev,
        {
          id: Date.now(),
          ...data,
        },
      ]);
    }

    setSelectedTx(null);
    setIsFormOpen(false);
  };

  // ------------------ Удаление ------------------
  const handleDelete = () => {
    setTransactions((prev) => prev.filter((tx) => tx.id !== selectedTx.id));
    setSelectedTx(null);
    setIsDeleteOpen(false);
  };

  return (
    <div className="w-full flex flex-col gap-y-6 sm:gap-y-10 px-2 sm:px-0">

      {/* Заголовок + кнопка */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <h1 className="font-montserrat text-2xl sm:text-4xl font-semibold">
          Операции
        </h1>

        <Button
          variant="yellow"
          className="w-full sm:w-auto"
          onClick={() => {
            setSelectedTx(null);
            setIsFormOpen(true);
          }}
        >
          Добавить операцию
        </Button>
      </div>

      {/* Фильтры */}
      <div className="overflow-x-auto">
        <Filters
          filters={filters}
          setFilters={setFilters}
          resetFilters={resetFilters}
        />
      </div>

      {/* Таблица */}
      <div className="overflow-x-auto">
        <TransactionTable
          loading={loading}
          error={error}
          data={filteredTransactions}
          onEdit={(tx) => {
            setSelectedTx(tx);
            setIsFormOpen(true);
          }}
          onDelete={(tx) => {
            setSelectedTx(tx);
            setIsDeleteOpen(true);
          }}
        />
      </div>

      {/* Модалки */}
      <TransactionForm
        isOpen={isFormOpen}
        mode={selectedTx ? "edit" : "create"}
        transaction={selectedTx}
        onSubmit={handleSubmit}
        onCancel={() => {
          setSelectedTx(null);
          setIsFormOpen(false);
        }}
      />

      <DeleteConfirmModal
        isOpen={isDeleteOpen}
        transactionInfo={selectedTx}
        onConfirm={handleDelete}
        onCancel={() => setIsDeleteOpen(false)}
      />
    </div>
  );

};

export default TransactionsPage;
