
import React, { useEffect, useState } from 'react';
import {
    Flex, Card, CardBody, CardHeader, Center, Divider, Box, VStack, FormControl, FormLabel, Input, Button, Heading, Text
} from '@chakra-ui/react';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';  // Pastikan axios diimpor


const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [fieldErrors, setFieldErrors] = useState({});

    const [email, setEmail] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/utils/db/all').then((response) => {
            console.log(response.data);
        })
    })

    const handleDaftar = async (e) => {
        
        e.preventDefault();
        setFieldErrors({});
        setSuccessMessage("");
        if (password !== confirmPassword) {
            setFieldErrors({ password: "Password and confirm password do not match." });
            return;
        }
        try {
            const response = await axios.post(
                "http://localhost:8000/auth/user/create",
                {
                    username: username,
                    email: email,
                    kkks_id: "Pemerintah",
                    password: password,
                    role: "Admin",


                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            if (response.status === 200) {
                console.log(response.data);
                setSuccessMessage(
                    "Registration successful! Redirecting to login page..."
                );
                setTimeout(() => {
                    navigate("/"); // Arahkan ke halaman login setelah 3 detik
                }, 3000); // Waktu tunggu 3 detik
            }
        } catch (error) {
            if (error.response) {
                const errorDetail = error.response.data.detail || "";
                const errors = {};

                if (errorDetail.includes("Email already registered")) {
                    errors.email = "Email already registered.";
                }
                if (errorDetail.includes("Username already exists")) {
                    errors.username = "Username already exists.";
                }

                setFieldErrors(errors);
                console.error("Error response:", error.response.data);
            } else if (error.request) {
                setFieldErrors({
                    form: "No response received from the server. Please try again later.",
                });
                console.error("Error request:", error.request);
            } else {
                setFieldErrors({
                    form: `Error during registration: ${error.message}`,
                });
                console.error("Error message:", error.message);
            }
        }
    }
    return (

        <Box
            minH="100vh"
            display="flex"
            alignItems="center"
            justifyContent="center"
            bg="gray.100"
            p={6}>
            <Box
                maxW="md"
                w="full"
                bg="white"
                p={8}
                borderRadius="md"
                boxShadow="md"
            >
                <Heading mb={6} textAlign="center">
                    Register
                </Heading>
                <form onSubmit={handleDaftar}>
                    <VStack spacing={4}>
                        <FormControl id="Email" isRequired>
                            <FormLabel>Email</FormLabel>
                            <Input
                                type="text"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Enter your email"
                            />
                        </FormControl>
                        <FormControl id="username" isRequired>
                            <FormLabel>Username</FormLabel>
                            <Input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter your username"
                            />
                        </FormControl>

                        <FormControl id="password" isRequired>
                            <FormLabel>Password</FormLabel>
                            <Input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter your password"
                            />
                        </FormControl>
                        <FormControl id="confPassword" isRequired>
                            <FormLabel>ConfirmPassword</FormLabel>
                            <Input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Confirm You Password"
                            />
                        </FormControl>
                        {fieldErrors.form && <Text color="red.500">{fieldErrors.form}</Text>}
                        {successMessage && <Text color="green.500">{successMessage}</Text>}
                        {errorMessage && <Text color="red.500">{errorMessage}</Text>}

                        <Button
                            mt={4}
                            colorScheme="teal"
                            type="submit"
                            width="full"
                        >
                            Register
                        </Button>
                    </VStack>
                </form>
            </Box>
        </Box>

    )
}

export default Register