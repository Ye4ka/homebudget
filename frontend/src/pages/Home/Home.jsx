import Balance from "../../components/Balance";
import FastAction from "../../components/FastAction";
import Transaction from "../../components/Transaction";
import Goals from "../../components/Goals";

const Home = () => {
  return (
    <>
      <div className="flex gap-10 flex-wrap">
        <div className="flex flex-col gap-10">
          <Balance />
          <Transaction />
        </div>

        <div className="flex flex-col gap-10 mb-10">
          <FastAction />
          <div className="mt-7">
            <Goals />
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
