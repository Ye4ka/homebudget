import { Link } from "react-router-dom";

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

      {/* user */}
      <div className="flex flex-col justify-between gap-y-5">
        <img src={Avatar} alt="ava" className="w-18 h-18 rounded-full" />
        <p className="font-montserrat font-bold">Данил Камерунин</p>
      </div>

      {/* navigation */}
      <div className="flex flex-col gap-y-3">

        <Link
          to="/dashboard"
          className="flex items-center gap-x-3 hover:opacity-80 transition"
        >
          <img src={Dash} alt="" />
          <p className="font-montserrat font-regular">главная страница</p>
        </Link>

        <Link
          to="/transactions"
          className="flex items-center gap-x-3 hover:opacity-80 transition"
        >
          <img src={Operation} alt="" />
          <p className="font-montserrat font-regular">операции</p>
        </Link>

        <Link
          to="/analytics"
          className="flex items-center gap-x-3 hover:opacity-80 transition"
        >
          <img src={Analyst} alt="" />
          <p className="font-montserrat font-regular">анализ</p>
        </Link>

        <Link
          to="/planning"
          className="flex items-center gap-x-3 hover:opacity-80 transition"
        >
          <img src={Plane} alt="" />
          <p className="font-montserrat font-regular">планирование</p>
        </Link>

      </div>

      {/* settings + quit */}
      <div className="flex flex-col gap-y-3">

        <Link
          to="/settings"
          className="flex items-center gap-x-3 hover:opacity-80 transition"
        >
          <img src={Settings} alt="" />
          <p className="font-montserrat font-regular">настройки</p>
        </Link>

        <div
          className="flex items-center gap-x-3 hover:opacity-80 cursor-pointer transition"
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
        >
          <img src={Quit} alt="" />
          <p className="font-montserrat font-regular">выйти</p>
        </div>

      </div>
    </div>
  );
};

export default Aside;
