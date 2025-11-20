import Coin from "../assets/images/coin.png";

const Balance = () => {
  return (
    <div className="flex flex-col gap-y-10 p-5 bg-gradient-to-b from-[#FFFCF6] to-[#FFF0DB] rounded-lg">
        <div className="flex items-end gap-x-20">
            <div className="flex flex-col gap-y-5">
                <p className="font-montserrat font-semibold text-2xl">Текущий баланс</p>
                <h1 className="font-montserrat font-semibold text-5xl">200000 ₽</h1>
            </div>
            <img src={Coin} alt="ava" className="" />
        </div>
        <div className="flex gap-x-10">
            <div className="flex flex-col">
                <p className="font-montserrat font-semibold text-2xl">250000 ₽</p>
                <h1 className="font-montserrat font-regular text-xl">доход</h1>
            </div>
            <div className="flex flex-col">
                <p className="font-montserrat font-semibold text-2xl">170000 ₽</p>
                <h1 className="font-montserrat font-regular text-xl">доход</h1>
            </div>
            <div className="flex flex-col">
                <p className="font-montserrat font-semibold text-2xl">10000 ₽</p>
                <h1 className="font-montserrat font-regular text-xl">доход</h1>
            </div>
        </div>
    </div>
  );
};

export default Balance;