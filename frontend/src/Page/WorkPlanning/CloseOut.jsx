import React from "react";
import {
  Box,
  Button,
  ButtonGroup,
  Heading,
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

const CloseOut = () => {
  const warnabutton = "teal";
  return (
    <Box p={5}>
      <VStack spacing={4} align="stretch">
        <Box mt={25}>
          <ButtonGroup variant="outline" spacing={2}>
            <Button colorScheme={warnabutton} variant={"solid"}>
              Selesai PPP
            </Button>
            <Button colorScheme={warnabutton} variant={"solid"}>
              Diajukan
            </Button>
            <Button colorScheme={warnabutton} variant={"solid"}>
              Selesai
            </Button>
          </ButtonGroup>
        </Box>

        <HStack justify="flex-end">
          <Button colorScheme="blue">Tambah Data</Button>
        </HStack>

        <Box
          borderWidth="1px"
          borderRadius="lg"
          overflow="hidden"
          boxShadow="sm"
        >
          <TableContainer>
            <Table variant="simple">
              <TableCaption placement="top">
                Tabel Data Status CloseOut Pekerjaan
              </TableCaption>
              <Thead>
                <Tr>
                  <Th>Status</Th>
                  <Th>Count</Th>
                </Tr>
              </Thead>
              <Tbody>
                <Tr>
                  <Td>Status 1</Td>
                  <Td>10</Td>
                </Tr>
              </Tbody>
            </Table>
          </TableContainer>
        </Box>
      </VStack>
    </Box>
  );
};

export default CloseOut;
