import Logo from "../assets/images/Logo.png";

const Header = () => {
  return (
    <header className="flex justify-between items-center mt-5 px-3 sm:px-5">
      <img src={Logo} className="w-36 sm:w-44" alt="Logo" />

      <div className="text-base sm:text-xl font-semibold text-right">
        Баланс: <span className="text-green-600">200 000 ₽</span>
      </div>
    </header>
  );
};

export default Header;
