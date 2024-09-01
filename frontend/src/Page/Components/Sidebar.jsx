import React, { useEffect, useState } from "react";
import {
  Box,
  VStack,
  Button,
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
import Logo from "../../assets/logo.png";
import { useLocation, Link, useNavigate } from "react-router-dom";

const Sidebar = ({ handleMenuValue }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [openMenu, setOpenMenu] = useState(null);
  const [onClickPage, setOnClickPage] = useState("");

  useEffect(() => {
    if (location.pathname.includes("/dashboard/planning")) {
      setOnClickPage("Planning");
    } else if (location.pathname.includes("/dashboard/operasi")) {
      setOnClickPage("operation");
    } else if (location.pathname.includes("/dashboard/ppp")) {
      setOnClickPage("ppp");
    } else if (location.pathname.includes("/dashboard")) {
      setOnClickPage("homeDash");
    } else if (location.pathname.includes("/development")) {
      setOnClickPage("development");
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
      boxShadow= '0px 1px 2px rgba(0, 0, 0, 0.10)'
      position="sticky"
      top={0}
      overflowY="auto"
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
        <Button
          as={Link}
          to="/dashboard"
          px={4}
          fontSize={"20px"}
          py={4}
          rounded="md"
          _hover={{ bg: "#f5f5f5" }}
          width="full"
          justifyContent="flex-start"
          leftIcon={<Icon as={FaHome} />}
          variant="ghost"
        >
          Dashboard
        </Button>

        {/* Exploration Section */}
        <Box width="full">
          <Button
            px={4}
            fontSize={"20px"}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            justifyContent="space-between"
            onClick={() => handleMenuClick("exploration")}
            leftIcon={<Icon as={FaMap} />}
            rightIcon={
              openMenu === "exploration" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )
            }
            variant="ghost"
          >
            Exploration
          </Button>
          <Collapse in={openMenu === "exploration"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/planning"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "Planning" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  Planning
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/operasi"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "operation" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Operations
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/ppp"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "ppp" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  P3
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg="#f9f9f9"
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Close Out
                </Button>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* Development Section */}
        <Box width="full">
          <Button
            as={Link}
            
            px={4}
            fontSize={"20px"}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            justifyContent="space-between"
            onClick={() => handleMenuClick("development")}
            leftIcon={<Icon as={FaTools} />}
            rightIcon={
              openMenu === "development" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )
            }
            variant="ghost"
          >
            Development
          </Button>
          <Collapse in={openMenu === "development"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/planning"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "Planning" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  Planning
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/operasi"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "operation" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Operations
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/ppp"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "ppp" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  P3
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg="#f9f9f9"
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Close Out
                </Button>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* Work Over Section */}
        <Box width="full">
          <Button
            as={Link}
            px={4}
            fontSize={"20px"}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            justifyContent="space-between"
            onClick={() => handleMenuClick("workover")}
            leftIcon={<Icon as={FaHammer} />}
            rightIcon={
              openMenu === "workover" ? <FaChevronDown /> : <FaChevronRight />
            }
            variant="ghost"
          >
            Work Over
          </Button>
          <Collapse in={openMenu === "workover"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/planning"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "Planning" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  Planning
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/operasi"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "operation" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Operations
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/ppp"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "ppp" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  P3
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg="#f9f9f9"
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Close Out
                </Button>
              </ListItem>
            </List>
          </Collapse>
        </Box>

        {/* Well Service Section */}
        <Box width="full">
          <Button
            as={Link}
            
            px={4}
            fontSize={"20px"}
            py={4}
            rounded="md"
            _hover={{ bg: "#f5f5f5" }}
            width="full"
            justifyContent="space-between"
            onClick={() => handleMenuClick("wellservice")}
            leftIcon={<Icon as={FaCogs} />}
            rightIcon={
              openMenu === "wellservice" ? (
                <FaChevronDown />
              ) : (
                <FaChevronRight />
              )
            }
            variant="ghost"
          >
            Well Service
          </Button>
          <Collapse in={openMenu === "wellservice"}>
            <List spacing={2} pl={4} mt={2} styleType="none">
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/planning"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "Planning" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  Planning
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/operasi"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "operation" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Operations
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  as={Link}
                  to="/dashboard/ppp"
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg={onClickPage === "ppp" ? "#e0e0e0" : "none"}
                  leftIcon={<Icon as={FaToolbox} />}
                  variant="ghost"
                >
                  P3
                </Button>
              </ListItem>
              <ListItem>
                <Button
                  px={3}
                  fontSize={"18px"}
                  py={2}
                  rounded="md"
                  _hover={{ bg: "#e0e0e0" }}
                  width="full"
                  justifyContent="flex-start"
                  bg="#f9f9f9"
                  leftIcon={<Icon as={FaCog} />}
                  variant="ghost"
                >
                  Close Out
                </Button>
              </ListItem>
            </List>
          </Collapse>
        </Box>
      </VStack>
    </Box>
  );
};

export default Sidebar;
