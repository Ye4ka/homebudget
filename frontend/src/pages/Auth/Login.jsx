import { useForm } from "react-hook-form";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

function Login() {
  const [apiError, setApiError] = useState(null); 
  const navigate = useNavigate();
  const { login, authLoading } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm();

  const onSubmit = async (data) => {
    setApiError(null);

    try {
      const result = await login({
        email: data.email,
        password: data.password
      });
      if (result.success) {
        navigate("/dashboard");
      } else {
        setApiError(
          result.error?.detail || 
          result.error?.message || 
          "Неверный email или пароль"
        );
      }
    } catch (err) {
    setApiError("Ошибка подключения к серверу");
  }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md space-y-5 m-6"
      >
        <h2 className="text-2xl font-bold text-center">Вход</h2>
        {apiError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
            {apiError}
          </div>
        )}

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

        {/* Submit */}
        <button
          type="submit"
          disabled={authLoading}
          className="w-full py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition disabled:bg-blue-300"
        >
          {authLoading ? "Загрузка..." : "Войти"}
        </button>
        <p className="text-center text-gray-600">
          Нет аккаунта?{" "}
          <button
            type="button"
            onClick={() => navigate("/register")}
            className="text-blue-600 hover:underline"
          >
            Зарегистрироваться
          </button>
        </p>
      </form>
    </div>
  );
}
export default Login;