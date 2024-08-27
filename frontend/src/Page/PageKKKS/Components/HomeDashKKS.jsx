import {
  Box,
  Grid,
  GridItem,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  SimpleGrid,
  CircularProgress,
  CircularProgressLabel,
  Text,
  Image,
} from "@chakra-ui/react";
import Plot from "react-plotly.js";
import { CheckIcon, EditIcon, SettingsIcon, CloseIcon } from "@chakra-ui/icons";
import WellTable from "../Components/Card/WellTable";
import FilterBar from "./Card/FilterBar";
import SummaryBox from "./Card/SummaryBox";
import Hero from "../../../assets/Hero.jpg";
import CustomCard from "./Card/CustomCard";
import { FaCalendarDay, FaChartLine, FaChartPie } from "react-icons/fa";
import PropTypes from "prop-types";

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

const trace1 = {
  x: ["Eksplorasi", "Eksploitasi", "Workover", "Well Service"],
  y: [7, 567, 196, 0],
  name: "Primary Data",
  type: "bar",
  text: [7, 567, 196, 0],
  textposition: "auto",
  hoverinfo: "none",
  marker: {
    color: ["#4CAF50", "#FF5252", "#2196F3", "#FFC107"],
  },
};

const trace2 = {
  x: ["Eksplorasi", "Eksploitasi", "Workover", "Well Service"],
  y: [5, 51, 8, 0],
  name: "Secondary Data",
  type: "bar",
  text: [5, 51, 8, 0],
  textposition: "auto",
  hoverinfo: "none",
  marker: {
    color: ["#81C784", "#FF8A80", "#64B5F6", "#FFD54F"],
  },
};

const data = [trace1, trace2];

const layout = {
  title: "Activity Type Distribution",
  xaxis: { title: "Activity Type" },
  yaxis: { title: "Count" },
  barmode: "group",
  bargap: 0.15,
  bargroupgap: 0.1,
  width: 1000,
  height: 600,
};
// Komponen untuk grafik batang dengan line chart kumulatif di dalamnya
const CombinedBarLineChart = () => <Plot data={data} layout={layout} />;

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

const MultiSeriesChart = () => {
  // Generate dates for x-axis (30 days)
  const generateDates = (count) => {
    const dates = [];
    let currentDate = new Date(2024, 11, 2); // Start from December 2, 2024
    for (let i = 0; i < count; i++) {
      dates.push(currentDate.toISOString().split("T")[0]);
      currentDate.setDate(currentDate.getDate() - 1);
    }
    return dates;
  };

  const dates = generateDates(30);

  // Actual data from the chart
  const getRandomInt = (min, max) =>
    Math.floor(Math.random() * (max - min)) ;

  const rencana = Array.from({ length: 30 }, () => getRandomInt(0, 2));
  const realisasi = Array.from({ length: 30 }, () => getRandomInt(0, 2));
  // console.log(rencana);
  

  // Calculate cumulative data
  const cumulativeSum = (arr) =>
    arr.reduce(
      (sum, value) => [
        ...sum,
        sum.length > 0 ? sum[sum.length - 1] + value : value,
      ],
      []
    );

  console.log(cumulativeSum(rencana));

  const outlookKumulatif = cumulativeSum(rencana);
  const realisasiKumulatif = cumulativeSum(realisasi);

  const data = [
    {
      x: dates,
      y: rencana,
      type: "bar",
      name: "Rencana",
      marker: { color: "rgba(158,202,225,0.8)" },
      yaxis: "y2",
      width: 0.4,
    },
    {
      x: dates,
      y: realisasi,
      type: "bar",
      name: "Realisasi",
      marker: { color: "rgba(107,174,214,0.8)" },
      yaxis: "y2",
      width: 0.4,
    },
    {
      x: dates,
      y: outlookKumulatif,
      type: "scatter",
      mode: "lines",
      name: "Outlook Kumulatif",
      line: { color: "rgb(31,119,180)", width: 2 },
    },
    {
      x: dates,
      y: realisasiKumulatif,
      type: "scatter",
      mode: "lines",
      name: "Realisasi Kumulatif",
      line: { color: "rgb(44,160,44)", width: 2 },
    },
  ];

  const layout = {
    title: "Rencana vs Realisasi",
    xaxis: {
      title: "",
      tickangle: 45,
      tickformat: "%d %b %Y",
      tickfont: { size: 10 },
      dtick: 86400000 * 2, // Show every other day
    },
    yaxis: {
      title: "Cumulative Value",
      side: "left",
      range: [0, 8],
      tickfont: { size: 10 },
    },
    yaxis2: {
      title: "Daily Value",
      side: "right",
      overlaying: "y",
      range: [0, 2],
      tickfont: { size: 10 },
    },
    legend: {
      x: 1.05,
      y: 1,
      xanchor: "left",
      yanchor: "top",
      bgcolor: "rgba(255,255,255,0.8)",
      bordercolor: "rgba(0,0,0,0.1)",
      borderwidth: 1,
      font: { size: 10 },
    },
    barmode: "group",
    bargap: 0.15,
    bargroupgap: 0.1,
    width: 1500,
    height: 600,
    margin: { l: 50, r: 150, t: 50, b: 100 }, // Increased right margin to accommodate legend
    plot_bgcolor: "white",
    paper_bgcolor: "white",
  };

  return (
    <div className="chart-container">
      <Plot data={data} layout={layout} config={{ responsive: true }} />
    </div>
  );
};

const HomeDashKKKS = () => {
  return (
    <Box p={4}>
      <Grid templateColumns="repeat(5, 1fr)" gap={4}>
        <GridItem colSpan={5}>
          <Box
            borderRadius="2xl"
            bg="white"
            boxShadow="md"
            overflow="hidden"
            position="relative"
            height="200px" // Membuat height lebih rendah untuk bagian welcome
          >
            <Image
              src={Hero} // Ganti dengan URL gambar Anda
              alt="Background Image"
              width="100%"
              height="100%"
              objectFit="cover"
            />
            <Box
              position="absolute"
              top="0"
              left="0"
              width="100%"
              height="100%"
              bg="rgba(0, 0, 0, 0.4)"
              color="white"
              p={5}
              display="flex"
              flexDirection="column"
              justifyContent="center"
              textAlign="center"
            >
              <Text fontSize="2xl" fontWeight="bold">
                Selamat Datang di SIPS
              </Text>
              <Text fontSize="lg">Sistem Informasi Pengoboran dan Sumuran</Text>
            </Box>
          </Box>
        </GridItem>

        <GridItem colSpan={5}>
          <Tabs variant="soft-rounded" colorScheme="green">
            <TabList>
              <Tab>Summary</Tab>
              <Tab>Progress</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid templateColumns="repeat(4, 1fr)" gap={4}>
                  <SummaryBox
                    icon={<CheckIcon />}
                    value="102"
                    label="Disetujui"
                    percentage="+2,36%"
                    gradient="linear(to-r, #3EC7AD, #80F571)"
                    iconColor="#3EC7AD"
                  />
                  <SummaryBox
                    icon={<EditIcon />} // Pisau bedah
                    value="102"
                    label="Operasi"
                    percentage="+2,36%"
                    gradient="linear(to-r, #9BE3FC, #53B4EB)"
                    iconColor="#53B4EB"
                  />
                  <SummaryBox
                    icon={<SettingsIcon />} // Gear
                    value="102"
                    label="P3"
                    percentage="+2,36%"
                    gradient="linear(to-r, #74A7FB, #397BFE)"
                    iconColor="#397BFE"
                  />
                  <SummaryBox
                    icon={<CloseIcon />} // Exit
                    value="102"
                    label="Close Out"
                    percentage="+2,36%"
                    gradient="linear(to-r, #8D6DF6, #6940FE)"
                    iconColor="#6940FE"
                  />
                </Grid>
                <Box mt={8}>
                  <WellTable />
                </Box>
              </TabPanel>

              <TabPanel>
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
                      <CombinedBarLineChart />
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

                <Box
                  width={"100%"}
                  borderRadius="2xl"
                  bg="white"
                  boxShadow="md"
                  p={5}
                  mt={4}
                  height="100%"
                >
                  <FilterBar />

                  <Grid templateColumns="repeat(3, 1fr)" gap={4} mt={4} mb={4}>
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
                </Box>
                <MultiSeriesChart />
              </TabPanel>
            </TabPanels>
          </Tabs>
        </GridItem>
      </Grid>
    </Box>
  );
};

export default HomeDashKKKS;
