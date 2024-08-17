import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  Input,
  Checkbox,
  Button,
  Typography,
} from "@material-tailwind/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext"; // Pastikan import useAuth sesuai

axios.defaults.withCredentials = true;

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth(); // Mengambil fungsi login dari context

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/auth/token", new URLSearchParams({
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
      // console.log(response);

      // console.log(token);

      localStorage.setItem("token", token);

      // Ambil detail pengguna
      const userResponse = await axios.get("http://localhost:8000/auth/user/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      // console.log(userResponse);
      const userDetails = userResponse.data;
      localStorage.setItem("user", JSON.stringify(userDetails));

      login(); // Update state autentikasi di context
      navigate("/dashboard"); // Redirect ke dashboard
    } catch (error) {
      if (error.response) {
        // Permintaan berhasil dikirim tetapi server merespons dengan status kode yang tidak dalam rentang 2xx
        setErrorMessage(`Login failed: ${error.response.data.message || 'Please try again.'}`);
        console.error('Login error response:', error.response.data);
      } else if (error.request) {
        // Permintaan dibuat tetapi tidak ada respons yang diterima
        setErrorMessage('Login failed: No response from server.');
        console.error('Login error request:', error.request);
      } else {
        // Kesalahan lain
        setErrorMessage('Login failed: An error occurred.');
        console.error('Login error:', error.message);
      }
    }

  };

  return (
    <div className="flex w-full items-center justify-center min-h-screen">
      <Card className=" shadow-lg   p-6" shadow={true}>
        <Typography variant="h4" color="blue-gray" className="text-center">
          Sign In
        </Typography>

        <form
          className="mt-8 mb-2 w-80 max-w-screen-lg sm:w-96"
          onSubmit={handleLogin}
        >
          <div className="mb-4 flex flex-col gap-6">
            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Username
            </Typography>
            <Input
              size="lg"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="!border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              required
            />
            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Password
            </Typography>
            <Input
              type="password"
              size="lg"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="!border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              required
            />
          </div>
          {errorMessage && (
            <Typography color="red" className="text-center">
              {errorMessage}
            </Typography>
          )}
          <Checkbox
            label={
              <Typography
                variant="small"
                color="gray"
                className="flex items-center font-normal"
              >
                Remember me
              </Typography>
            }
            containerProps={{ className: "-ml-2.5" }}
          />
          <Button type="submit" className="mt-6" fullWidth>
            Sign In
          </Button>
          <Typography color="gray" className="mt-4 text-center font-normal">
            Don't have an account?{" "}
            <a href="/register" className="font-medium text-gray-900">
              Sign Up
            </a>
          </Typography>
        </form>
      </Card>
    </div>
  );
}

export default LoginPage;
