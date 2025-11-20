const FastAction = () => {
  return (
    <div className="flex flex-col gap-y-5">
        <h2 className="font-montserrat font-semibold text-2xl">Быстрые действия</h2>
        <input
        type="text"
        className="border border-black/20 p-2 rounded w-74"
        placeholder="Введите сумму..."
        />
        <button className="px-5 py-3 bg-green-500 font-montserrat font-medium w-74 rounded-2xl text-white">Добавить доход</button>
        <button className="px-5 py-3 bg-red-500 font-montserrat font-medium w-74 rounded-2xl text-white">Добавить расход</button>
    </div>
  );
};

export default FastAction;