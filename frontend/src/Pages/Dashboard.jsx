import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Navbar } from "@material-tailwind/react";
import FormInput from "./Components/FormInput";
import { useAuth } from "../AuthContext";
import { SidebarWithLogo } from "./Components/Sidebar";

const Homepage = () => {
  return (
    <div>
      <h1>Homepage</h1>
    </div>
  );
};

export function Dashboard() {
  const [selectedNav, setSelectedNav] = useState(1);
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleNavClick = (value) => {
    if (value === 4) {
      handleLogout();
    } else {
      setSelectedNav(value);
    }
  };

  return (
    <div className="flex">
      <SidebarWithLogo onClickNavItem={handleNavClick} selectedNav={selectedNav} />
      <div className="flex-1 p-4">
        <Navbar className="max-w-4/5 px-6 py-3 ml-[20rem]">
          <div className="flex items-center justify-between text-blue-gray-900 w-5/6 ">
            <div className="flex">
                <h1 className="text-lg font-bold">{selectedNav === 1 && 'Homepage'}{ selectedNav === 2 && 'Add Data'}</h1>
            </div>
          </div>
        </Navbar>
        <div className="flex ml-[20rem] flex-col w-4/5 mt-4">
          {selectedNav === 1 && <Homepage />}
          {selectedNav === 2 && <FormInput />}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
