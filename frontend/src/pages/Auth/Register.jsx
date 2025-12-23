import { useForm } from "react-hook-form";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

function Register() {
  const [apiError, setApiError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const navigate = useNavigate();
  const { register: registerUser, authLoading } = useAuth();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm();

  const onSubmit = async (data) => {
    setApiError(null);
    setSuccessMessage(null);
    try {
      const result = await registerUser({
        email: data.email,
        password: data.password,
        password2: data.confirmPassword,
        first_name: data.first_name,
        last_name: data.last_name
      });
      if (result.success) {
        setSuccessMessage(result.message);
        
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        const errorMessages = [];
        
        if (typeof result.error === 'object') {
          Object.entries(result.error).forEach(([field, messages]) => {
            if (Array.isArray(messages)) {
              errorMessages.push(...messages);
            } else {
              errorMessages.push(messages);
            }
          });
        } else {
          errorMessages.push(result.error);
        }

        setApiError(errorMessages.join('. '));
      }
    } catch (err) {
      setApiError("Ошибка подключения к серверу");
    } 
  };

  const passwordValue = watch("password");

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md space-y-5 m-6"
      >
        <h2 className="text-2xl font-bold text-center">Регистрация</h2>
        {successMessage && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-xl">
            {successMessage}
          </div>
        )}
        {apiError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
            {apiError}
          </div>
        )}             

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
          disabled={authLoading}
          className="w-full py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition disabled:bg-green-300"
        >
          {authLoading ? "Загрузка..." : "Зарегистрироваться"}
        </button>
        <p className="text-center text-gray-600">
          Уже есть аккаунт?{" "}
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="text-blue-600 hover:underline"
          >
            Войти
          </button>
        </p>
      </form>
    </div>
  );
}
export default Register;