import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Box,
  Flex,
  Text,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Card,
  CardBody,
  CardHeader,
  SimpleGrid,
  useColorModeValue,
} from "@chakra-ui/react";
import Sidebar from "./../Components/Sidebar";
import Navbar from "./../Components/Navbar";
import { Outlet, useLocation } from "react-router-dom";
import Plot from "react-plotly.js";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const accordionButtonStyles = [
  { bg: "blue.500", color: "white" },
  { bg: "green.500", color: "white" },
  { bg: "red.500", color: "white" },
  { bg: "purple.500", color: "white" },
];

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
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="lg"
      mb={4}
      key={key}
      w={"98%"}
      maxW="400px"
    >
      <Text fontWeight="bold">{key}:</Text>
      <Text>{String(value)}</Text>
    </Box>
  );

  const renderDetails = (title, data, index) => (
    <AccordionItem mb={4}>
      <h2>
        <AccordionButton
          _expanded={{
            bg: accordionButtonStyles[index % accordionButtonStyles.length].bg,
            color:
              accordionButtonStyles[index % accordionButtonStyles.length].color,
          }}
        >
          <Box as="span" flex="1" textAlign="left">
            <Text fontSize="xl" fontWeight="bold">
              {title}
            </Text>
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel>
        {data && Object.keys(data).length > 0 ? (
          <SimpleGrid columns={4} spacing={4}>
            {Object.entries(data).map(([key, value]) =>
              renderCardItem(key, value)
            )}
          </SimpleGrid>
        ) : (
          <Text>Data tidak tersedia</Text>
        )}
      </AccordionPanel>
    </AccordionItem>
  );

  const renderPlot = (title, plotData, layout, index) => (
    <AccordionItem mb={4}>
      <h2>
        <AccordionButton
          _expanded={{
            bg: accordionButtonStyles[index % accordionButtonStyles.length].bg,
            color:
              accordionButtonStyles[index % accordionButtonStyles.length].color,
          }}
        >
          <Box as="span" flex="1" textAlign="left">
            <Text fontSize="xl" fontWeight="bold">
              {title}
            </Text>
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel w={"full"} minW={"100%"}>
        {plotData && plotData.length > 0 ? (
          <Plot
            data={plotData}
            layout={{
              ...layout,
              width: undefined,
              autosize: true,
            }}
            useResizeHandler
            style={{ width: "100%", height: "400px" }}
          />
        ) : (
          <Text>Data plot tidak tersedia</Text>
        )}
      </AccordionPanel>
    </AccordionItem>
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

  const renderAgGrid = (title, rowData, columnDefs, index) => (
    <AccordionItem mb={4}>
      <h2>
        <AccordionButton
          _expanded={{
            bg: accordionButtonStyles[index % accordionButtonStyles.length].bg,
            color:
              accordionButtonStyles[index % accordionButtonStyles.length].color,
          }}
        >
          <Box as="span" flex="1" textAlign="left">
            <Text fontSize="xl" fontWeight="bold">
              {title}
            </Text>
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel>
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
      </AccordionPanel>
    </AccordionItem>
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
            <Accordion allowToggle mt={5}>
              {/* Row 1: Operational and Technical Details */}

              {renderDetails("Operational Details", apiData.operational, 0)}
              {renderDetails("Technical Details", apiData.technical, 1)}

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
                    ),
                    2
                  )}
                  {renderPlot(
                    "Job Operation Days Plot",
                    apiData.job_operation_days.plot.data,
                    apiData.job_operation_days.plot.layout,
                    3
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
                    })),
                    4
                  )}
                  {renderPlot(
                    "Work Breakdown Structure Plot",
                    apiData.work_breakdown_structure.plot.data,
                    apiData.work_breakdown_structure.plot.layout,
                    5
                  )}
                </>
              )}

              {/* Row 4: Well Trajectory and Well Casing */}
              <Flex direction="column" wrap="wrap">
                {apiData.well_trajectory && apiData.well_trajectory.plot ? (
                  renderPlot(
                    "Well Trajectory",
                    apiData.well_trajectory.plot.data,
                    apiData.well_trajectory.plot.layout,
                    6
                  )
                ) : (
                  <Text>Data Well Trajectory tidak tersedia</Text>
                )}

                {apiData.well_casing && apiData.well_casing.path ? (
                  <AccordionItem mb={4}>
                    <h2>
                      <AccordionButton
                        _expanded={{ bg: "teal.500", color: "white" }} // Misalnya warna hijau tua saat di-expand
                      >
                        <Box as="span" flex="1" textAlign="left">
                          <Text fontSize="xl" fontWeight="bold">
                            Well Casing
                          </Text>
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel>
                      <Flex
                        direction="column"
                        align="center"
                        justify="center"
                        height="100%" // Optional: use if you need the panel to be of certain height
                      >
                        <img
                          src={wellCasingImage}
                          alt="Well Casing"
                          style={{
                            width: "40%",
                            maxWidth: "40%",
                            height: "auto",
                          }} // Adjust width and maxWidth as needed
                        />
                      </Flex>
                    </AccordionPanel>
                  </AccordionItem>
                ) : (
                  <Text>Data Well Casing tidak tersedia</Text>
                )}
              </Flex>
            </Accordion>
          )}

          <Outlet />
        </Box>
      </Box>
    </Flex>
  );
};

export default ViewPlanning;
