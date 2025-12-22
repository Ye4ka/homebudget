export function Button({ children, onClick, variant = "primary", className = "", ...props }) {
    const base = "px-5 py-3 rounded-xl font-medium transition-all w-74";
    const variants = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white",
    success: "bg-green-500 hover:bg-green-600 text-white",
    danger: "bg-red-500 hover:bg-red-600 text-white",
    yellow: "bg-yellow-400 hover:bg-yellow-500 text-black",
};
    return (
        <button
        onClick={onClick}
        className={`${base} ${variants[variant]} ${className}`}
        {...props}
        >
        {children}
        </button>
    );
}