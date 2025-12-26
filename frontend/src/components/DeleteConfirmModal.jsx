import { Button } from "./Button";

const DeleteConfirmModal = ({ isOpen, transactionInfo, onConfirm, onCancel }) => {
  if (!isOpen) return null;

  return (
    <div className="z-100 fixed inset-0 bg-black/50 flex justify-center items-center p-4">
      <div className="bg-white rounded-xl p-6 w-full max-w-md shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Удалить операцию?</h2>

        <div className="mb-4 text-gray-700">
          <p><strong>Категория:</strong> {transactionInfo?.category}</p>
          <p><strong>Сумма:</strong> {transactionInfo?.amount} ₽</p>
          <p><strong>Дата:</strong> {transactionInfo?.date}</p>
        </div>

        <div className="flex justify-end gap-3">
          <Button variant="primary" onClick={onCancel}>
            Отмена
          </Button>

          <Button variant="danger" onClick={() => onConfirm(transactionInfo)}>
            Удалить
          </Button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;
