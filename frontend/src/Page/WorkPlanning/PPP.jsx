import React from "react";
import {
  Box,
  Button,
  SimpleGrid,
  VStack,
  HStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
} from "@chakra-ui/react";
import { Outlet, Link } from "react-router-dom";
import { FaClipboardCheck, FaFileUpload, FaHandshake } from "react-icons/fa";

import CustomCard from "./../Components/Card/CustomCard"; // Path yang sesuai
import WellTable from "./../Components/Card/WellTable"; // Path yang sesuai

const PPP = ({ handleTambahData }) => {
  const warnabutton = "teal";
  return (
    <>
      <Box p={5}>
        <VStack spacing={4} align="stretch">
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} mt={5}>
            <CustomCard
              icon={FaClipboardCheck}
              count={12}
              label="Pekerjaan Selesai"
              bgColor="white"
              iconBgColor="#ECF2FE"
              iconColor="#3478ff"
            />
            <CustomCard
              icon={FaFileUpload}
              count={5}
              label="Diajukan PPP"
              bgColor="white"
              iconBgColor="#FEE2E2"
              iconColor="#bd0808"
            />
            <CustomCard
              icon={FaHandshake}
              count={20}
              label="Selesai PPP"
              bgColor="white"
              iconBgColor="#E6FFFA"
              iconColor="#00c9a1"
            />
          </SimpleGrid>
          <HStack justify="flex-end" mt={4} mb={4}>
            <Button colorScheme="blue" as={Link} to={"/dashboard/ppp/pppform"}>
              Tambah Data
            </Button>
          </HStack>

          {/* Tabel */}
          <Box>
            <WellTable />
          </Box>
        </VStack>
      </Box>
      <Outlet />
    </>
  );
};

export default PPP;
