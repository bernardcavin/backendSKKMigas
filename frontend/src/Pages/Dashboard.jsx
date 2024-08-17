import React, { useState, } from "react";
import { useNavigate } from "react-router-dom";
import {
    Navbar,
    Collapse,
    Typography,
    Button,
    Drawer,
    Card,
    List,
    ListItem,
    ListItemPrefix,
    ListItemSuffix,
    Chip,
    IconButton,
    Input,
} from "@material-tailwind/react";
import { Bars3Icon, XMarkIcon, PowerIcon, PlusIcon, InboxIcon, Cog6ToothIcon } from "@heroicons/react/24/outline";
import FormInput from "./Components/FormInput";
import { useAuth } from "../AuthContext";

const Homepage = () => {
    return (
        <div>
            <h1>Homepage</h1>
        </div>
    );
}


const NavList = () => {
    return (
        <h1>Hello</h1>
    );
}

export function Dashboard() {
    const [open, setOpen] = React.useState(false);
    
    const { logout } = useAuth();
    const navigate = useNavigate();
  
    const handleLogout = async () => {
      try {
        await logout();
        navigate('/login');  // Redirect to login page after successful logout
      } catch (error) {
        console.error('Logout failed:', error);
        // You might want to show an error message to the user here
      }
    };

    const [handleOpen, setHandleOpen] = useState(1);
    
    const click = (value) => {
        setHandleOpen(value);
        closeDrawer();
    }

    const [isDrawerOpen, setIsDrawerOpen] = React.useState(false);
    const openDrawer = () => setIsDrawerOpen(true);
    const closeDrawer = () => setIsDrawerOpen(false);
    const SideBar = () => {
        return (
            <>
                <Drawer open={isDrawerOpen} onClose={closeDrawer}>
                    <Card
                        color="white"
                        shadow={false}
                        className="h-[calc(100vh-2rem)] w-full p-4"
                    >
                        <div className="mb-2 flex items-center gap-4 p-4">

                            <Typography variant="h5" color="blue-gray">
                                SKK Migas
                            </Typography>
                        </div>

                        <List>
                            <ListItem onClick={() => click(1) }>
                                <ListItemPrefix>
                                    <PlusIcon className="h-5 w-5" />
                                </ListItemPrefix>
                                Dashboard


                            </ListItem>
                            <ListItem onClick={() => click(2) }>
                                <ListItemPrefix>
                                    <PlusIcon className="h-5 w-5" />
                                </ListItemPrefix>
                                Add Data
                                <ListItemSuffix>
                                    <Chip
                                        value="14"
                                        size="sm"
                                        variant="ghost"
                                        color="blue-gray"
                                        className="rounded-full"
                                    />
                                </ListItemSuffix>
                            </ListItem>
                            <ListItem>
                                <ListItemPrefix>
                                    <Cog6ToothIcon className="h-5 w-5" />
                                </ListItemPrefix>
                                About Us
                            </ListItem>
                            <ListItem onClick={handleLogout}>
                                <ListItemPrefix>
                                    <PowerIcon className="h-5 w-5" />
                                </ListItemPrefix>
                                Log Out
                            </ListItem>
                        </List>

                    </Card>
                </Drawer>
            </>
        );
    }

    const [openNav, setOpenNav] = React.useState(false);

    const handleWindowResize = () =>
        window.innerWidth >= 960 && setOpenNav(false);

    React.useEffect(() => {
        window.addEventListener("resize", handleWindowResize);

        return () => {
            window.removeEventListener("resize", handleWindowResize);
        };
    }, []);

    return (
        <>
            <SideBar />
            <Navbar className="mx-auto max-w-full px-6 py-3">


                <div className="flex items-center justify-between text-blue-gray-900">
                    <div className="flex">
                        <IconButton
                            variant="text"
                            className="ml-auto h-6 w-6 text-inherit hover:bg-transparent focus:bg-transparent active:bg-transparent "
                            ripple={false}
                            onClick={openDrawer}>
                            {open ? (
                                <XMarkIcon className="h-6 w-6" strokeWidth={2} />
                            ) : (
                                <Bars3Icon className="h-6 w-6" strokeWidth={2} />
                            )}
                        </IconButton>

                    </div>


                </div>
                <Collapse open={openNav}>
                    <NavList />
                </Collapse>


            </Navbar>
            <div className="flex flex-col mt-12 ">
                {handleOpen === 1 && <Homepage />}
                {handleOpen === 2 && <FormInput />}

            </div>


        </>

    );
}

export default Dashboard
