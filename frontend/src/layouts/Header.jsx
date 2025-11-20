import Logo from "../assets/images/Logo.png";
import Noth from "../assets/images/noth.png";
import Lk from "../assets/images/lk.png";

const Header = () => {
  return (
    <div className="flex justify-between items-center">
        <img src={Logo} alt="" className="w-44 h-8" />
        <div className="flex gap-x-5">
            <img src={Noth} alt="" className="w-21 h-21" />
            <img src={Lk} alt="" className="w-21 h-21" />
        </div>
    </div>
  );
};

export default Header;