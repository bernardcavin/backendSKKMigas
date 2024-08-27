import "./App.css";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";
import Dashboard from "./Page/Dashboard";
import { useAuth } from "./Auth/AuthContext";
import Login from "./Auth/Login";
import Register from "./Auth/Register";
import PengajuanPekerjaan from "./Page/WorkPlanning/PengajuanPekerjaan";
import OperasiPengerjaan from "./Page/WorkPlanning/OperasiPengerjaan";
import PPP from "./Page/WorkPlanning/PPP";
import PengajuanPekerjaanForm from "./Page/Forms/PengajuaanPekerjaanForm";
import PengajuanOperasiForm from "./Page/Forms/OperasiPengajuaanForm";
import PlanningWows from "./Page/Forms/PlanningWows";
import WowsForm from "./Page/Forms/OperasiPengajuaanForm";
import OperasiPengajuaanForm from "./Page/Forms/OperasiPengajuaanForm";
import ProtectedRoute from "./Auth/ProtectedUser";
import DashboardSKK from "./Page/PageKKKS/DashboardKKS";
import HomeDashKKKS from "./Page/PageKKKS/Components/HomeDashKKS";
import ViewPlanning from "./Page/WorkPlanning/ViewPlanning";

function App() {
  const { isAuthenticated } = useAuth();

  const router = createBrowserRouter([
    {
      path: "/",
      element: isAuthenticated ? <Dashboard /> : <Login />,
    },
    {
      path: "/register",
      element: <Register />,
    },
    {
      path: "/dashboard",
      element: (
        <ProtectedRoute element={<Dashboard />} allowedRoles={["Admin"]} />
      ),

      children: [
        {
          path: "submission",
          element: (
            <ProtectedRoute
              element={<PengajuanPekerjaan />}
              allowedRoles={["Admin"]}
            />
          ),
          children: [
            {
              path: "pengajuanform",
              element: <PengajuanPekerjaanForm />,
            },
          ],
        },
        {
          path: "operasi",
          element: <OperasiPengerjaan />,
          children: [
            {
              path: "operasiform",
              element: <OperasiPengajuaanForm />,
            },
          ],
        },
        {
          path: "ppp",
          element: <PPP />,
          children: [
            {
              path: "pppform",
              element: <PengajuanPekerjaanForm />,
            },
          ],
        },
        
      ],
    },

    {
      path: "development",
      element: <Dashboard />,
      
    },
    {
      path: "/skk",
      element: <DashboardSKK />,
      children: [
        {
          path: "dashboard",
          element: <HomeDashKKKS />,
        },
      ],
    },
    {
      path: "/pengajuanpekerjaan",
      element: <PengajuanPekerjaan />,
    },
    {
      path: "/operasipekerjaan",
      element: <OperasiPengerjaan />,
    },
    {
      path: "/ppp",
      element: <PPP />,
    },
    {
      path: "/pengajuanpekerjaanform",
      element: <PengajuanPekerjaanForm />,
    },
    {
      path: "/pengajuanoperasiform",
      element: <PengajuanOperasiForm />,
    },
    {
      path: "/pengajuanwowsform",
      element: <PlanningWows />,
    },
    {
      path: "viewplanning/:id",
      element: <ViewPlanning />,
    },
  ]);

  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
