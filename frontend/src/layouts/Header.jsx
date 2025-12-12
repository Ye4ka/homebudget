import Logo from "../assets/images/Logo.png";

const Header = () => {
  return (
    <div className="flex justify-between items-center">
      <img src={Logo} className="w-44" />

      <div className="text-xl font-semibold">
        Баланс: <span className="text-green-600">200 000 ₽</span>
      </div>
    </div>
  );
};

export default Header;
