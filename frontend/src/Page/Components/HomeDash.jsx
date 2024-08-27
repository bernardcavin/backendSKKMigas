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
import Hero from "../../assets/Hero.jpg";
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
                    value="101"
                    label="Operasi"
                    percentage="+2,36%"
                    gradient="linear(to-r, #9BE3FC, #53B4EB)"
                    iconColor="#53B4EB"
                  />
                  <SummaryBox
                    icon={<SettingsIcon />} // Gear
                    value="102"
                    label="P3"
                    percentage={"+2,36%"}
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
                <FilterBar />

                <Grid templateColumns="repeat(3, 1fr)" gap={4} mb={4}>
                  <CustomCard
                    icon={FaCalendarDay}
                    count={20/20}
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
              </TabPanel>
            </TabPanels>
          </Tabs>
        </GridItem>
      </Grid>
    </Box>
  );
};

export default HomeDash;
