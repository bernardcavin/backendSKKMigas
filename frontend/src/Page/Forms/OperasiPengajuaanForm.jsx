import React, { useState, useEffect } from "react";
import {
  Box,
  Grid,
  VStack,
  HStack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  FormControl,
  FormLabel,
  Input,
  Select,
  Button,
  Text,
  List,
  ListItem,
  ListIcon,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
} from "@chakra-ui/react";
import { ChevronRightIcon, CheckIcon } from "@chakra-ui/icons";

// NavigationMenu Component
const NavigationMenu = ({ completedSections, activeTab }) => (
  <VStack align="stretch" spacing={2} position="sticky" top="20px">
    <Text fontWeight="bold" fontSize="xl" mb={2}>
      Navigasi
    </Text>
    <List spacing={2}>
      {Object.entries(completedSections[activeTab]).map(
        ([section, isCompleted]) => (
          <ListItem key={section} display="flex" alignItems="center">
            <ListIcon
              as={isCompleted ? CheckIcon : ChevronRightIcon}
              color={isCompleted ? "green.500" : "blue.500"}
            />
            {section}
          </ListItem>
        )
      )}
    </List>
  </VStack>
);

// Main WellForm Component
const OperasiPengajuaanForm = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [completedSections, setCompletedSections] = useState({
    teknis: {
      Well: false,
      Koordinat: false,
      Seismic: false,
      Keydates: false,
      Elevasi: false,
      "Well Summary": false,
      "Well Test": false,
      "Well Trajectory": false,
      "Pore Pressure Fracture Gradient": false,
    },
    operasional: {
      "Proposed Job": false,
      "Work breakdown structure": false,
      "Job document": false,
      "Job Operation Days": false,
      "Job Hazard": false,
    },
  });

  // Teknis Tab States
  const [wellData, setWellData] = useState({
    uwi: "",
    namaSumur: "",
    namaLengkapSumur: "",
    typeWell: "",
    wellStatus: "",
    wellProfileType: "",
    hydrocarbonTarget: "",
    environmentType: "",
  });

  const [koordinatData, setKoordinatData] = useState({
    surfaceLongitude: "",
    surfaceLatitude: "",
    bottomHoleLongitude: "",
    bottomHoleLatitude: "",
    maximumInclination: "",
    azimuth: "",
  });

  const [seismicData, setSeismicData] = useState({
    lineName: "",
  });

  const [keydatesData, setKeydatesData] = useState({
    spudDate: "",
    finalDrillDate: "",
    completionDate: "",
  });

  const [elevasiData, setElevasiData] = useState({
    unit: "",
    rotaryTableElev: "",
    kbElev: "",
    derrickFloorElev: "",
    groundElev: "",
    meanSeaLevel: "",
    depthDatum: "",
    kickOffPoint: "",
    maximumTvd: "",
    finalMd: "",
    remark: "",
  });

  const [wellSummary, setWellSummary] = useState([]);
  const [wellSummaryForm, setWellSummaryForm] = useState({
    depthDatum: "",
    unit: "",
    depth: "",
    holeDiameter: "",
    bit: "",
    casingDiameter: "",
    casingGrade: "",
    casingWeight: "",
    logging: "",
    mudProgram: "",
    cementingProgram: "",
    bottomHoleTemperature: "",
    rateOfPenetration: "",
    remarks: "",
  });

  const [wellTest, setWellTest] = useState([]);
  const [wellTestForm, setWellTestForm] = useState({
    depthDatum: "",
    unit: "",
    zoneName: "",
    zoneTopDepth: "",
    zoneBottomDepth: "",
  });

  const [wellDocumentData, setWellDocumentData] = useState({
    title: "",
    mediaType: "",
    documentType: "",
    remark: "",
  });

  const [porePressureFile, setPorePressureFile] = useState(null);

  const [wellTrajectoryFile, setWellTrajectoryFile] = useState(null);
  const [wellLogsFile, setWellLogsFile] = useState(null);
  const [wellDrillingParameterFile, setWellDrillingParameterFile] = useState(null);

  // Operasional Tab States
  const [proposedJob, setProposedJob] = useState({
    areaId: "",
    fieldId: "",
    afeNumber: "",
    totalBudget: "",
    wpbYear: "",
    startDate: "",
    endDate: "",
    rigName: "",
    rigType: "",
    rigHorsePower: "",
  });

  const [workBreakdown, setWorkBreakdown] = useState([]);
  const [workBreakdownForm, setWorkBreakdownForm] = useState({
    event: "",
    startDate: "",
    endDate: "",
    remark: "",
  });

  const [jobDocument, setJobDocument] = useState([]);
  const [jobDocumentForm, setJobDocumentForm] = useState({
    title: "",
    creatorName: "",
    createDate: "",
    documentType: "",
    itemCategory: "",
    itemSubCategory: "",
    digitalFormat: "",
    originalFileName: "",
    digitalSize: "",
    remark: "",
  });

  const [jobOperationDays, setJobOperationDays] = useState([]);
  const [jobOperationDaysForm, setJobOperationDaysForm] = useState({
    phase: "",
    depthDatum: "",
    unit: "",
    depthIn: "",
    depthOut: "",
    operationDays: "",
  });

  const [jobHazard, setJobHazard] = useState([]);
  const [jobHazardForm, setJobHazardForm] = useState({
    hazardType: "",
    hazardDescription: "",
    severity: "",
    mitigation: "",
    remark: "",
  });

  // Handle Input Change
  const handleInputChange = (tab, section, field, value) => {
    if (tab === "teknis") {
      switch (section) {
        case "Well":
          setWellData((prev) => ({ ...prev, [field]: value }));
          break;
        case "Koordinat":
          setKoordinatData((prev) => ({ ...prev, [field]: value }));
          break;
        case "Seismic":
          setSeismicData((prev) => ({ ...prev, [field]: value }));
          break;
        case "Keydates":
          setKeydatesData((prev) => ({ ...prev, [field]: value }));
          break;
        case "Elevasi":
          setElevasiData((prev) => ({ ...prev, [field]: value }));
          break;
        case "Well Summary":
          setWellSummaryForm((prev) => ({ ...prev, [field]: value }));
          break;
        case "Well Test":
          setWellTestForm((prev) => ({ ...prev, [field]: value }));
          break;
        case "Pore Pressure Fracture Gradient":
          setPorePressure((prev) => ({ ...prev, [field]: value }));
          break;
        default:
          break;
      }
    } else if (tab === "operasional") {
      switch (section) {
        case "Proposed Job":
          setProposedJob((prev) => ({ ...prev, [field]: value }));
          break;
        case "Work breakdown structure":
          setWorkBreakdownForm((prev) => ({ ...prev, [field]: value }));
          break;
        case "Job document":
          setJobDocumentForm((prev) => ({ ...prev, [field]: value }));
          break;
        case "Job Operation Days":
          setJobOperationDaysForm((prev) => ({ ...prev, [field]: value }));
          break;
        case "Job Hazard":
          setJobHazardForm((prev) => ({ ...prev, [field]: value }));
          break;
        default:
          break;
      }
    }
    updateSectionCompletion(tab, section);
  };

  // Handle Add Batch
  const handleAddBatch = (tab, section) => {
    if (tab === "teknis") {
      switch (section) {
        case "Well Summary":
          setWellSummary((prev) => [...prev, wellSummaryForm]);
          setWellSummaryForm({
            depthDatum: "",
            unit: "",
            depth: "",
            holeDiameter: "",
            bit: "",
            casingDiameter: "",
            casingGrade: "",
            casingWeight: "",
            logging: "",
            mudProgram: "",
            cementingProgram: "",
            bottomHoleTemperature: "",
            rateOfPenetration: "",
            remarks: "",
          });
          break;
        case "Well Test":
          setWellTest((prev) => [...prev, wellTestForm]);
          setWellTestForm({
            depthDatum: "",
            unit: "",
            zoneName: "",
            zoneTopDepth: "",
            zoneBottomDepth: "",
          });
          break;
        default:
          break;
      }
    } else if (tab === "operasional") {
      switch (section) {
        case "Work breakdown structure":
          setWorkBreakdown((prev) => [...prev, workBreakdownForm]);
          setWorkBreakdownForm({
            event: "",
            startDate: "",
            endDate: "",
            remark: "",
          });
          break;
        case "Job document":
          setJobDocument((prev) => [...prev, jobDocumentForm]);
          setJobDocumentForm({
            title: "",
            creatorName: "",
            createDate: "",
            documentType: "",
            itemCategory: "",
            itemSubCategory: "",
            digitalFormat: "",
            originalFileName: "",
            digitalSize: "",
            remark: "",
          });
          break;
        case "Job Operation Days":
          setJobOperationDays((prev) => [...prev, jobOperationDaysForm]);
          setJobOperationDaysForm({
            phase: "",
            depthDatum: "",
            unit: "",
            depthIn: "",
            depthOut: "",
            operationDays: "",
          });
          break;
        case "Job Hazard":
          setJobHazard((prev) => [...prev, jobHazardForm]);
          setJobHazardForm({
            hazardType: "",
            hazardDescription: "",
            severity: "",
            mitigation: "",
            remark: "",
          });
          break;
        default:
          break;
      }
    }
    updateSectionCompletion(tab, section);
  };

  // Handle File Upload for Well Trajectory
  const handleFileUpload = (event) => {
    setWellTrajectoryFile(event.target.files[0]);
    updateSectionCompletion("teknis", "Well Trajectory");
  };

  const handleWellDocumentChange = (field, value) => {
    setWellDocumentData(prev => ({ ...prev, [field]: value }));
    updateSectionCompletion("teknis", "Well Document");
  };

  const handlePorePressureFileUpload = (event) => {
    setPorePressureFile(event.target.files[0]);
    updateSectionCompletion("teknis", "Pore Pressure Fracture Gradient");
  };

  const handleWellLogsFileUpload = (event) => {
    setWellLogsFile(event.target.files[0]);
    updateSectionCompletion("teknis", "Well Logs");
  };

  const handleWellDrillingParameterFileUpload = (event) => {
    setWellDrillingParameterFile(event.target.files[0]);
    updateSectionCompletion("teknis", "Well Drilling Parameter");
  }

  // Update Section Completion
  const updateSectionCompletion = (tab, section) => {
    let isCompleted = false;
    if (tab === "teknis") {
      switch (section) {
        case "Well":
          isCompleted = Object.values(wellData).every((value) => value !== "");
          break;
        case "Koordinat":
          isCompleted = Object.values(koordinatData).every(
            (value) => value !== ""
          );
          break;
        case "Seismic":
          isCompleted = seismicData.lineName !== "";
          break;
        case "Keydates":
          isCompleted = Object.values(keydatesData).every(
            (value) => value !== ""
          );
          break;
        case "Elevasi":
          isCompleted = Object.values(elevasiData).every(
            (value) => value !== ""
          );
          break;
        case "Well Summary":
          isCompleted = wellSummary.length > 0;
          break;
        case "Well Test":
          isCompleted = wellTest.length > 0;
          break;
        case "Well Trajectory":
          isCompleted = wellTrajectoryFile !== null;
          break;
        case "Pore Pressure Fracture Gradient":
          isCompleted = wellTrajectoryFile !== null;
          break;
        default:
          break;
      }
    } else if (tab === "operasional") {
      switch (section) {
        case "Proposed Job":
          isCompleted = Object.values(proposedJob).every(
            (value) => value !== ""
          );
          break;
        case "Work breakdown structure":
          isCompleted = workBreakdown.length > 0;
          break;
        case "Job document":
          isCompleted = jobDocument.length > 0;
          break;
        case "Job Operation Days":
          isCompleted = jobOperationDays.length > 0;
          break;
        case "Job Hazard":
          isCompleted = jobHazard.length > 0;
          break;
        default:
          break;
      }
    }
    setCompletedSections((prev) => ({
      ...prev,
      [tab]: {
        ...prev[tab],
        [section]: isCompleted,
      },
    }));
  };

  // UseEffect to check completion status
  useEffect(() => {
    updateSectionCompletion("teknis", "Well");
    updateSectionCompletion("teknis", "Koordinat");
    updateSectionCompletion("teknis", "Seismic");
    updateSectionCompletion("teknis", "Keydates");
    updateSectionCompletion("teknis", "Elevasi");
    updateSectionCompletion("teknis", "Well Summary");
    updateSectionCompletion("teknis", "Well Test");
    updateSectionCompletion("teknis", "Well Trajectory");
    updateSectionCompletion("teknis", "Pore Pressure Fracture Gradient");

    updateSectionCompletion("operasional", "Proposed Job");
    updateSectionCompletion("operasional", "Work breakdown structure");
    updateSectionCompletion("operasional", "Job document");
    updateSectionCompletion("operasional", "Job Operation Days");
    updateSectionCompletion("operasional", "Job Hazard");
  }, [
    wellData,
    koordinatData,
    seismicData,
    keydatesData,
    elevasiData,
    wellSummary,
    wellTest,
    wellTrajectoryFile,
    porePressureFile,
    proposedJob,
    workBreakdown,
    jobDocument,
    jobOperationDays,
    jobHazard,
  ]);

  return (
    <Grid templateColumns="1fr 250px" gap={8}>
      <Box>
        <Tabs index={activeTab} onChange={(index) => setActiveTab(index)}>
          <TabList>
            <Tab>Teknis</Tab>
            <Tab>Operasional</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <VStack align="stretch" spacing={8}>
                {/* Well section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>UWI</FormLabel>
                      <Input
                        placeholder="Uwi"
                        value={wellData.uwi}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "uwi",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Nama Sumur</FormLabel>
                      <Input
                        placeholder="Nama Sumur"
                        value={wellData.namaSumur}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "namaSumur",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Nama Lengkap Sumur</FormLabel>
                      <Input
                        placeholder="Nama Lengkap Sumur"
                        value={wellData.namaLengkapSumur}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "namaLengkapSumur",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Type Well</FormLabel>
                      <Input
                        placeholder="Type Well"
                        value={wellData.typeWell}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "typeWell",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Well Status</FormLabel>
                      <Input
                        placeholder="Well Status"
                        value={wellData.wellStatus}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "wellStatus",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Well Profile Type</FormLabel>
                      <Input
                        placeholder="Well Profile Type"
                        value={wellData.wellProfileType}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "wellProfileType",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Hydrocarbon Target</FormLabel>
                      <Input
                        placeholder="Hydrocarbon Target"
                        value={wellData.hydrocarbonTarget}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "hydrocarbonTarget",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Environment Type</FormLabel>
                      <Input
                        placeholder="Environment Type"
                        value={wellData.environmentType}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well",
                            "environmentType",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                </Box>

                {/* Koordinat section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Koordinat
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>Surface Longitude</FormLabel>
                      <Input
                        placeholder="Surface Longitude"
                        value={koordinatData.surfaceLongitude}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "surfaceLongitude",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Surface Latitude</FormLabel>
                      <Input
                        placeholder="Surface Latitude"
                        value={koordinatData.surfaceLatitude}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "surfaceLatitude",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Bottom Hole Longitude</FormLabel>
                      <Input
                        placeholder="Bottom Hole Longitude"
                        value={koordinatData.bottomHoleLongitude}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "bottomHoleLongitude",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Bottom Hole Latitude</FormLabel>
                      <Input
                        placeholder="Bottom Hole Latitude"
                        value={koordinatData.bottomHoleLatitude}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "bottomHoleLatitude",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Maximum Inclination</FormLabel>
                      <Input
                        placeholder="Maximum Inclination"
                        value={koordinatData.maximumInclination}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "maximumInclination",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Azimuth</FormLabel>
                      <Input
                        placeholder="Azimuth"
                        value={koordinatData.azimuth}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Koordinat",
                            "azimuth",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                </Box>

                {/* Seismic section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Seismic
                  </Text>
                  <FormControl>
                    <FormLabel>Line Name</FormLabel>
                    <Input
                      placeholder="Line Name"
                      value={seismicData.lineName}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Seismic",
                          "lineName",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                </Box>

                {/* Keydates section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Keydates
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>Spud Date</FormLabel>
                      <Input
                        type="date"
                        value={keydatesData.spudDate}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Keydates",
                            "spudDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Final Drill Date</FormLabel>
                      <Input
                        type="date"
                        value={keydatesData.finalDrillDate}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Keydates",
                            "finalDrillDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <FormControl>
                    <FormLabel>Completion Date</FormLabel>
                    <Input
                      type="date"
                      value={keydatesData.completionDate}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Keydates",
                          "completionDate",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                </Box>

                {/* Elevasi section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Elevasi
                  </Text>
                  <FormControl>
                    <FormLabel>Unit</FormLabel>
                    <Select
                      placeholder="Select Unit"
                      value={elevasiData.unit}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Elevasi",
                          "unit",
                          e.target.value
                        )
                      }
                    >
                      <option value="meters">Meters</option>
                      <option value="feet">Feet</option>
                    </Select>
                  </FormControl>
                  <HStack>
                    <FormControl>
                      <FormLabel>Rotary Table Elev</FormLabel>
                      <Input
                        placeholder="Rotary Table Elev"
                        value={elevasiData.rotaryTableElev}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "rotaryTableElev",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>KB Elev</FormLabel>
                      <Input
                        placeholder="KB Elev"
                        value={elevasiData.kbElev}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "kbElev",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Derrick Floor Elev</FormLabel>
                      <Input
                        placeholder="Derrick Floor Elev"
                        value={elevasiData.derrickFloorElev}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "derrickFloorElev",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Ground Elev</FormLabel>
                      <Input
                        placeholder="Ground Elev"
                        value={elevasiData.groundElev}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "groundElev",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <FormControl>
                    <FormLabel>Mean Sea Level</FormLabel>
                    <Input
                      placeholder="Mean Sea Level"
                      value={elevasiData.meanSeaLevel}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Elevasi",
                          "meanSeaLevel",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Depth Datum</FormLabel>
                    <Select
                      placeholder="Select Depth Datum"
                      value={elevasiData.depthDatum}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Elevasi",
                          "depthDatum",
                          e.target.value
                        )
                      }
                    >
                      <option value="msl">MSL</option>
                      <option value="rt">RT</option>
                      <option value="kb">KB</option>
                    </Select>
                  </FormControl>
                  <HStack>
                    <FormControl>
                      <FormLabel>Kick Off Point</FormLabel>
                      <Input
                        placeholder="Kick Off Point"
                        value={elevasiData.kickOffPoint}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "kickOffPoint",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Maximum TVD</FormLabel>
                      <Input
                        placeholder="Maximum TVD"
                        value={elevasiData.maximumTvd}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "maximumTvd",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Final MD</FormLabel>
                      <Input
                        placeholder="Final MD"
                        value={elevasiData.finalMd}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "finalMd",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Remark</FormLabel>
                      <Input
                        placeholder="Remark"
                        value={elevasiData.remark}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Elevasi",
                            "remark",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                </Box>

                {/* Well Summary section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Summary
                  </Text>
                  <FormControl>
                    <FormLabel>Depth Datum</FormLabel>
                    <Select
                      placeholder="Select Depth Datum"
                      value={wellSummaryForm.depthDatum}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Well Summary",
                          "depthDatum",
                          e.target.value
                        )
                      }
                    >
                      <option value="msl">MSL</option>
                      <option value="rt">RT</option>
                      <option value="kb">KB</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel>Unit</FormLabel>
                    <Select
                      placeholder="Select Unit"
                      value={wellSummaryForm.unit}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Well Summary",
                          "unit",
                          e.target.value
                        )
                      }
                    >
                      <option value="meters">Meters</option>
                      <option value="feet">Feet</option>
                    </Select>
                  </FormControl>
                  <HStack>
                    <FormControl>
                      <FormLabel>Depth</FormLabel>
                      <Input
                        placeholder="Depth"
                        value={wellSummaryForm.depth}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "depth",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Hole Diameter</FormLabel>
                      <Input
                        placeholder="Hole Diameter"
                        value={wellSummaryForm.holeDiameter}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "holeDiameter",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Bit</FormLabel>
                      <Input
                        placeholder="Bit"
                        value={wellSummaryForm.bit}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "bit",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Casing Diameter</FormLabel>
                      <Input
                        placeholder="Casing Diameter"
                        value={wellSummaryForm.casingDiameter}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "casingDiameter",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Casing Grade</FormLabel>
                      <Input
                        placeholder="Casing Grade"
                        value={wellSummaryForm.casingGrade}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "casingGrade",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Casing Weight</FormLabel>
                      <Input
                        placeholder="Casing Weight"
                        value={wellSummaryForm.casingWeight}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "casingWeight",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Logging</FormLabel>
                      <Input
                        placeholder="Logging"
                        value={wellSummaryForm.logging}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "logging",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Mud Program</FormLabel>
                      <Input
                        placeholder="Mud Program"
                        value={wellSummaryForm.mudProgram}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "mudProgram",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Cementing Program</FormLabel>
                      <Input
                        placeholder="Cementing Program"
                        value={wellSummaryForm.cementingProgram}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "cementingProgram",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Bottom Hole Temperature</FormLabel>
                      <Input
                        placeholder="Bottom Hole Temperature"
                        value={wellSummaryForm.bottomHoleTemperature}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "bottomHoleTemperature",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Rate of Penetration</FormLabel>
                      <Input
                        placeholder="Rate of Penetration"
                        value={wellSummaryForm.rateOfPenetration}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "rateOfPenetration",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Remarks</FormLabel>
                      <Input
                        placeholder="Remarks"
                        value={wellSummaryForm.remarks}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Summary",
                            "remarks",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() => handleAddBatch("teknis", "Well Summary")}
                  >
                    Tambah Batch
                  </Button>

                  {wellSummary.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Depth Datum</Th>
                          <Th>Unit</Th>
                          <Th>Depth</Th>
                          <Th>Hole Diameter</Th>
                          <Th>Bit</Th>
                          <Th>Casing Diameter</Th>
                          <Th>Casing Grade</Th>
                          <Th>Casing Weight</Th>
                          <Th>Logging</Th>
                          <Th>Mud Program</Th>
                          <Th>Cementing Program</Th>
                          <Th>Bottom Hole Temperature</Th>
                          <Th>Rate of Penetration</Th>
                          <Th>Remarks</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {wellSummary.map((summary, index) => (
                          <Tr key={index}>
                            <Td>{summary.depthDatum}</Td>
                            <Td>{summary.unit}</Td>
                            <Td>{summary.depth}</Td>
                            <Td>{summary.holeDiameter}</Td>
                            <Td>{summary.bit}</Td>
                            <Td>{summary.casingDiameter}</Td>
                            <Td>{summary.casingGrade}</Td>
                            <Td>{summary.casingWeight}</Td>
                            <Td>{summary.logging}</Td>
                            <Td>{summary.mudProgram}</Td>
                            <Td>{summary.cementingProgram}</Td>
                            <Td>{summary.bottomHoleTemperature}</Td>
                            <Td>{summary.rateOfPenetration}</Td>
                            <Td>{summary.remarks}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>

                {/* Well Test section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Test
                  </Text>
                  <FormControl>
                    <FormLabel>Depth Datum</FormLabel>
                    <Select
                      placeholder="Select Depth Datum"
                      value={wellTestForm.depthDatum}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Well Test",
                          "depthDatum",
                          e.target.value
                        )
                      }
                    >
                      <option value="msl">MSL</option>
                      <option value="rt">RT</option>
                      <option value="kb">KB</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel>Unit</FormLabel>
                    <Select
                      placeholder="Select Unit"
                      value={wellTestForm.unit}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Well Test",
                          "unit",
                          e.target.value
                        )
                      }
                    >
                      <option value="meters">Meters</option>
                      <option value="feet">Feet</option>
                    </Select>
                  </FormControl>
                  <HStack>
                    <FormControl>
                      <FormLabel>Zone Name</FormLabel>
                      <Input
                        placeholder="Zone Name"
                        value={wellTestForm.zoneName}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Test",
                            "zoneName",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Zone Top Depth</FormLabel>
                      <Input
                        placeholder="Zone Top Depth"
                        value={wellTestForm.zoneTopDepth}
                        onChange={(e) =>
                          handleInputChange(
                            "teknis",
                            "Well Test",
                            "zoneTopDepth",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <FormControl>
                    <FormLabel>Zone Bottom Depth</FormLabel>
                    <Input
                      placeholder="Zone Bottom Depth"
                      value={wellTestForm.zoneBottomDepth}
                      onChange={(e) =>
                        handleInputChange(
                          "teknis",
                          "Well Test",
                          "zoneBottomDepth",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() => handleAddBatch("teknis", "Well Test")}
                  >
                    Tambah Batch
                  </Button>

                  {wellTest.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Depth Datum</Th>
                          <Th>Unit</Th>
                          <Th>Zone Name</Th>
                          <Th>Zone Top Depth</Th>
                          <Th>Zone Bottom Depth</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {wellTest.map((test, index) => (
                          <Tr key={index}>
                            <Td>{test.depthDatum}</Td>
                            <Td>{test.unit}</Td>
                            <Td>{test.zoneName}</Td>
                            <Td>{test.zoneTopDepth}</Td>
                            <Td>{test.zoneBottomDepth}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>

                {/* Well Trajectory section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Trajectory
                  </Text>
                  <FormControl>
                    <FormLabel>Upload Well Trajectory File</FormLabel>
                    <Input type="file" onChange={handleFileUpload} />
                  </FormControl>
                  {wellTrajectoryFile && (
                    <Text mt={2}>File uploaded: {wellTrajectoryFile.name}</Text>
                  )}
                </Box>
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Logs
                  </Text>
                  <FormControl>
                    <FormLabel>Upload Well Logs File</FormLabel>
                    <Input type="file" onChange={handleWellLogsFileUpload} />
                  </FormControl>
                  {wellTrajectoryFile && (
                    <Text mt={2}>File uploaded: {wellTrajectoryFile.name}</Text>
                  )}
                </Box>
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Driliing Parameter
                  </Text>
                  <FormControl>
                    <FormLabel>Upload Well Driliing Parameter File</FormLabel>
                    <Input type="file" onChange={handleWellDrillingParameterFileUpload} />
                  </FormControl>
                  {wellTrajectoryFile && (
                    <Text mt={2}>File uploaded: {wellTrajectoryFile.name}</Text>
                  )}
                </Box>
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Well Document
                  </Text>
                  <HStack>
                  <FormControl>
                    <FormLabel>Title</FormLabel>
                    <Input
                      placeholder="Title"
                      value={wellDocumentData.title}
                      onChange={(e) =>
                        handleWellDocumentChange("title", e.target.value)
                      }
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Media Type</FormLabel>
                    <Select
                      placeholder="Select Media Type"
                      value={wellDocumentData.mediaType}
                      onChange={(e) =>
                        handleWellDocumentChange("mediaType", e.target.value)
                      }
                    >
                      <option value="Peta Satuan">Peta Satuan</option>
                      <option value="Harddisk">Harddisk</option>
                      <option value="CDROM">CDROM</option>
                    </Select>
                  </FormControl>
                  </HStack>
                  <FormControl mt={4}>
                    <FormLabel>Document Type</FormLabel>
                    <Input
                      placeholder="Document Type"
                      value={wellDocumentData.documentType}
                      onChange={(e) =>
                        handleWellDocumentChange("documentType", e.target.value)
                      }
                    />
                  </FormControl>
                  <FormControl mt={4}>
                    <FormLabel>Remark</FormLabel>
                    <Input
                      placeholder="Remark"
                      value={wellDocumentData.remark}
                      onChange={(e) =>
                        handleWellDocumentChange("remark", e.target.value)
                      }
                    />
                  </FormControl>
                </Box>

                {/* Pore Pressure Fracture Gradient section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Pore Pressure Fracture Gradient
                  </Text>
                  <FormControl>
                    <FormLabel>
                      Upload Pore Pressure Fracture Gradient File
                    </FormLabel>
                    <Input
                      type="file"
                      onChange={handlePorePressureFileUpload}
                    />
                  </FormControl>
                  {porePressureFile && (
                    <Text mt={2}>File uploaded: {porePressureFile.name}</Text>
                  )}
                </Box>
              </VStack>
            </TabPanel>

            {/* Operasional Tab */}
            <TabPanel>
              <VStack align="stretch" spacing={8}>
                {/* Proposed Job section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Proposed Job
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>Area ID</FormLabel>
                      <Select
                        placeholder="Select Area ID"
                        value={proposedJob.areaId}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "areaId",
                            e.target.value
                          )
                        }
                      >
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                      </Select>
                    </FormControl>
                    <FormControl>
                      <FormLabel>Field ID</FormLabel>
                      <Select
                        placeholder="Select Field ID"
                        value={proposedJob.fieldId}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "fieldId",
                            e.target.value
                          )
                        }
                      >
                        <option value="PHR">PHR</option>
                        <option value="PHM">PHM</option>
                        <option value="PHE">PHE</option>
                      </Select>
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>AFE Number</FormLabel>
                      <Input
                        placeholder="AFE Number"
                        value={proposedJob.afeNumber}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "afeNumber",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Total Budget</FormLabel>
                      <Input
                        placeholder="Total Budget"
                        value={proposedJob.totalBudget}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "totalBudget",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>WPB Year</FormLabel>
                      <Input
                        placeholder="WPB Year"
                        value={proposedJob.wpbYear}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "wpbYear",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Start Date</FormLabel>
                      <Input
                        type="date"
                        value={proposedJob.startDate}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "startDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>End Date</FormLabel>
                      <Input
                        type="date"
                        value={proposedJob.endDate}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "endDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Rig Name</FormLabel>
                      <Input
                        placeholder="Rig Name"
                        value={proposedJob.rigName}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "rigName",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Rig Type</FormLabel>
                      <Select
                        placeholder="Select Rig Type"
                        value={proposedJob.rigType}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "rigType",
                            e.target.value
                          )
                        }
                      >
                        <option value="jackup">Jackup</option>
                        <option value="floater">Floater</option>
                      </Select>
                    </FormControl>
                    <FormControl>
                      <FormLabel>Rig Horse Power</FormLabel>
                      <Input
                        placeholder="Rig Horse Power"
                        value={proposedJob.rigHorsePower}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Proposed Job",
                            "rigHorsePower",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                </Box>

                {/* Work breakdown structure section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Work breakdown structure
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>Event</FormLabel>
                      <Input
                        placeholder="Event"
                        value={workBreakdownForm.event}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Work breakdown structure",
                            "event",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Start Date</FormLabel>
                      <Input
                        type="date"
                        value={workBreakdownForm.startDate}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Work breakdown structure",
                            "startDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>End Date</FormLabel>
                      <Input
                        type="date"
                        value={workBreakdownForm.endDate}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Work breakdown structure",
                            "endDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Remark</FormLabel>
                      <Input
                        placeholder="Remark"
                        value={workBreakdownForm.remark}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Work breakdown structure",
                            "remark",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() =>
                      handleAddBatch("operasional", "Work breakdown structure")
                    }
                  >
                    Tambah Batch
                  </Button>

                  {workBreakdown.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Event</Th>
                          <Th>Start Date</Th>
                          <Th>End Date</Th>
                          <Th>Remark</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {workBreakdown.map((item, index) => (
                          <Tr key={index}>
                            <Td>{item.event}</Td>
                            <Td>{item.startDate}</Td>
                            <Td>{item.endDate}</Td>
                            <Td>{item.remark}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>

                {/* Job Document section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Job Document
                  </Text>
                  <HStack>
                    <FormControl>
                      <FormLabel>Title</FormLabel>
                      <Input
                        placeholder="Title"
                        value={jobDocumentForm.title}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "title",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Creator Name</FormLabel>
                      <Input
                        placeholder="Creator Name"
                        value={jobDocumentForm.creatorName}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "creatorName",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Create Date</FormLabel>
                      <Input
                        type="date"
                        value={jobDocumentForm.createDate}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "createDate",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Document Type</FormLabel>
                      <Input
                        placeholder="Document Type"
                        value={jobDocumentForm.documentType}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "documentType",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Item Category</FormLabel>
                      <Input
                        placeholder="Item Category"
                        value={jobDocumentForm.itemCategory}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "itemCategory",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Item Sub Category</FormLabel>
                      <Input
                        placeholder="Item Sub Category"
                        value={jobDocumentForm.itemSubCategory}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "itemSubCategory",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Digital Format</FormLabel>
                      <Input
                        placeholder="Digital Format"
                        value={jobDocumentForm.digitalFormat}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "digitalFormat",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Original File Name</FormLabel>
                      <Input
                        placeholder="Original File Name"
                        value={jobDocumentForm.originalFileName}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "originalFileName",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Digital Size</FormLabel>
                      <Input
                        placeholder="Digital Size"
                        value={jobDocumentForm.digitalSize}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "digitalSize",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Remark</FormLabel>
                      <Input
                        placeholder="Remark"
                        value={jobDocumentForm.remark}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job document",
                            "remark",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() =>
                      handleAddBatch("operasional", "Job document")
                    }
                  >
                    Tambah Batch
                  </Button>

                  {jobDocument.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Title</Th>
                          <Th>Creator Name</Th>
                          <Th>Create Date</Th>
                          <Th>Document Type</Th>
                          <Th>Item Category</Th>
                          <Th>Item Sub Category</Th>
                          <Th>Digital Format</Th>
                          <Th>Original File Name</Th>
                          <Th>Digital Size</Th>
                          <Th>Remark</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {jobDocument.map((doc, index) => (
                          <Tr key={index}>
                            <Td>{doc.title}</Td>
                            <Td>{doc.creatorName}</Td>
                            <Td>{doc.createDate}</Td>
                            <Td>{doc.documentType}</Td>
                            <Td>{doc.itemCategory}</Td>
                            <Td>{doc.itemSubCategory}</Td>
                            <Td>{doc.digitalFormat}</Td>
                            <Td>{doc.originalFileName}</Td>
                            <Td>{doc.digitalSize}</Td>
                            <Td>{doc.remark}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>

                {/* Job Operation Days section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Job Operation Days
                  </Text>
                  <FormControl>
                    <FormLabel>Phase</FormLabel>
                    <Input
                      placeholder="Phase"
                      value={jobOperationDaysForm.phase}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Operation Days",
                          "phase",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <HStack>
                    <FormControl>
                      <FormLabel>Depth Datum</FormLabel>
                      <Select
                        placeholder="Select Depth Datum"
                        value={jobOperationDaysForm.depthDatum}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job Operation Days",
                            "depthDatum",
                            e.target.value
                          )
                        }
                      >
                        <option value="RT">RT</option>
                        <option value="KB">KB</option>
                      </Select>
                    </FormControl>
                    <FormControl>
                      <FormLabel>Unit</FormLabel>
                      <Select
                        placeholder="Select Unit"
                        value={jobOperationDaysForm.unit}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job Operation Days",
                            "unit",
                            e.target.value
                          )
                        }
                      >
                        <option value="Metriks">Metriks</option>
                        <option value="Imperial">Imperial</option>
                      </Select>
                    </FormControl>
                  </HStack>
                  <HStack>
                    <FormControl>
                      <FormLabel>Depth In</FormLabel>
                      <Input
                        placeholder="Depth In"
                        value={jobOperationDaysForm.depthIn}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job Operation Days",
                            "depthIn",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>Depth Out</FormLabel>
                      <Input
                        placeholder="Depth Out"
                        value={jobOperationDaysForm.depthOut}
                        onChange={(e) =>
                          handleInputChange(
                            "operasional",
                            "Job Operation Days",
                            "depthOut",
                            e.target.value
                          )
                        }
                      />
                    </FormControl>
                  </HStack>
                  <FormControl>
                    <FormLabel>Operation Days</FormLabel>
                    <Input
                      placeholder="Operation Days"
                      value={jobOperationDaysForm.operationDays}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Operation Days",
                          "operationDays",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() =>
                      handleAddBatch("operasional", "Job Operation Days")
                    }
                  >
                    Tambah Batch
                  </Button>

                  {jobOperationDays.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Phase</Th>
                          <Th>Depth Datum</Th>
                          <Th>Unit</Th>
                          <Th>Depth In</Th>
                          <Th>Depth Out</Th>
                          <Th>Operation Days</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {jobOperationDays.map((op, index) => (
                          <Tr key={index}>
                            <Td>{op.phase}</Td>
                            <Td>{op.depthDatum}</Td>
                            <Td>{op.unit}</Td>
                            <Td>{op.depthIn}</Td>
                            <Td>{op.depthOut}</Td>
                            <Td>{op.operationDays}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>

                {/* Job Hazard section */}
                <Box>
                  <Text fontWeight="bold" fontSize="xl">
                    Job Hazard
                  </Text>
                  <FormControl>
                    <FormLabel>Hazard Type</FormLabel>
                    <Select
                      placeholder="Select Hazard Type"
                      value={jobHazardForm.hazardType}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Hazard",
                          "hazardType",
                          e.target.value
                        )
                      }
                    >
                      <option value="Gas Kick">Gas Kick</option>
                      {/* Add more hazard types as needed */}
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel>Hazard Description</FormLabel>
                    <Input
                      placeholder="Hazard Description"
                      value={jobHazardForm.hazardDescription}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Hazard",
                          "hazardDescription",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Severity</FormLabel>
                    <Select
                      placeholder="Select Severity"
                      value={jobHazardForm.severity}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Hazard",
                          "severity",
                          e.target.value
                        )
                      }
                    >
                      <option value="High">High</option>
                      <option value="Low">Low</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel>Mitigation</FormLabel>
                    <Input
                      placeholder="Mitigation"
                      value={jobHazardForm.mitigation}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Hazard",
                          "mitigation",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Remark</FormLabel>
                    <Input
                      placeholder="Remark"
                      value={jobHazardForm.remark}
                      onChange={(e) =>
                        handleInputChange(
                          "operasional",
                          "Job Hazard",
                          "remark",
                          e.target.value
                        )
                      }
                    />
                  </FormControl>
                  <Button
                    mt={4}
                    colorScheme="blue"
                    onClick={() => handleAddBatch("operasional", "Job Hazard")}
                  >
                    Tambah Batch
                  </Button>

                  {jobHazard.length > 0 && (
                    <Table variant="simple" mt={4}>
                      <Thead>
                        <Tr>
                          <Th>Hazard Type</Th>
                          <Th>Hazard Description</Th>
                          <Th>Severity</Th>
                          <Th>Mitigation</Th>
                          <Th>Remark</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {jobHazard.map((hazard, index) => (
                          <Tr key={index}>
                            <Td>{hazard.hazardType}</Td>
                            <Td>{hazard.hazardDescription}</Td>
                            <Td>{hazard.severity}</Td>
                            <Td>{hazard.mitigation}</Td>
                            <Td>{hazard.remark}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                  )}
                </Box>
              </VStack>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
      <Box>
        <NavigationMenu
          completedSections={completedSections}
          activeTab={activeTab === 0 ? "teknis" : "operasional"}
        />
      </Box>
    </Grid>
  );
};

export default OperasiPengajuaanForm;
