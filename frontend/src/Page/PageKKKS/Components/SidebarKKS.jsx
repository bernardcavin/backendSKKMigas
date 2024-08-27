import React, { useEffect, useState } from "react";
import {
  Box,
  VStack,
  Link as ChakraLink,
  Image,
  List,
  ListItem,
  Collapse,
  Icon,
  Text,
} from "@chakra-ui/react";
import {
  FaHome,
  FaTools,
  FaMap,
  FaToolbox,
  FaCog,
  FaHammer,
  FaCogs,
  FaChevronDown,
  FaChevronRight,
} from "react-icons/fa";
import Logo from "../../../assets/logo.png";
import { useLocation, Link } from "react-router-dom"; // Import Link from react-router-dom

const SidebarKKS = ({ handleMenuValue }) => {
  const location = useLocation();
  const [openMenu, setOpenMenu] = useState(null);
  const [onClickPage, setOnClickPage] = useState("");

  useEffect(() => {
    if (location.pathname.includes("/dashboard/submission")) {
      setOnClickPage("submission");
    } else if (location.pathname.includes("/dashboard/operasi")) {
      setOnClickPage("operation");
    } else if (location.pathname.includes("/dashboard/ppp")) {
      setOnClickPage("ppp");
    } else if (location.pathname.includes("/dashboard")) {
      setOnClickPage("homeDash");
    }
  }, [location.pathname]);

  const handleMenuClick = (menuName) => {
    setOpenMenu(openMenu === menuName ? null : menuName);
  };

  return (
    <Box
      bg="white"
      w="250px"
      h="100vh"
      p={4}
      color="#10042C"
      boxShadow="md"
      position="sticky" // Menggunakan position: sticky
      top={0} // Menempelkan SidebarKKS ke bagian atas viewport
      overflowY="auto" // Mengaktifkan scrollbar jika konten SidebarKKS melebihi tinggi viewport
    >
      <Box
        flex={1}
        margin={"auto"}
        justifyItems={"center"}
        w={"fit-content"}
        marginBottom={"30px"}
      >
        <Image src={Logo} alt="SKK Migas" w={"120px"} />
      </Box>
      <VStack align="start" spacing={4}>
        <ChakraLink
          as={Link} // Use Link from react-router-dom
          to="/skk/dashboard"
          px={4}
          py={4}
          rounded="md"
          _hover={{ bg: "#f5f5f5" }}
          width="full"
          display="flex"
          alignItems="center"

        
        >
          <Icon as={FaHome} mr={2} />
          Dashboard
        </ChakraLink>

        {/* Exploration Section */}
        <Box width="full">
          <ChakraLink
            px={4}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            display="flex"
            alignItems="center"
            onClick={() => handleMenuClick("exploration")}
          >
            <Icon as={FaMap} mr={2} />
            Exploration
            <Box ml="auto">
              {openMenu === "exploration" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )}
            </Box>
          </ChakraLink>
          <Collapse in={openMenu === "exploration"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/submission"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg={onClickPage === "submission" ? "#e0e0e0" : "none"}
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>Submission</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/operasi"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg={onClickPage === "operation" ? "#e0e0e0" : "none"}
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Operations</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/ppp"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg={onClickPage === "ppp" ? "#e0e0e0" : "none"}
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>P3</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Close Out</Text>
                </ChakraLink>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* development Section */}
        <Box width="full">
          <ChakraLink
            px={4}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            display="flex"
            alignItems="center"
            onClick={() => handleMenuClick("development")}
          >
            <Icon as={FaTools} mr={2} />
            Development
            <Box ml="auto">
              {openMenu === "development" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )}
            </Box>
          </ChakraLink>
          <Collapse in={openMenu === "development"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/development/submission"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>Submission</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/development/operations"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Operations</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/development/p3"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>P3</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/development/closeout"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Close Out</Text>
                </ChakraLink>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* Work Over Section */}
        <Box width="full">
          <ChakraLink
            px={4}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            display="flex"
            alignItems="center"
            onClick={() => handleMenuClick("workover")}
          >
            <Icon as={FaHammer} mr={2} />
            Work Over
            <Box ml="auto">
              {openMenu === "workover" ? <FaChevronDown /> : <FaChevronRight />}
            </Box>
          </ChakraLink>
          <Collapse in={openMenu === "workover"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/workover/submission"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>Submission</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/workover/operations"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Operations</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/workover/p3"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>P3</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/workover/closeout"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Close Out</Text>
                </ChakraLink>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* Well Service Section */}
        <Box width="full">
          <ChakraLink
            px={4}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            display="flex"
            alignItems="center"
            onClick={() => handleMenuClick("wellservice")}
          >
            <Icon as={FaCogs} mr={2} />
            Well Service
            <Box ml="auto">
              {openMenu === "wellservice" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )}
            </Box>
          </ChakraLink>
          <Collapse in={openMenu === "wellservice"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/wellservice/submission"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>Submission</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/wellservice/operations"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Operations</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/wellservice/p3"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaToolbox} mr={2} />
                  <Text>P3</Text>
                </ChakraLink>
              </ListItem>
              <ListItem>
                <ChakraLink
                  as={Link}
                  to="/dashboard/wellservice/closeout"
                  px={3}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  display="flex"
                  alignItems="center"
                  bg="#f9f9f9"
                >
                  <Icon as={FaCog} mr={2} />
                  <Text>Close Out</Text>
                </ChakraLink>
              </ListItem>
            </List>
          </Collapse>
        </Box>
      </VStack>
    </Box>
  );
};

export default SidebarKKS;
