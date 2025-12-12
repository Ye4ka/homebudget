import { useForm } from "react-hook-form";
import { Button } from "../Button";

const categories = [
  "Еда",
  "Транспорт",
  "Зарплата",
  "Покупки",
  "Развлечения",
  "Путешествия",
];

const TransactionForm = ({ isOpen, mode = "create", transaction = {}, onSubmit, onCancel }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm({
    defaultValues: transaction || {},
  });

  if (!isOpen) return null;

  const submitHandler = (data) => {
    const payload = {
      ...data,
      amount: Number(data.amount),
    };
    onSubmit(payload);
    reset();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-center items-center p-4">
      <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-lg">
        <h2 className="text-xl font-semibold mb-4">
          {mode === "create" ? "Добавить операцию" : "Редактировать операцию"}
        </h2>

        <form className="flex flex-col gap-4" onSubmit={handleSubmit(submitHandler)}>
          
          {/* Amount */}
          <div className="flex flex-col">
            <label className="font-medium">Сумма</label>
            <input
              type="number"
              className="border rounded-xl px-3 py-2"
              {...register("amount", { required: true, min: 1 })}
            />
            {errors.amount && (
              <p className="text-red-500 text-sm">Введите сумму больше 0</p>
            )}
          </div>

          {/* Category */}
          <div className="flex flex-col">
            <label className="font-medium">Категория</label>
            <select
              className="border rounded-xl px-3 py-2"
              {...register("category", { required: true })}
            >
              <option value="">Выберите категорию</option>
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
            {errors.category && (
              <p className="text-red-500 text-sm">Выберите категорию</p>
            )}
          </div>

          {/* Type */}
          <div className="flex flex-col">
            <label className="font-medium">Тип</label>
            <select
              className="border rounded-xl px-3 py-2"
              {...register("type", { required: true })}
            >
              <option value="income">Доход</option>
              <option value="expense">Расход</option>
            </select>
          </div>

          {/* Date */}
          <div className="flex flex-col">
            <label className="font-medium">Дата</label>
            <input
              type="date"
              className="border rounded-xl px-3 py-2"
              {...register("date", { required: true })}
            />
            {errors.date && (
              <p className="text-red-500 text-sm">Укажите дату</p>
            )}
          </div>

          {/* Description */}
          <div className="flex flex-col">
            <label className="font-medium">Описание</label>
            <textarea
              className="border rounded-xl px-3 py-2 resize-none h-24"
              {...register("description")}
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-4 justify-end mt-4">
            <Button variant="danger" onClick={onCancel} type="button">
              Отмена
            </Button>

            <Button variant="primary" type="submit">
              Сохранить
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TransactionForm;
