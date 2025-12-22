import Header from "./Header";
import Aside from "./Aside";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className="px-4">
      <Header />

      <div className="mt-20 flex">
        <Aside />
        
        <div className="sm:ml-20 flex gap-x-20 w-full">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
