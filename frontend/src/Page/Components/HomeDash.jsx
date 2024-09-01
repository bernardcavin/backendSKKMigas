import {
  Box,
  Grid,
  GridItem,
  CircularProgress,
  CircularProgressLabel,
  Text,
  Tr,
  Td,
  Flex,
  Image,
} from "@chakra-ui/react";
import Plot from "react-plotly.js";
import { CheckIcon, EditIcon, SettingsIcon, CloseIcon } from "@chakra-ui/icons";
import WellTable from "../Components/Card/WellTable";
import FilterBar from "./Card/FilterBar";
import SummaryBox from "./Card/SummaryBox";
import Hero from "../../assets/Hero.jpg";
import { SimpleGrid } from "@chakra-ui/react";
import CustomCard from "./Card/CustomCard";
import { FaCalendarDay, FaChartLine, FaChartPie } from "react-icons/fa";
import PropTypes from "prop-types";
import HeaderTitle from "./Card/HeaderTitle";
import TableDashboard from "./Card/TableDashboard";
import DashboardBarChart from "./Card/DashboardBarChart";
import { FiArrowUp, FiInfo } from "react-icons/fi";
import { useState } from "react";

// Data yang dibutuhkan
const progressData = [
  { label: "Eksplorasi", value: 85, color: "#3182CE", lineValue: 75 }, // Blue
  { label: "Exploitation", value: 69, color: "#DD6B20", lineValue: 65 }, // Orange
  { label: "Work Over", value: 46, color: "#38A169", lineValue: 55 }, // Green
  { label: "Well Service", value: 68, color: "#805AD5", lineValue: 70 }, // Purple
];

const monthlyData = [
  { month: "Jan", planning: 1000, actual: 800 },
  { month: "Feb", planning: 1200, actual: 900 },
  { month: "Mar", planning: 1500, actual: 1200 },
  { month: "Apr", planning: 1800, actual: 1400 },
  { month: "May", planning: 2000, actual: 1700 },
  { month: "Jun", planning: 2200, actual: 1900 },
  { month: "Jul", planning: 2500, actual: 2100 },
  { month: "Aug", planning: 2700, actual: 2400 },
  { month: "Sep", planning: 3000, actual: 2600 },
  { month: "Oct", planning: 3200, actual: 2900 },
  { month: "Nov", planning: 3500, actual: 3100 },
  { month: "Dec", planning: 3800, actual: 3300 },
];

// Fungsi untuk menghitung data kumulatif
const cumulativeData = (data) => {
  let cumulative = 0;
  return data.map((item) => {
    cumulative += item;
    return cumulative;
  });
};

// Komponen untuk grafik batang dengan line chart kumulatif di dalamnya
const CombinedBarLineChart = () => (
  <Plot
    data={[
      {
        x: monthlyData.map((item) => item.month),
        y: monthlyData.map((item) => item.planning),
        type: "bar",
        name: "Perencanaan",
        marker: { color: "#3182CE" },
        text: monthlyData.map((item) => item.planning),
        textposition: "outside",
        yaxis: "y1",
      },
      {
        x: monthlyData.map((item) => item.month),
        y: monthlyData.map((item) => item.actual),
        type: "bar",
        name: "Terealisasi",
        marker: { color: "#38A169" },
        text: monthlyData.map((item) => item.actual),
        textposition: "outside",
        yaxis: "y1",
      },
      {
        x: monthlyData.map((item) => item.month),
        y: cumulativeData(monthlyData.map((item) => item.planning)),
        type: "scatter",
        mode: "lines+markers",
        name: "Kumulatif Perencanaan",
        line: { color: "#3182CE", width: 2 },
        marker: { color: "#3182CE" },
        yaxis: "y2",
      },
      {
        x: monthlyData.map((item) => item.month),
        y: cumulativeData(monthlyData.map((item) => item.actual)),
        type: "scatter",
        mode: "lines+markers",
        name: "Kumulatif Terealisasi",
        line: { color: "#38A169", width: 2 },
        marker: { color: "#38A169" },
        yaxis: "y2",
      },
    ]}
    layout={{
      width: "1100",
      title: "",
      height: "600",
      paper_bgcolor: "transparent",
      plot_bgcolor: "transparent",
      barmode: "group",
      xaxis: { automargin: true },
      yaxis: {
        title: "Jumlah",
        side: "left",
        automargin: true,
        showgrid: true,
        zeroline: true,
      },
      yaxis2: {
        title: "Jumlah Kumulatif",
        overlaying: "y",
        side: "right",
        automargin: true,
        showgrid: false,
        zeroline: false,
      },
      showlegend: true,
      legend: { orientation: "h", y: -0.2 },
    }}
    config={{ responsive: true }}
    useResizeHandler={true}
    style={{ width: "100%", height: "100%" }}
  />
);

// Komponen untuk Circular Progress Bar
const CircularProgressBar = ({ label, value, color }) => (
  <Box textAlign="center">
    <CircularProgress value={value} color={color} size="120px">
      <CircularProgressLabel fontSize="xl">{value}%</CircularProgressLabel>
    </CircularProgress>
    <Text mt={2} fontSize="xl">
      {label}
    </Text>
  </Box>
);
CircularProgressBar.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  color: PropTypes.string.isRequired,
};

const HomeDash = () => {
  const dateNow = new Date();
  const formatter = new Intl.DateTimeFormat("id-ID", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  const titlePekerjaanKUPS = [
    "Info",
    "Rencana",
    "Realisasi",
    "Percentage",
    "Change",
  ];
  const data = [
    {
      info: "Exploration",
      rencana: 50,
      realisasi: 12,
      percentage: 24,
      change: 1,
    },
    {
      info: "Development",
      rencana: 990,
      realisasi: 150,
      percentage: 15,
      change: 15,
    },
    {
      info: "Workover",
      rencana: 906,
      realisasi: 197,
      percentage: 22,
      change: null,
    },
    {
      info: "Well Service",
      rencana: 35690,
      realisasi: 7559,
      percentage: 21,
      change: 562,
    },
  ];

  const dataKKKS = [
    {
      kkks: "KKKS1",
      exploration: 50,
      development: 12,
      workover: 45,
      wellservice: 80,
    },
    {
      kkks: "KKKS1",
      exploration: 50,
      development: 12,
      workover: 24,
      wellservice: 100,
    },
    {
      kkks: "KKKS1",
      exploration: 50,
      development: 12,
      workover: 24,
      wellservice: 100,
    },
  ];

  const titlePekerjaanKUPSKKS = [
    "Info",
    "KKKS",
    "Explorasi",
    "Development",
    "Workover",
    "Well Service",
  ];

  const formattedDate = formatter.format(dateNow);
  return (
    <Box p={4}>
      <Grid templateColumns="repeat(5, 1fr)" gap={4}>
        {/* <GridItem colSpan={5}>
          <HeaderTitle
            title={"Realisasi Kegiatan Pengeboran & KUPS"}
            subtitle={formattedDate}
          >
            <Grid templateColumns={"repeat(2, 1fr)"} gap={8}>
              <TableDashboard headers={titlePekerjaanKUPS}>
                {data.map((row, index) => (
                  <Tr key={index}>
                    <Td textAlign={"center"}>
                      <Flex>
                        <FiInfo color="" size={"30px"} />
                      </Flex>
                    </Td>
                    <Td>
                      <Text>{row.info}</Text>
                    </Td>
                    <Td>{row.rencana.toLocaleString()}</Td>
                    <Td>
                      <Flex justifyContent="flex-start" alignItems="center">
                        {row.realisasi}
                        {row.change && (
                          <Box ml={2} color="green.500">
                            <Flex alignItems="center">
                              <FiArrowUp />
                              <Text fontSize="md" ml={1}>
                                {row.change}
                              </Text>
                            </Flex>
                          </Box>
                        )}
                      </Flex>
                    </Td>
                    <Td>{row.percentage}%</Td>
                  </Tr>
                ))}
              </TableDashboard>
              <DashboardBarChart />
            </Grid>
          </HeaderTitle>
        </GridItem>
        <GridItem colSpan={5}>
          <HeaderTitle
            title={"Rencana Kegiatan Pengeboran & KUPS KKKS"}
            subtitle={"Realisasi pekerjaan tiap KKKS"}
          >
            <TableDashboard headers={titlePekerjaanKUPSKKS}>
              {dataKKKS.map((row, index) => {
                return (
                  <Tr key={index}>
                    <Td>
                      <Flex>
                        <FiInfo color="" size={"30px"} />
                      </Flex>
                    </Td>
                    <Td width={"40%"}>{row.kkks}</Td>
                    <Td
                      bg={
                        row.exploration < 45
                          ? "red.500"
                          : row.exploration < 60
                          ? "orange.500"
                          : row.exploration < 100
                          ? "yellow.500"
                          : "green.500"
                      }
                    >
                      {row.exploration}
                    </Td>
                    <Td
                      bg={
                        row.development < 45
                          ? "red.500"
                          : row.development < 60
                          ? "orange.500"
                          : row.development < 100
                          ? "yellow.500"
                          : "green.500"
                      }
                    >
                      {row.development}
                    </Td>
                    <Td
                      bg={
                        row.workover < 45
                          ? "red.500"
                          : row.workover < 60
                          ? "orange.500"
                          : row.workover < 100
                          ? "yellow.500"
                          : "green.500"
                      }
                    >
                      {row.workover}
                    </Td>
                    <Td
                      bg={
                        row.wellservice < 45
                          ? "red.500"
                          : row.wellservice < 60
                          ? "orange.500"
                          : row.wellservice < 100
                          ? "yellow.500"
                          : "green.500"
                      }
                    >
                      {row.wellservice}
                    </Td>
                  </Tr>
                );
              })}
            </TableDashboard>
          </HeaderTitle>
        </GridItem> */}

        <GridItem colSpan={5}>
          <FilterBar />
          <Grid templateColumns="repeat(3, 1fr)" gap={4} mb={4}>
            <CustomCard
              icon={FaCalendarDay}
              count={20 / 20}
              label="Rencana/Realisasi"
              bgColor="white"
              iconBgColor="#E6FFFA"
              iconColor="#00c9a1"
            />
            <CustomCard
              icon={FaChartLine}
              count={20}
              label="Realisasi"
              bgColor="white"
              iconBgColor="#ffe6ea"
              iconColor="#a3001b"
            />
            <CustomCard
              icon={FaChartPie}
              count={20}
              label="Pencapaian 2024"
              bgColor="white"
              iconBgColor="#e6ecff"
              iconColor="#2255ff"
            />
          </Grid>

          <Grid templateColumns="2fr 1fr" gap={4}>
            <GridItem>
              <Box
                width={"100%"}
                borderRadius="2xl"
                bg="white"
                boxShadow="md"
                p={5}
                height="100%"
              >
                <CombinedBarLineChart/>
              </Box>
            </GridItem>
            <GridItem>
              <SimpleGrid columns={1} spacing={4}>
                {progressData.map((data, index) => (
                  <CircularProgressBar
                    key={index}
                    label={data.label}
                    value={data.value}
                    color={data.color}
                  />
                ))}
              </SimpleGrid>
              
            </GridItem>
          </Grid>
        </GridItem>
      </Grid>
    </Box>
  );
};

export default HomeDash;
