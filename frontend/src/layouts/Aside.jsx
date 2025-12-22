import { Link } from "react-router-dom";
import { useState } from "react";

import Avatar from "../assets/images/ava.png";
import Dash from "../assets/images/dashboard.png";
import Operation from "../assets/images/operation.svg";
import Analyst from "../assets/images/analys.png";
import Plane from "../assets/images/Plane.svg";
import Settings from "../assets/images/settings.png";
import Quit from "../assets/images/quit.png";

const Aside = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        className="sm:hidden fixed left-0 top-1/2 -translate-y-1/2 z-50
                   bg-white shadow-md rounded-r-xl px-2 py-4"
      >
        <span
          className={`block transition-transform duration-300 ${
            open ? "rotate-180" : ""
          }`}
        >
          ▶
        </span>
      </button>

      <aside
        className={`
          fixed sm:static top-0 left-0 z-40
          h-full sm:h-auto
          w-64 bg-white
          px-6 py-8
          flex flex-col gap-y-20
          transition-transform duration-300
          ${open ? "translate-x-0" : "-translate-x-full"}
          sm:translate-x-0
        `}
      >
        <div className="flex flex-col gap-y-5 items-center sm:items-start">
          <img src={Avatar} alt="ava" className="w-18 h-18 rounded-full" />
          <p className="font-montserrat font-bold">Данил Камерунин</p>
        </div>

        <nav className="flex flex-col gap-y-3">
          <NavItem to="/dashboard" icon={Dash} label="главная страница" />
          <NavItem to="/transactions" icon={Operation} label="операции" />
          <NavItem to="/analytics" icon={Analyst} label="анализ" />
          <NavItem to="/planning" icon={Plane} label="планирование" />
        </nav>

        <div className="flex flex-col gap-y-3 mt-auto">
          <NavItem to="/settings" icon={Settings} label="настройки" />

          <button
            className="flex items-center gap-x-3 hover:opacity-80 transition"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
          >
            <img src={Quit} alt="" />
            <p className="font-montserrat font-regular">выйти</p>
          </button>
        </div>
      </aside>

      {open && (
        <div
          className="sm:hidden fixed inset-0 bg-black/30 z-30"
          onClick={() => setOpen(false)}
        />
      )}
    </>
  );
};

const NavItem = ({ to, icon, label }) => (
  <Link
    to={to}
    className="flex items-center gap-x-3 hover:opacity-80 transition"
  >
    <img src={icon} alt="" />
    <p className="font-montserrat font-regular">{label}</p>
  </Link>
);

export default Aside;
