import { useEffect, useState } from "react";

const Goals = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    setTimeout(() => {

      setGoals([
        { title: "Путешествие", percent: 45, color: "bg-blue-600" },
        { title: "Xbox", percent: 65, color: "bg-green-600" },
        { title: "Кисти", percent: 15, color: "bg-orange-600" },
      ]);

      setLoading(false);
    }, 800);
  }, []);

  if (loading)
    return (
      <div className="p-4 bg-white rounded-lg shadow text-center">
        <p className="animate-pulse text-gray-500">Загрузка целей…</p>
      </div>
    );

  if (error)
    return (
      <div className="p-4 bg-red-100 text-red-600 rounded-lg font-medium">
        Ошибка загрузки целей
      </div>
    );

  if (goals.length === 0)
    return (
      <div className="p-4 text-gray-500 bg-white rounded-lg">
        Целей пока нет
      </div>
    );

  return (
    <div className="flex flex-col gap-y-5">
      <h2 className="font-montserrat font-semibold text-2xl">Цели</h2>

      <div className="flex flex-col gap-y-7">
        {goals.map((goal, i) => (
          <div key={i}>
            <div className="flex justify-between mb-1">
              <span className="font-montserrat font-medium">{goal.title}</span>
              <span className="font-montserrat font-medium">
                {goal.percent}%
              </span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`${goal.color} h-3 rounded-full`}
                style={{ width: `${goal.percent}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Goals;
