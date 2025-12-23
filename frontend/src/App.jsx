import AppRoutes from "./routes/AppRoutes";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { useContext } from "react";
import Spinner from "./components/Spinner";

function AppContent() {
  const { appLoading } = useContext(AuthContext);

  if (appLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner/>
      </div>
    );
  }

  return <AppRoutes />;
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
