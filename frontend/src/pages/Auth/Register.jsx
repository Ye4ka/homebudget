import { useForm } from "react-hook-form";
import { useState } from "react";

function Register() {
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      console.log("Register data:", data);
      await new Promise((res) => setTimeout(res, 1000));
    } finally {
      setLoading(false);
    }
  };

  const passwordValue = watch("password");

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md space-y-5 m-6"
      >
        <h2 className="text-2xl font-bold text-center">Register</h2>

        {/* First Name */}
        <div>
          <input
            type="text"
            placeholder="Имя"
            className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500"
            {...register("first_name", {
              required: "Имя обязательно"
            })}
          />
          {errors.first_name && (
            <p className="text-red-500 text-sm mt-1">
              {errors.first_name.message}
            </p>
          )}
        </div>

        {/* Last Name */}
        <div>
          <input
            type="text"
            placeholder="Фамилия"
            className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500"
            {...register("last_name", {
              required: "Фамилия обязательна"
            })}
          />
          {errors.last_name && (
            <p className="text-red-500 text-sm mt-1">
              {errors.last_name.message}
            </p>
          )}
        </div>

        {/* Email */}
        <div>
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500"
            {...register("email", {
              required: "Email обязателен",
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: "Некорректный email"
              }
            })}
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
          )}
        </div>

        {/* Password */}
        <div>
          <input
            type="password"
            placeholder="Пароль"
            className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500"
            {...register("password", {
              required: "Пароль обязателен",
              minLength: {
                value: 8,
                message: "Минимум 8 символов"
              }
            })}
          />
          {errors.password && (
            <p className="text-red-500 text-sm mt-1">
              {errors.password.message}
            </p>
          )}
        </div>

        {/* Confirm Password */}
        <div>
          <input
            type="password"
            placeholder="Повторите пароль"
            className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500"
            {...register("confirmPassword", {
              required: "Подтвердите пароль",
              validate: (value) =>
                value === passwordValue || "Пароли не совпадают"
            })}
          />
          {errors.confirmPassword && (
            <p className="text-red-500 text-sm mt-1">
              {errors.confirmPassword.message}
            </p>
          )}
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition disabled:bg-green-300"
        >
          {loading ? "Загрузка..." : "Зарегистрироваться"}
        </button>
      </form>
    </div>
  );
}
export default Register;