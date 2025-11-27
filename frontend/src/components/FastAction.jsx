import { Button } from "./Button.jsx";
import { Input } from "./Input.jsx";

const FastAction = () => {
  return (
    <div className="flex flex-col gap-y-5">
        <h2 className="font-montserrat font-semibold text-2xl">Быстрые действия</h2>
        <Input placeholder={"Введите сумму..."}></Input>
        <Button variant="success" className=" w-74">Добавить доход</Button>
        <Button variant="danger" className=" w-74">Добавить расход</Button>
    </div>
  );
};

export default FastAction;