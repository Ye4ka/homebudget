import { useEffect, useState } from "react";
import Coin from "../assets/images/coin.png";

const Balance = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    setTimeout(() => {
      setData({
        balance: 200000,
        income: 250000,
        expense: 170000,
        savings: 10000,
      });

      setLoading(false);
    }, 800);
  }, []);

  if (loading)
    return (
      <div className="p-6 bg-white rounded-lg shadow-md text-center">
        <p className="animate-pulse text-gray-500">Загрузка баланса…</p>
      </div>
    );

  if (error)
    return (
      <div className="p-6 bg-red-100 text-red-600 font-medium rounded-lg">
        Ошибка загрузки баланса
      </div>
    );

  if (!data)
    return (
      <div className="p-6 text-center text-gray-500 bg-white rounded-lg">
        Нет данных о балансе
      </div>
    );

  return (
    <div className="flex flex-col gap-y-10 p-5 bg-gradient-to-b from-[#FFFCF6] to-[#FFF0DB] rounded-lg">
      <div className="flex items-end gap-x-20">
        <div className="flex flex-col gap-y-5">
          <p className="font-montserrat font-semibold text-2xl">Текущий баланс</p>
          <h1 className="font-montserrat font-semibold text-5xl">
            {data.balance} ₽
          </h1>
        </div>
        <img src={Coin} alt="coin" />
      </div>

      <div className="flex gap-x-10">
        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-2xl">
            {data.income} ₽
          </p>
          <h1 className="font-montserrat text-xl">доход</h1>
        </div>

        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-2xl">
            {data.expense} ₽
          </p>
          <h1 className="font-montserrat text-xl">расход</h1>
        </div>

        <div className="flex flex-col">
          <p className="font-montserrat font-semibold text-2xl">
            {data.savings} ₽
          </p>
          <h1 className="font-montserrat text-xl">накопления</h1>
        </div>
      </div>
    </div>
  );
};

export default Balance;
