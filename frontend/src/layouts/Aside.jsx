import Avatar from "../assets/images/ava.png";
import Dash from "../assets/images/dashboard.png";
import Operation from "../assets/images/operation.svg";
import Analyst from "../assets/images/analys.png";
import Plane from "../assets/images/Plane.svg";
import Settings from "../assets/images/settings.png";
import Quit from "../assets/images/quit.png";

const Aside = () => {
  return (
    <div className="flex flex-col gap-y-20">
        <div className="flex flex-col justify-between gap-y-5">
            <img src={Avatar} alt="ava" className="w-18 h-18 rounded-full" />
            <p className="font-montserrat font-bold">Данил Камерунин</p>
        </div>
        <div className="flex flex-col gap-y-3">
            <div className="flex items-center gap-x-3">
                <img src={Dash} alt="ava" className="" />
                <p className="font-montserrat font-regular">главная страница</p>
            </div>
            <div className="flex items-center gap-x-3">
                <img src={Operation} alt="ava" className="" />
                <p className="font-montserrat font-regular">операции</p>
            </div>
            <div className="flex items-center gap-x-3">
                <img src={Analyst} alt="ava" className="" />
                <p className="font-montserrat font-regular">анализ</p>
            </div>
            <div className="flex items-center gap-x-3">
                <img src={Plane} alt="ava" className="" />
                <p className="font-montserrat font-regular">планирование</p>
            </div>
        </div>
        <div className="flex flex-col gap-y-3">
            <div className="flex items-center gap-x-3">
                <img src={Settings} alt="ava" className="" />
                <p className="font-montserrat font-regular">настройки</p>
            </div>
            <div className="flex items-center gap-x-3">
                <img src={Quit} alt="ava" className="" />
                <p className="font-montserrat font-regular">выйти</p>
            </div>
        </div>
    </div>
  );
};

export default Aside;