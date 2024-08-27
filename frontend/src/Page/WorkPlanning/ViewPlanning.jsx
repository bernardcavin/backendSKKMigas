import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Box,
  Flex,
  Text,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
} from "@chakra-ui/react";
import Sidebar from "./../Components/Sidebar";
import Navbar from "./../Components/Navbar";
import { Outlet, useLocation } from "react-router-dom";
import Plot from "react-plotly.js";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const ViewPlanning = () => {
  const { id } = useParams();
  const [selectedNav, setSelectedNav] = useState("homeDash");
  const [pageForm, setPageForm] = useState("");
  const [apiData, setApiData] = useState(null);
  const [wellCasingImage, setWellCasingImage] = useState(null);
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
    } else {
      setPageForm("");
    }

    // Fetch data dari API
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/job/planning/view/${id}/`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
              accept: "application/json",
            },
          }
        );

        const data = await response.json();
        setApiData(data);

        if (data.well_casing && data.well_casing.path) {
          const casingResponse = await fetch(
            `http://127.0.0.1:8000${data.well_casing.path}`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
                accept: "application/json",
              },
            }
          );
          const blob = await casingResponse.blob();
          const imageUrl = URL.createObjectURL(blob);
          setWellCasingImage(imageUrl);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [location.pathname, id]);

  const renderCardItem = (key, value) => (
    <Box p={4} borderWidth="1px" borderRadius="lg" mb={4} key={key} w={"98%"}>
      <Text fontWeight="bold">{key}:</Text>
      <Text>{String(value)}</Text>
    </Box>
  );

  const renderDetails = (title, data) => (
    <Card mb={4} w={"full"}>
      <CardHeader>
        <Text fontSize="xl" fontWeight="bold">
          {title}
        </Text>
      </CardHeader>
      <CardBody>
        {data && Object.keys(data).length > 0 ? (
          <SimpleGrid columns={2}>
            {Object.entries(data).map(([key, value]) =>
              renderCardItem(key, value)
            )}
          </SimpleGrid>
        ) : (
          <Text>Data tidak tersedia</Text>
        )}
      </CardBody>
    </Card>
  );

  const renderPlot = (title, plotData, layout) => (
    <Card mb={4}>
      <CardHeader>
        <Text fontSize="xl" fontWeight="bold">
          {title}
        </Text>
      </CardHeader>
      <CardBody>
        {plotData && plotData.length > 0 ? (
          <Plot
            data={plotData}
            layout={{
              ...layout,
              width: undefined,
              autosize: true,
            }}
            useResizeHandler
            style={{ width: "100%", height: "100%" }}
          />
        ) : (
          <Text>Data plot tidak tersedia</Text>
        )}
      </CardBody>
    </Card>
  );

  const transformJobOperationData = (tableData) => {
    const rowCount = Object.keys(tableData.Event).length;
    const transformedData = [];

    for (let i = 0; i < rowCount; i++) {
      transformedData.push({
        Event: tableData.Event[i],
        Days: tableData.Days[i],
        "Start Depth": tableData["Start Depth"][i],
        "End Depth": tableData["End Depth"][i],
        Cost: tableData.Cost[i],
      });
    }

    return transformedData;
  };

  const renderAgGrid = (title, rowData, columnDefs) => (
    <Card mb={4}>
      <CardHeader>
        <Text fontSize="xl" fontWeight="bold">
          {title}
        </Text>
      </CardHeader>
      <CardBody>
        {rowData && rowData.length > 0 ? (
          <div
            className="ag-theme-alpine"
            style={{ height: "400px", width: "100%" }}
          >
            <AgGridReact
              rowData={rowData}
              columnDefs={columnDefs.map((colDef) => ({ ...colDef, flex: 1 }))}
            />
          </div>
        ) : (
          <Text>Data tabel tidak tersedia</Text>
        )}
      </CardBody>
    </Card>
  );

  return (
    <Flex>
      <Sidebar handleMenuValue={handleNavClick} selectedNav={selectedNav} />
      <Box flex="1" p={4}>
        <Navbar appName="View Planning" />
        <Box mt={4}>
          <Breadcrumb mb={4}>
            <BreadcrumbItem>
              <BreadcrumbLink href="/">View Planning</BreadcrumbLink>
            </BreadcrumbItem>
            {pageForm === "submission" && (
              <BreadcrumbItem>
                <BreadcrumbLink href="/dashboard">Exploration</BreadcrumbLink>
                <BreadcrumbLink href="#" fontWeight={"bold"}>
                  Submission
                </BreadcrumbLink>
              </BreadcrumbItem>
            )}
          </Breadcrumb>

          <Text mt={4}>ID: {id}</Text>

          {apiData && (
            <>
              {/* Row 1: Operational and Technical Cards */}
              <Flex mb={4} justifyContent={"space-between"} gap={8}>
                {renderDetails("Operational Details", apiData.operational)}
                {renderDetails("Technical Details", apiData.technical)}
              </Flex>

              {/* Row 2: Job Operation Days Table and Plot */}
              {apiData.job_operation_days && (
                <>
                  {renderAgGrid(
                    "Job Operation Days Table",
                    transformJobOperationData(apiData.job_operation_days.table),
                    Object.keys(apiData.job_operation_days.table).map(
                      (key) => ({
                        headerName: key,
                        field: key,
                      })
                    )
                  )}
                  {renderPlot(
                    "Job Operation Days Plot",
                    apiData.job_operation_days.plot.data,
                    apiData.job_operation_days.plot.layout
                  )}
                </>
              )}

              {/* Row 3: Work Breakdown Structure Table and Plot */}
              {apiData.work_breakdown_structure && (
                <>
                  {renderAgGrid(
                    "Work Breakdown Structure Table",
                    apiData.work_breakdown_structure.table,
                    Object.keys(
                      apiData.work_breakdown_structure.table[0] || {}
                    ).map((key) => ({
                      headerName: key,
                      field: key,
                    }))
                  )}
                  {renderPlot(
                    "Work Breakdown Structure Plot",
                    apiData.work_breakdown_structure.plot.data,
                    apiData.work_breakdown_structure.plot.layout,
                    true
                  )}
                </>
              )}

              {/* Row 4: Well Trajectory and Well Casing */}
              <Flex mb={8}>
                <Box flex="1" mr={4} minW="40%">
                  {apiData.well_trajectory && apiData.well_trajectory.plot ? (
                    renderPlot(
                      "Well Trajectory",
                      apiData.well_trajectory.plot.data,
                      apiData.well_trajectory.plot.layout
                    )
                  ) : (
                    <Text>Data Well Trajectory tidak tersedia</Text>
                  )}
                </Box>

                <Box flex="1" minW="40%" justifyContent={"space-between"} gap={8}>
                  {apiData.well_casing && apiData.well_casing.path ? (
                    <Card>
                      <CardHeader>
                        <Text fontSize="xl" fontWeight="bold" mb={4}>
                          Well Casing
                        </Text>
                      </CardHeader>
                      <CardBody>
                        <img
                          src={wellCasingImage}
                          alt="Well Casing"
                          style={{ width: "100%" }}
                        />
                      </CardBody>
                    </Card>
                  ) : (
                    <Text>Data Well Casing tidak tersedia</Text>
                  )}
                </Box>
              </Flex>
            </>
          )}

          <Outlet />
        </Box>
      </Box>
    </Flex>
  );
};

export default ViewPlanning;
