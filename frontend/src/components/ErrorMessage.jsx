const ErrorMessage = ({ message }) => {
  return (
    <div className="bg-red-100 text-red-600 p-4 rounded-xl">
      {message || "Произошла ошибка"}
    </div>
  );
};

export default ErrorMessage;
