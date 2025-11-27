export function Input({ placeholder, className = "", ...props }) {
    return (
        <input
            placeholder={placeholder}
            className={`border border-black/20 p-2 rounded w-74 focus:ring-2 focus:ring-blue-400 ${className}`}
            {...props}
        />
    );
}