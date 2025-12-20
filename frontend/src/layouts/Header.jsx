import Logo from "../assets/images/Logo.png";

const Header = () => {
  return (
    <div className="flex justify-between items-center mt-5">
      <img src={Logo} className="w-38 sm:w-44" />

      <div className="sm:text-xl font-semibold">
        Баланс: <span className="text-green-600">200 000 ₽</span>
      </div>
    </div>
  );
};

export default Header;
