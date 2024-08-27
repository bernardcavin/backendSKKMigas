import React ,{ useState,useEffect } from "react";
import {
  Box,
  Button,
  SimpleGrid,
  VStack,
  HStack,
 
} from "@chakra-ui/react";
import { Outlet, useNavigate, Link, useLocation } from "react-router-dom";
import CustomCard from "./../Components/Card/CustomCard"; // Path yang sesuai
import WellTable from "./../Components/Card/WellTable"; // Path yang sesuai
import { FaCheckCircle, FaCogs, FaFlagCheckered } from "react-icons/fa";



const OperasiPengerjaan = ({ handleTambahData }) => {
  const [dataDrilling, setDataDrilling] = useState([]);

  const location = useLocation();

  const [showPengajuanPekerjaan, setShowPengajuanPekerjaan] = useState(true);
  useEffect(() => {
    if (location.pathname === "/dashboard/submission/pengajuanform") {
      setShowPengajuanPekerjaan(!showPengajuanPekerjaan);
    }
  },[location.pathname]);

  const sendData = (data) => {
    setDataDrilling(data);
  };
  const navigate = useNavigate();
  const warnabutton = "teal";
  return (
    <>
      <Box p={5}>
        <VStack spacing={4} align="stretch">
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mt={5}>
            <CustomCard
              icon={FaCheckCircle}
              count={12}
              label="Disetujui"
              bgColor="white"
              iconBgColor="#ECF2FE"
              iconColor="#3478ff"
            />
            <CustomCard
              icon={FaCogs}
              count={5}
              label="Beroperasi"
              bgColor="white"
              iconBgColor="#FEE2E2"
              iconColor="#bd0808"
            />
            <CustomCard
              icon={FaFlagCheckered}
              count={20}
              label="Selesai"
              bgColor="white"
              iconBgColor="#E6FFFA"
              iconColor="#00c9a1"
            />
          </SimpleGrid>
          <HStack justify="flex-end" mt={4} mb={4}>
            <Button
              colorScheme="blue"
              as={Link}
              to="/dashboard/operasi/operasiform"
            >
              Tambah Data
            </Button>
          </HStack>

          {/* Tabel */}
          <Box>
            <WellTable />
          </Box>
        </VStack>
      </Box>
      <Outlet context={{ sendData }} />
    </>
  );
};

export default OperasiPengerjaan;
