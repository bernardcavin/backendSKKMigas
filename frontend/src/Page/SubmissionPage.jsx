// eslint-disable-next-line no-unused-vars
import React, { useState } from "react";
import { Box, Flex, Breadcrumb, BreadcrumbItem, BreadcrumbLink } from "@chakra-ui/react";
import Sidebar from "./Components/Sidebar";
import Navbar from "./Components/Navbar";
import HomePage from "./Components/HomeDash";
import PengajuanPekerjaan from "./WorkPlanning/PengajuanPekerjaan";
import OperasiPengerjaan from "./WorkPlanning/OperasiPengerjaan";
import PPP from "./WorkPlanning/PPP";
import PengajuanPekerjaanForm from "./Forms/PengajuaanPekerjaanForm";


export function Dashboard() {
    const [selectedNav, setSelectedNav] = useState('homeDash');
    const [pageDashboard, setPageDashboard] = useState(1);
    const [pageForm, setPageForm] = useState('');


    const ControllerButtonPageForm = (value) => {
        setPageForm(value)
    }

    const handleNavClick = (value) => {
        setSelectedNav(value);
        setPageForm('');


    };

    return (
        <Flex>
            <Sidebar handleMenuValue={handleNavClick} selectedNav={selectedNav} />
            {/* <SidebarResponsive selectedNav={selectedNav} /> */}
            <Box flex="1" p={4}>
                <Navbar
                // appName={selectedNav === 1 && "Homepage"}
                // {selectedNav === 2 && "Add Data"}
                />
                <Box mt={4}>
                    <Breadcrumb mb={4}>
                        <BreadcrumbItem>
                            <BreadcrumbLink href='#'>Home</BreadcrumbLink>
                        </BreadcrumbItem>

                        {selectedNav === 2 && (
                            <BreadcrumbItem>
                                <BreadcrumbLink href='#'>Add Data</BreadcrumbLink>
                            </BreadcrumbItem>
                        )}

                        {selectedNav === 1 && (
                            <BreadcrumbItem isCurrentPage>
                                <BreadcrumbLink href='#'>Homepage</BreadcrumbLink>
                            </BreadcrumbItem>
                        )}

                        {selectedNav === 2 && (
                            <BreadcrumbItem isCurrentPage>
                                <BreadcrumbLink href='#'>Form</BreadcrumbLink>
                            </BreadcrumbItem>
                        )}
                    </Breadcrumb>


                    <Box>
                        {selectedNav === 'homeDash' && <HomePage handleTambahData={setPageForm} />}
                        {selectedNav === 'submission' && <PengajuanPekerjaan handleTambahData={setPageForm} />}
                        {selectedNav === 'operations' && <OperasiPengerjaan handleTambahData={setPageForm} />}
                        {selectedNav === 'PPP' && <PPP handleTambahData={setPageForm} />}

                        {pageForm === 'addData' && <PengajuanPekerjaanForm />}
                        {/* {selectedNav === 2 && <AddData />} */}
                    </Box>
                </Box>
            </Box>
        </Flex>
    );
}

export default Dashboard;
