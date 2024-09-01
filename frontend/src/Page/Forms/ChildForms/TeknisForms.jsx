import React, { useState, useEffect } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Button,
  HStack,
  Select,
  Grid,
  GridItem,
  Heading,
  Flex,
  Menu,
  MenuButton,
  MenuList,
  Table,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  Checkbox,
  MenuItem,
} from "@chakra-ui/react";

import { ChevronDownIcon } from "@chakra-ui/icons";

const CardFormWell = ({ onFormChange }) => {
  const [formData, setFormData] = useState({
    uwi: "string",
    field_id: "string",
    area_id: "string",
    kkks_id: "string",
    well_name: "string",
    alias_long_name: "string",
    well_type: "WILDCAT",
    well_status: "Active",
    well_profile_type: "DIRECTIONAL",
    hydrocarbon_target: "OIL",
    environment_type: "MARINE",
    surface_longitude: 0,
    surface_latitude: 0,
    bottom_hole_longitude: 0,
    bottom_hole_latitude: 0,
    maximum_inclination: 0,
    azimuth: 0,
    line_name: "string",
    spud_date: "2024-08-31T02:04:33.198Z",
    final_drill_date: "2024-08-31T02:04:33.198Z",
    completion_date: "2024-08-31T02:04:33.198Z",
    rotary_table_elev: 0,
    rotary_table_elev_uom: "FEET",
    kb_elev: 0,
    kb_elev_uom: "FEET",
    derrick_floor_elev: 0,
    derrick_floor_elev_uom: "FEET",
    ground_elev: 0,
    ground_elev_uom: "FEET",
    mean_sea_level: 0,
    mean_sea_level_uom: "FEET",
    depth_datum: "RT",
    kick_off_point: 0,
    kick_off_point_uom: "FEET",
    maximum_tvd: 0,
    maximum_tvd_uom: "FEET",
    final_md: 0,
    final_md_uom: "FEET",
    remark: "string",
  });

  useEffect(() => {
    onFormChange(formData);
  }, [formData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const parsedValue =
      value === ""
        ? ""
        : isNaN(value)
        ? value
        : value.includes(".")
        ? parseFloat(value)
        : parseInt(value, 10);
    setFormData((prevData) => ({
      ...prevData,
      [name]: parsedValue,
    }));
  };

  const handleMenuItemClick = (unit) => {
    setFormData((prevData) => ({
      ...prevData,
      rotary_table_elev_uom: unit,
      kb_elev_uom: unit,
      derrick_floor_elev_uom: unit,
      ground_elev_uom: unit,
      mean_sea_level_uom: unit,
      kick_off_point_uom: unit,
      maximum_tvd_uom: unit,
      final_md_uom: unit,
    }));
  };

  const handleInputUOM = (e) => {
    const { value } = e.target;
    setCurrentEntry((prevData) => ({
      ...prevData,
      depth_uom: value,
      length_uom: value,
    }));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentEntry((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleInputChangeWellCasing = (e) => {
    const { name, value } = e.target;
    setWellCasing((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const handleInputChangeWellStraigraphy = (e) => {
    const { name, value } = e.target;
    setWellStratigraphy((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const [tableData, setTableData] = useState([]);

  const [currentEntry, setCurrentEntry] = useState({
    depth_datum: "RT",
    depth: 0,
    depth_uom: "FEET",
    hole_diameter: 0,
    hole_diameter_uom: "INCH",
    bit: "string",
    casing_outer_diameter: 0,
    casing_outer_diameter_uom: "INCH",
    logging: "string",
    mud_program: "string",
    cementing_program: "string",
    bottom_hole_temperature: 0,
    bottom_hole_temperature_uom: "C",
    rate_of_penetration: 0,
    remarks: "string",
  });
  const [tableWellCasing, setTableWellCasing] = useState([]);
  const [wellCasing, setWellCasing] = useState({
    depth_datum: "RT",
    depth: null,
    depth_uom: "FEET",
    length: null,
    length_uom: "FEET",
    hole_diameter: null,
    hole_diameter_uom: "INCH",
    casing_outer_diameter: null,
    casing_outer_diameter_uom: "INCH",
    casing_inner_diameter: null,
    casing_inner_diameter_uom: "INCH",
    casing_grade: "",
    casing_weight: null,
    casing_weight_uom: "PPF",
    connection: "",
    description: "",
  });
  const [TablewellStratigraphy, setTablewellStratigraphy] = useState([]);
  const [WellStratigraphy, setWellStratigraphy] = useState({
    depth_datum: "RT",
    depth: 0,
    depth_uom: "FEET",
    stratigraphy_id: "string",
  });

  const handleAddClick = () => {
    const newEntry = { ...currentEntry };
    setTableData((prevData) => [...prevData, newEntry]);
    setFormData((prevData) => ({
      ...prevData,
      well_summary: [...(prevData.well_summary || []), newEntry], // Ensure well_summary is an array and append the new entry
    }));
    // Reset wellCasing after adding
    setCurrentEntry({
      depth_datum: "RT",
      depth: 0,
      depth_uom: "FEET",
      hole_diameter: 0,
      hole_diameter_uom: "INCH",
      bit: "string",
      casing_outer_diameter: 0,
      casing_outer_diameter_uom: "INCH",
      logging: "string",
      mud_program: "string",
      cementing_program: "string",
      bottom_hole_temperature: 0,
      bottom_hole_temperature_uom: "C",
      rate_of_penetration: 0,
      remarks: "string",
    });
  };

  const handleWellCasing = () => {
    const newEntry = { ...wellCasing };
    setTableWellCasing((prevData) => [...prevData, newEntry]);
    setFormData((prevData) => ({
      ...prevData,
      well_casing: [...(prevData.well_casing || []), newEntry], // Ensure well_casing is an array and append newEntry
    }));
    // Reset currentEntry after adding
    setWellCasing({
      depth_datum: "RT",
      depth: 0,
      depth_uom: "FEET",
      length: 0,
      length_uom: "FEET",
      hole_diameter: 0,
      hole_diameter_uom: "INCH",
      casing_outer_diameter: 0,
      casing_outer_diameter_uom: "INCH",
      casing_inner_diameter: 0,
      casing_inner_diameter_uom: "INCH",
      casing_grade: "string",
      casing_weight: 0,
      casing_weight_uom: "PPF",
      connection: "",
      description: "",
    });
  };
  const handleWellStratichy = () => {
    const newEntry = { ...WellStratigraphy };
    setTablewellStratigraphy((prevData) => [...prevData, newEntry]);
    setFormData((prevData) => ({
      ...prevData,
      well_stratigraphy: [...(prevData.well_stratigraphy || []), newEntry], // Ensure well_casing is an array and append newEntry
    }));
    // Reset currentEntry after adding
    setWellStratigraphy({
        depth_datum: "RT",
        depth: 0,
        depth_uom: "FEET",
        stratigraphy_id: "",
    });
  };
  return (
    <>
      <Box borderWidth="1px" borderRadius="lg" p={6} m="auto">
        <Flex justifyContent="space-between" alignItems="center" mb={6}>
          <Heading size="lg">New Exploration Well</Heading>
          <Menu>
            <MenuButton
              as={Button}
              rightIcon={<ChevronDownIcon />}
              variant="outline"
            >
              Pilih Satuan
            </MenuButton>
            <MenuList>
              <MenuItem onClick={() => handleMenuItemClick("FEET")}>
                FEET
              </MenuItem>
              <MenuItem onClick={() => handleMenuItemClick("METER")}>
                METER
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>

        <VStack spacing={4} align="stretch">
          <HStack spacing={4}>
            <FormControl>
              <FormLabel>UWI</FormLabel>
              <Input
                name="uwi"
                value={formData.uwi}
                onChange={handleChange}
                placeholder="UWI"
              />
            </FormControl>
            <FormControl>
              <FormLabel>Well Name</FormLabel>
              <Input
                name="wellName"
                value={formData.wellName}
                onChange={handleChange}
                placeholder="Nama Sumur"
              />
            </FormControl>
          </HStack>
          <HStack spacing={4}>
            <FormControl>
              <FormLabel>Alias Long Name</FormLabel>
              <Input
                name="aliasLongName"
                value={formData.aliasLongName}
                onChange={handleChange}
                placeholder="Nama Lengkap Sumur"
              />
            </FormControl>
            <FormControl>
              <FormLabel>Well Type</FormLabel>
              <Select
                name="well_type"
                placeholder="J-Type"
                onChange={handleChange}
              >
                <option value="DELINEATION">DELINEATION</option>
                <option value="WILDCAT">WILDCAT</option>
                <option value="INFILL">INFILL</option>
                <option value="PRODUCER">PRODUCER</option>
                <option value="INJECTION">INJECTION</option>
                <option value="STEPOUT">STEOPOUT</option>
              </Select>
            </FormControl>
          </HStack>
          <HStack spacing={4}>
            <FormControl>
              <FormLabel>Well Profile Type</FormLabel>
              <Select
                name="well_profile_type"
                placeholder="J-Type"
                onChange={handleChange}
              >
                <option value="DIRECTIONAL">DIRECTIONAL</option>
                <option value="HORIZONTAL">HORIZONTAL</option>
                <option value="VERTICAL">VERTICAL</option>
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Environment Type</FormLabel>
              <Select
                name="environment_type"
                placeholder="J-Type"
                onChange={handleChange}
              >
                <option value="SWAMP">SWAMP</option>
                <option value="MARINE">MARINE</option>
                <option value="LAND">LAND</option>
              </Select>
            </FormControl>
          </HStack>
        </VStack>
      </Box>

      <Box
        borderWidth="1px"
        borderRadius="lg"
        p={6}
        boxShadow="md"
        bg="white"
        mt={6}
      >
        <VStack align="stretch" spacing={4}>
          <Heading size="md" display="flex" alignItems="center">
            <Box as="span" mr={2}>
              ↗️
            </Box>
            Directional
          </Heading>

          <FormControl>
            <FormLabel>Directional Type</FormLabel>
            <Select
              name="directionalType"
              placeholder="J-Type"
              onChange={handleChange}
            >
              <option value="j-type">J-Type</option>
              <option value="s-type">S-Type</option>
              <option value="horizontal">Horizontal</option>
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel>Kick Off Point</FormLabel>
            <Input
              name="kick_off_point"
              placeholder="kick off point"
              onChange={handleChange}
            />
          </FormControl>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Maximum Inclination</FormLabel>
                <Input
                  name="maximum_inclination"
                  placeholder="maximum inclination"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Azimuth</FormLabel>
                <Input
                  name="azimuth"
                  type="number"
                  placeholder="Azimuth"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
          </Grid>
        </VStack>
      </Box>

      <Box borderWidth="1px" borderRadius="lg" p={6} mt={4}>
        <VStack align="stretch" spacing={4}>
          <Heading size="md" display="flex" alignItems="center">
            <Box as="span" mr={2}>
              📍
            </Box>
            Well Location
          </Heading>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Surface Longitude</FormLabel>
                <Input
                  name="surface_longitude"
                  placeholder="Surface longitude"
                  type="number"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Surface Latitude</FormLabel>
                <Input
                  type="number"
                  name="surface_latitude"
                  placeholder="Surface latitude"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
          </Grid>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Bottom Hole Longitude</FormLabel>
                <Input
                  name="bottom_hole_longitude"
                  placeholder="bottom hole longitude"
                  onChange={handleChange}
                  type="number"
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Bottom Hole Latitude</FormLabel>
                <Input
                  name="bottom_hole_latitude"
                  placeholder="bottom hole latitude"
                  onChange={handleChange}
                  type="number"
                />
              </FormControl>
            </GridItem>
          </Grid>
        </VStack>
      </Box>
      <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md" bg="white">
        <VStack align="stretch" spacing={4}>
          <Heading size="md" display="flex" alignItems="center">
            <Box as="span" mr={2}>
              🌐
            </Box>
            Elevations and Depths
          </Heading>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Rotary Table Elevation</FormLabel>
                <Input
                  name="rotary_table_elev"
                  placeholder="rotary table elev"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Kelly Bushing Elevation</FormLabel>
                <Input
                  name="kellyBushingElev"
                  placeholder="kelly bushing elev"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
          </Grid>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Derrick Floor Elevation</FormLabel>
                <Input
                  name="derrick_floor_elev"
                  placeholder="derrick floor elev"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Ground Elevation</FormLabel>
                <Input
                  name="ground_elev"
                  placeholder="ground elev"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
          </Grid>

          <FormControl>
            <FormLabel>Mean Sea Level</FormLabel>
            <Input
              name="mean_sea_level"
              placeholder="mean sea level"
              onChange={handleChange}
            />
          </FormControl>

          <Grid templateColumns="repeat(2, 1fr)" gap={4}>
            <GridItem>
              <FormControl>
                <FormLabel>Final MD</FormLabel>
                <Input
                  name="final_md"
                  placeholder="final md"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
            <GridItem>
              <FormControl>
                <FormLabel>Maximum TVD</FormLabel>
                <Input
                  name="maximum_tvd"
                  placeholder="maximum tvd"
                  onChange={handleChange}
                />
              </FormControl>
            </GridItem>
          </Grid>
        </VStack>
      </Box>

      <VStack spacing={6} align="stretch">
        <Box
          borderWidth="1px"
          borderRadius="lg"
          p={6}
          boxShadow="md"
          bg="white"
        >
          <VStack align="stretch" spacing={4}>
            <Heading size="md" display="flex" alignItems="center">
              <Box as="span" mr={2}>
                📊
              </Box>
              Seismic
            </Heading>

            <FormControl>
              <FormLabel>Seismic Line Name</FormLabel>
              <Input
                name="seismicLineName"
                placeholder="Seismic line name"
                onChange={handleChange}
              />
            </FormControl>
          </VStack>
        </Box>

        <Box
          borderWidth="1px"
          borderRadius="lg"
          p={6}
          boxShadow="md"
          bg="white"
        >
          <VStack align="stretch" spacing={4}>
            <Heading size="md" display="flex" alignItems="center">
              <Box as="span" mr={2}>
                📅
              </Box>
              Key Dates
            </Heading>

            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              <GridItem>
                <FormControl>
                  <FormLabel>Spud Date</FormLabel>
                  <Input
                    name="spud_date"
                    placeholder="spud date"
                    type="date"
                    onChange={handleChange}
                  />
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Final Drill Date</FormLabel>
                  <Input
                    name="final_drill_date"
                    placeholder="final drill date"
                    type="date"
                    onChange={handleChange}
                  />
                </FormControl>
              </GridItem>
            </Grid>

            <FormControl>
              <FormLabel>Completion Date</FormLabel>
              <Input
                name="completionDate"
                placeholder="completion date"
                type="date"
                onChange={handleChange}
              />
            </FormControl>
          </VStack>
        </Box>
      </VStack>

      <Grid templateColumns="repeat(1, 1fr)" gap={3}>
        <GridItem colSpan={1}>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Flex justifyContent="space-between" alignItems="center" mb={6}>
              <Heading size="lg">Well Summary</Heading>
              <Box>
                <Select
                  name="unit"
                  onChange={handleInputUOM}
                  value={currentEntry.bottom_hole_temperature_uom}
                >
                  <option value="METER">METER</option>
                  <option value="FEET">FEET</option>
                </Select>
              </Box>
            </Flex>
            <VStack spacing={4} align="stretch">
              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <FormControl>
                  <FormLabel>Depth</FormLabel>
                  <Input
                    name="depth"
                    type="number"
                    value={currentEntry.depth}
                    onChange={handleInputChange}
                    placeholder="Depth"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Hole Diameter</FormLabel>
                  <Input
                    name="hole_diameter"
                    value={currentEntry.hole_diameter}
                    onChange={handleInputChange}
                    placeholder="Hole Diameter"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Casing Outer Diameter</FormLabel>
                  <Input
                    name="casing_outer_diameter"
                    value={currentEntry.casing_outer_diameter}
                    onChange={handleInputChange}
                    placeholder="Casing Outer Diameter"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Mud Program</FormLabel>
                  <Input
                    name="mud_program"
                    value={currentEntry.mud_program}
                    onChange={handleInputChange}
                    placeholder="Mud Program"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Bit</FormLabel>
                  <Input
                    name="bit"
                    value={currentEntry.bit}
                    onChange={handleInputChange}
                    placeholder="Bit"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Logging Program</FormLabel>
                  <Input
                    name="logging"
                    value={currentEntry.logging}
                    onChange={handleInputChange}
                    placeholder="Logging Program"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Cementing Program</FormLabel>
                  <Input
                    name="cementing_program"
                    value={currentEntry.cementing_program}
                    onChange={handleInputChange}
                    placeholder="Cementing Program"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Bottom Hole Temperature</FormLabel>
                  <Input
                    name="bottom_hole_temperature"
                    value={currentEntry.bottom_hole_temperature}
                    onChange={handleInputChange}
                    placeholder="Bottom Hole Temperature"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Rate of Penetration</FormLabel>
                  <Input
                    name="rate_of_penetration"
                    value={currentEntry.rate_of_penetration}
                    onChange={handleInputChange}
                    placeholder="Rate of Penetration"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Remarks</FormLabel>
                  <Input
                    name="remarks"
                    value={currentEntry.remarks}
                    onChange={handleInputChange}
                    placeholder="Remarks"
                  />
                </FormControl>
              </Grid>
              <Button colorScheme="blue" onClick={handleAddClick}>
                Add
              </Button>
            </VStack>
          </Box>
        </GridItem>
        <GridItem colSpan={1}>
          {/* You can place additional content or another form here */}
        </GridItem>
        <GridItem>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Heading size="md" mb={4}>
              Table Well Summary
            </Heading>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Bit</Th>
                  <Th>Depth</Th>
                  <Th>Hole Diameter</Th>
                  <Th>Casing Diameter</Th>
                  <Th>Logging</Th>
                  <Th>Mud Program</Th>
                  <Th>Bottom Hole Temperature</Th>
                  <Th>RATE PENETRATION</Th>
                  <Th>Remarks</Th>
                  {/* Tambahkan header lain sesuai kebutuhan */}
                </Tr>
              </Thead>
              <Tbody>
                {tableData.map((row, index) => (
                  <Tr key={index}>
                    <Td>{row.bit}</Td>
                    <Td>{row.depth}</Td>
                    <Td>{row.hole_diameter}</Td>
                    <Td>{row.casing_outer_diameter}</Td>
                    <Td>{row.logging}</Td>
                    <Td>{row.mud_program}</Td>
                    <Td>{row.bottom_hole_temperature}</Td>
                    <Td>{row.rate_of_penetration}</Td>
                    <Td>{row.remarks}</Td>
                    {/* Tambahkan sel lain sesuai kebutuhan */}
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </GridItem>
      </Grid>

      <Grid templateColumns="repeat(1, 1fr)" gap={3}>
        <GridItem colSpan={1}>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Flex justifyContent="space-between" alignItems="center" mb={6}>
              <Heading size="lg">Well Casing</Heading>
              <Box>
                <Select
                  name="unit"
                  onChange={handleInputUOM}
                  value={wellCasing.length_uom}
                >
                  <option value="METER">METER</option>
                  <option value="FEET">FEET</option>
                </Select>
              </Box>
            </Flex>
            <VStack spacing={4} align="stretch">
              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <FormControl>
                  <FormLabel>Depth</FormLabel>
                  <Input
                    name="depth"
                    type="number"
                    value={wellCasing.depth}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Depth"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Strati Graphy</FormLabel>
                  <Input
                    name="stratigraphy_id"
                    type="number"
                    value={wellCasing.stratigraphy_id}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Depth"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Hole Diameter</FormLabel>
                  <Input
                    name="hole_diameter"
                    value={wellCasing.hole_diameter}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Hole Diameter"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Casing Outer Diameter</FormLabel>
                  <Input
                    name="casing_outer_diameter"
                    value={wellCasing.casing_outer_diameter}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Casing Outer Diameter"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Casing Inner Diameter</FormLabel>
                  <Input
                    name="casing_inner_diameter"
                    value={wellCasing.casing_inner_diameter}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Casing Outer Diameter"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Casing Grade</FormLabel>
                  <Input
                    name="casing_grade"
                    value={wellCasing.casing_grade}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Mud Program"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Casing Weight</FormLabel>
                  <Input
                    name="casing_weight"
                    value={wellCasing.casing_weight}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Casing Weight"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Logging Program</FormLabel>
                  <Input
                    name="connection"
                    value={wellCasing.connection}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Logging Program"
                  />
                </FormControl>
                <FormControl>
                  <FormLabel>Description</FormLabel>
                  <Input
                    name="description"
                    value={wellCasing.description}
                    onChange={handleInputChangeWellCasing}
                    placeholder="Cementing Program"
                  />
                </FormControl>
              </Grid>
              <Button colorScheme="blue" onClick={handleWellCasing}>
                Add
              </Button>
            </VStack>
          </Box>
        </GridItem>

        <GridItem>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Heading size="md" mb={4}>
              Table Well Casing
            </Heading>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Depth</Th>
                  <Th>Hole Diameter</Th>

                  <Th>Length</Th>
                  <Th>Casing Outer </Th>
                  <Th>Casing Inner</Th>
                  <Th>Casing Grade</Th>
                  <Th>Casing Weight</Th>
                  <Th>Connection</Th>
                  <Th>Description</Th>
                  {/* Tambahkan header lain sesuai kebutuhan */}
                </Tr>
              </Thead>
              <Tbody>
                {tableWellCasing.map((row, index) => (
                  <Tr key={index}>
                    <Td>{row.depth}</Td>
                    <Td>{row.hole_diameter}</Td>
                    <Td>{row.casing}</Td>
                    <Td>{row.length}</Td>
                    <Td>{row.casing_outer_diameter}</Td>
                    <Td>{row.casing_inner_diameter}</Td>
                    <Td>{row.casing_grade}</Td>
                    <Td>{row.casing_weight}</Td>
                    <Td>{row.connection}</Td>
                    <Td>{row.description}</Td>
                    {/* Tambahkan sel lain sesuai kebutuhan */}
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </GridItem>
      </Grid>

      <Grid templateColumns="repeat(2, 1fr)" gap={3} mt={3}>
        <GridItem colSpan={1}>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Flex justifyContent="space-between" alignItems="center" mb={6}>
              <Heading size="lg">STRATIGRAPHY</Heading>
              <Box>
                <Select
                  name="unit"
                  onChange={handleInputUOM}
                  value={wellCasing.length_uom}
                >
                  <option value="METER">METER</option>
                  <option value="FEET">FEET</option>
                </Select>
              </Box>
            </Flex>
            <VStack spacing={4} align="stretch">
              <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                <Flex gap={2}>
                  <FormControl>
                    <FormLabel>Stratigraphy</FormLabel>
                    <Input
                      name="stratigraphy_id"
                      value={WellStratigraphy.stratigraphy_id}
                      onChange={handleInputChangeWellStraigraphy}
                      placeholder="stratigraphy"
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>depth</FormLabel>
                    <Input
                      name="depth"
                      type="number"
                      value={WellStratigraphy.depth}
                      onChange={handleInputChangeWellStraigraphy}
                      placeholder="Depth"
                    />
                  </FormControl>
                </Flex>
              </Grid>
              <Button colorScheme="blue" onClick={handleWellStratichy}>
                Add
              </Button>
            </VStack>
          </Box>
        </GridItem>

        <GridItem>
          <Box borderWidth="1px" borderRadius="lg" p={6} boxShadow="md">
            <Heading size="md" mb={4}>
              Table Straticgraphy
            </Heading>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Depth</Th>
                  <Th>Hole Diameter</Th>

                  {/* Tambahkan header lain sesuai kebutuhan */}
                </Tr>
              </Thead>
              <Tbody>
                {TablewellStratigraphy.map((row, index) => (
                  <Tr key={index}>
                    <Td>{row.depth}</Td>
                    <Td>{row.stratigraphy_id}</Td>

                    {/* Tambahkan sel lain sesuai kebutuhan */}
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </GridItem>
      </Grid>
    </>
  );
};

export default CardFormWell;
