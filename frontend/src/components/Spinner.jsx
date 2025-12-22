function Spinner({ size = 32 }) {
    return (
        <div
            className="animate-spin border-4 border-gray-300 border-t-blue-600 rounded-full"
            style={{ width: size, height: size }}
        >
        </div>
    );
}

export default Spinner;