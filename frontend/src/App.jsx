import React, { useState, useEffect } from "react";
import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
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
import OperasiPengajuaanForm from "./Page/Forms/OperasiPengajuaanForm";
import ProtectedRoute from "./Auth/ProtectedUser";
import DashboardSKK from "./Page/PageSKK/DashboardKKS";
import HomeDashKKKS from "./Page/PageSKK/Components/HomeDashSKK";
import ViewPlanning from "./Page/WorkPlanning/ViewPlanning";
import HomeExploitation from "./Page/Components/PageExploitasi/HomeDashExplo";
import SplashScreen from "./Page/Components/SplashScreen"; // Import SplashScreen
import RoleRedirect from "./Auth/RoleRedirect";
import GraphTable from "./Page/Components/PageExploitasi/GraphTable";
import Exploration from "./Page/PageSKK/Exploration";
import DevelopmentSKK from "./Page/PageSKK/DevelopmentSKK";
import WellServiceSKK from "./Page/PageSKK/WellServiceSKK";
import WorkOverSKK from "./Page/PageSKK/WorkOverSKK";
import PlanningExp from "./Page/PageSKK/ChildExploration/PlanningExp";
import PlanningDevelopment from "./Page/PageSKK/ChildDevelopment/PlanningDev";
import PlanningWellService from "./Page/PageSKK/ChildWellService/PlanningWS";
import PlanningWorkOver from "./Page/PageSKK/ChildWorkOver/PlanningWO";
import PengajuanDrillingForm from "./Page/Forms/PengajuanDrillingForm";

function App() {
  const { isAuthenticated } = useAuth();
  const [showSplashScreen, setShowSplashScreen] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      const splashScreenShown = localStorage.getItem("splashScreenShown");

      if (!splashScreenShown) {
        setShowSplashScreen(true);
        localStorage.setItem("splashScreenShown", "true");

        const timer = setTimeout(() => {
          setShowSplashScreen(false);
        }, 3000); // Tampilkan splash screen selama 3 detik

        return () => clearTimeout(timer);
      }
    }
  }, [isAuthenticated]);

  const router = createBrowserRouter([
    {
      path: "/login",
      element: <Login />,
    },
    {
      path: "/",
      element: <RoleRedirect />,
    },
    {
      path: "/register",
      element: <Register />,
    },
    {
      path: "/dashboard",
      element: showSplashScreen ? (
        <SplashScreen />
      ) : (
        <ProtectedRoute element={<Dashboard />} allowedRoles={["KKKS"]} />
      ),
      children: [
        {
          path: "planning",
          element: (<ProtectedRoute element={<PengajuanPekerjaan />} allowedRoles={["KKKS"]}/> ),
        },
        {
          path: "planning/planningform",
          element: (<ProtectedRoute element={<PengajuanDrillingForm />} allowedRoles={["KKKS"]}/> ),
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
      children: [
        {
          path: "grafikexploitasi",
          element: <GraphTable />,
        },
        {
          path: "perencanaan",
          element: <HomeExploitation />,
        },
      ],
    },
    {
      path: "/skk",
      element: (
        <ProtectedRoute element={<DashboardSKK />} allowedRoles={["Admin"]} />
      ),
      children: [
        {
          path: "dashboard",
          element: (
            <ProtectedRoute
              element={<HomeDashKKKS />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "exploration",
          element: (
            <ProtectedRoute
              element={<Exploration />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "exploration/planningexploration",
          element: (
            <ProtectedRoute
              element={<PlanningExp />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "development",
          element: (
            <ProtectedRoute
              element={<DevelopmentSKK />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "development/planningdevelopment",
          element: (
            <ProtectedRoute
              element={<PlanningDevelopment />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "wellservice",
          element: (
            <ProtectedRoute
              element={<WellServiceSKK />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "wellservice/planningwellservice",
          element: (
            <ProtectedRoute
              element={<PlanningWellService />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "workover",
          element: (
            <ProtectedRoute
              element={<WorkOverSKK />}
              allowedRoles={["Admin"]}
            />
          ),
        },
        {
          path: "workover/planningworkover",
          element: (
            <ProtectedRoute
              element={<PlanningWorkOver />}
              allowedRoles={["Admin"]}
            />
          ),
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
