import { HStack, Select, Button } from "@chakra-ui/react";

// Filter Bar Component
const FilterBar = () => {
  return (
    <HStack spacing={4} mb={4} align="center" width="100%">
      <Select
        placeholder="Pilih Pekerjaan"
        size="lg"
        variant="filled"
        borderColor="gray.300"
        _hover={{ borderColor: "gray.400" }}
        flex="1"
      >
        <option value="eksplorasi">Eksplorasi</option>
        <option value="exploitation">Eksploitasi</option>
        <option value="workover">Work Over</option>
        <option value="wellservice">Well Service</option>
      </Select>

      <Select
        placeholder="Pilih Laporan"
        size="lg"
        variant="filled"
        borderColor="gray.300"
        _hover={{ borderColor: "gray.400" }}
        flex="1"
      >
        <option value="harian">Harian</option>
        <option value="mingguan">Mingguan</option>
        <option value="bulanan">Bulanan</option>
      </Select>

      <Select
        placeholder="Pilih KKKS"
        size="lg"
        variant="filled"
        borderColor="gray.300"
        _hover={{ borderColor: "gray.400" }}
        flex="1"
      >
        <option value="semua">Semua</option>
      </Select>

      <Button
        colorScheme="blue"
        size="lg"
        fontWeight="bold"
        flex={0.5}
        px={10} // Membuat tombol lebih besar
        _hover={{ bg: "blue.600" }}
      >
        Filter
      </Button>
    </HStack>
  );
};

export default FilterBar;