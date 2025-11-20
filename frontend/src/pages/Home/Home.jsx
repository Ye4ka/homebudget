import Header from "../../layouts/Header";
import Aside from "../../layouts/Aside";
import Balance from "../../components/Balance";
import FastAction from "../../components/FastAction";
import Transaction from "../../components/Transaction";
import Goals from "../../components/Goals";

const Home = () => {
  return (
    <div className="px-4">
        <div>
            <Header />
            <div className="mt-20 flex">
                <Aside />
                <div className="ml-20 flex gap-x-20">
                    <div className="flex flex-col gap-10 mb-20">
                        <Balance />
                        <Transaction />
                    </div>
                    <div className="flex flex-col gap-10 mb-20 w-128">
                        <FastAction />
                        <div className="mt-13">
                            <Goals />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
};

export default Home;