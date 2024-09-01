import React, { useState } from "react";
import {
  Flex,
  Box,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Button,
  Heading,
  Text,
  Image,
  HStack,
} from "@chakra-ui/react";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import LoginImage from "../assets/login-images.jpg";
import SplashScreen from "./../Page/Components/SplashScreen";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();
  const [showSplashScreen, setShowSplashScreen] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/auth/token",
        new URLSearchParams({
          username: username,
          password: password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      const token = response.data.access_token;
      localStorage.setItem("token", token);

      const userResponse = await axios.get(
        "http://localhost:8000/auth/user/me",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const userDetails = userResponse.data;
      login(userDetails, token); // Kirim userDetails dan token ke fungsi login di AuthContext

      // Tampilkan splash screen
      setShowSplashScreen(true);
      
    } catch (error) {
      if (error.response) {
        setErrorMessage(() => {
          const details = error.response.data.detail;

          if (details && details.length > 0) {
            if (
              details.length === 2 &&
              details[0].msg === "Field required" &&
              details[1].msg === "Field required"
            ) {
              return "Masukkan Username dan Password";
            }
            if (details.length === 1 && details[0].msg === "Field required") {
              return "Harap Di Isi Secara Lengkap";
            }
          }

          return details;
        });
      }
    }
  };

  const handleSplashScreenComplete = () => {
    navigate("/dashboard");
  };

  if (showSplashScreen) {
    return <SplashScreen onAnimationComplete={handleSplashScreenComplete} />;
  }

  return (
    <Box
      minH="100vh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      bg="gray.100"
      p={8}
    >
      <Flex
        maxW="150vh"
        h="80vh"
        w="full"
        bg="white"
        p={8}
        borderRadius="2xl"
        boxShadow="md"
        alignItems="center"
        gap={4}
      >
        <Box w="50%" mr={6}>
          <Heading mb={2} textAlign="left">
            Welcome Back!
          </Heading>
          <Text fontSize="lg" mb={6}>
            Please log in to manage your site.
          </Text>
          <form onSubmit={handleLogin}>
            <VStack spacing={10}>
              <FormControl id="username" isRequired>
                <FormLabel>Username</FormLabel>
                <Input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your username"
                  size={"lg"}
                />
              </FormControl>

              <FormControl id="password" isRequired>
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  size={"lg"}
                />
              </FormControl>

              {errorMessage && <Text color="red.500">{errorMessage}</Text>}

              <Button
                mt={4}
                colorScheme="teal"
                size={"lg"}
                type="submit"
                width="full"
              >
                Log In
              </Button>
            </VStack>
            <HStack justifyContent={"Center"} mt={2}>
              <Text>Don't have an account?</Text>
              <Button
                colorScheme="teal"
                variant="link"
                size={"lg"}
                onClick={() => navigate("/register")}
              >
                Register
              </Button>
            </HStack>
          </form>
        </Box>
        <Box w="50%" h="full" objectPosition="center">
          <Image
            src={LoginImage}
            alt="Login Image"
            objectFit="cover"
            borderRadius="md"
            w="full"
            h="full"
          />
        </Box>
      </Flex>
    </Box>
  );
};

export default Login;
