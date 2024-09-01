// eslint-disable-next-line no-unused-vars
import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import "./PageExploitasi/Animation.css";
import {
  Box,
  Flex,
  Avatar,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Text,
  HStack,
  useDisclosure,
  Button,
  MenuDivider,
} from "@chakra-ui/react";
import { BellIcon, HamburgerIcon, CloseIcon } from "@chakra-ui/icons";
import { FaRegClock } from "react-icons/fa";
import { useAuth } from "../../Auth/AuthContext";
import { useNavigate } from "react-router-dom";

const Navbar = ({ appName = "Aplikasi Pengeboran Dan Sumuran", nameUser }) => {
  const { logout } = useAuth();
  const navigator = useNavigate();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const logoutOnClick = () => {
    logout();

    navigator("/");
  };
  const [notifications] = useState([
    {
      message: "You have a new message!",
      time: "2 mins ago",
      icon: "📩",
    },
    {
      message: "Your profile was updated.",
      time: "10 mins ago",
      icon: "🔄",
    },
    {
      message: "New comment on your post.",
      time: "30 mins ago",
      icon: "💬",
    },
  ]);

  // Replace this with actual user data
  const userName = "John Doe";

  return (
    <Box bg="white" shadow={"md"} px={4} py={1} borderRadius={"lg"}>
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <IconButton
          size="md"
          icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
          aria-label="Open Menu"
          display={{ md: "none" }}
          onClick={isOpen ? onClose : onOpen}
          color="#10042C"
        />
        <Box color="#10042C" width={"300px"} fontWeight="bold">
          <marquee >{appName}</marquee>
        </Box>
        <Flex alignItems="center" gap={4}>
          <Menu borderRadius={"lg"}>
            <MenuButton
              as={IconButton}
              aria-label="notifications"
              icon={<BellIcon />}
              variant="ghost"
              color="#10042C"
            />
            <MenuList w={"300px"} px={4} py={4} borderRadius={"lg"} zIndex={10}>
              {notifications.length > 0 ? (
                notifications.map((notification, index) => (
                  <MenuItem key={index} borderRadius={"lg"}>
                    <HStack>
                      <Text fontSize="xl">{notification.icon}</Text>
                      <Box>
                        <Text fontSize="md">{notification.message}</Text>
                        <HStack spacing={1}>
                          <FaRegClock color="#718096" />
                          <Text fontSize="sm" color="#718096">
                            {notification.time}
                          </Text>
                        </HStack>
                      </Box>
                    </HStack>
                  </MenuItem>
                ))
              ) : (
                <MenuItem>No new notifications</MenuItem>
              )}
            </MenuList>
          </Menu>
          <Menu>
            <MenuButton
              as={Button}
              rounded={"full"}
              variant={"link"}
              cursor={"pointer"}
              minW={0}
            >
              <HStack>
                <Text>{nameUser}</Text>
                <Avatar size={"sm"} src={"https://bit.ly/sage-adebayo"} />
              </HStack>
            </MenuButton>
            <MenuList backgroundColor={"white"} zIndex={10}>
              <MenuItem>Profile</MenuItem>
              <MenuItem>Settings</MenuItem>
              <MenuDivider />
              <MenuItem onClick={logoutOnClick}>Logout</MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </Flex>

      {isOpen ? (
        <Box pb={4} display={{ md: "none" }}>
          {/* Mobile menu can be added here */}
        </Box>
      ) : null}
    </Box>
  );
};

Navbar.propTypes = {
  appName: PropTypes.string, // Ensure appName is a string
};

export default Navbar;
