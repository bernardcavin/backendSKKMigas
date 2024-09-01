import React, { useState, useEffect } from "react";
import {
  Box,
  Flex,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
} from "@chakra-ui/react";
import Sidebar from "./Components/Sidebar";
import Navbar from "./Components/Navbar";
import HomePage from "./Components/HomeDash";
import { Outlet, useLocation } from "react-router-dom";

export function Dashboard() {
  const [selectedNav, setSelectedNav] = useState("homeDash");
  const [pageForm, setPageForm] = useState("");
  const location = useLocation();

  const handleNavClick = (value) => {
    setSelectedNav(value);
    setPageForm("");
  };

  useEffect(() => {
    const path = location.pathname;
    if (path.includes("/dashboard/submission")) {
      setPageForm("submission");
      setSelectedNav("submission");
    } else if (path.includes("/dashboard/operasi")) {
      setPageForm("operations");
      setSelectedNav("operations");
    } else if (path.includes("/dashboard/ppp")) {
      setPageForm("PPP");
      setSelectedNav("PPP");
    } else if (path.includes("/dashboard")) {
      setPageForm("homeDash");
      setSelectedNav("homeDash");
    } else if (path.includes("/development")) {
      setPageForm("development");
      setSelectedNav("development");
    } else if (path.includes("/development/perencanaan")) {
      setPageForm("perencanaan");
      setSelectedNav("perencanaan");
    } else {
      setPageForm(""); // Default or reset state
    }
  }, [location.pathname]);
  const path = location.pathname;
  return (
    <Flex>
      <Sidebar handleMenuValue={handleNavClick} selectedNav={selectedNav} />
      <Box flex="1" p={4}>
        <Navbar />
        <Box mt={4}>
          {/* <Breadcrumb mb={4}>
            <BreadcrumbItem>
              <BreadcrumbLink href="/">Home</BreadcrumbLink>
            </BreadcrumbItem>
            {pageForm === 'submission' && (
              <>
                <Breadcrumb>
                  <BreadcrumbItem>
                    <BreadcrumbLink href='/dashboard'>Exploration</BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbItem >
                    <BreadcrumbLink href='#' fontWeight={'bold'}>Submission</BreadcrumbLink>
                  </BreadcrumbItem>
                </Breadcrumb>
              </>
            )}
            {pageForm === 'operations' && (
              <>
                <Breadcrumb>
                  <BreadcrumbItem>
                    <BreadcrumbLink href='/dashboard'>Exploration</BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbItem >
                    <BreadcrumbLink href='#' fontWeight={'bold'}>Operation</BreadcrumbLink>
                  </BreadcrumbItem>
                </Breadcrumb>
              </>
            )}
            {pageForm === 'PPP' && (
              <>
                <Breadcrumb>
                  <BreadcrumbItem>
                    <BreadcrumbLink href='/dashboard'>Exploration</BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbItem >
                    <BreadcrumbLink href='#' fontWeight={'bold'}>P3</BreadcrumbLink>
                  </BreadcrumbItem>
                </Breadcrumb>
              </>
            )}
            {path.includes("/development") && (
              <BreadcrumbItem>
                <BreadcrumbLink fontWeight={path.includes("/development")  &&  !path.includes("/development/perencanaan") && "bold"} href="/dashboard">
                  Development
                </BreadcrumbLink>
              </BreadcrumbItem>
            )}
            {path.includes("/development/perencanaan") && (
              <BreadcrumbItem>
                <BreadcrumbLink fontWeight={"bold"} href="/dashboard">
                  Submission
                </BreadcrumbLink>
              </BreadcrumbItem>
          )}
          </Breadcrumb> */}

          <Box>
            {/* {selectedNav === "homeDash" && (
              <HomePage handleTambahData={setPageForm} />
            )} */}
            <Outlet />
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}

export default Dashboard;
