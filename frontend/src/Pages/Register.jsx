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

export function RegisterPage() {
  const [namakks, setNamaKks] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [instansi] = useState(""); // Nilai default kosong
  const [detilInstansi] = useState(""); // Nilai default kosong
  const [fieldErrors, setFieldErrors] = useState({}); // Untuk menampung error per field
  const [successMessage, setSuccessMessage] = useState("");

  const navigate = useNavigate(); // Hook untuk navigasi

  const handleRegister = async (e) => {
    e.preventDefault();
    setFieldErrors({});
    setSuccessMessage("");
    if(password !== confirmPassword) {
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
          role:"Admin",
          

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
  };

  return (
    <div className="flex w-full items-center justify-center min-h-screen">
      <Card color="transparent" className="p-6 shadow-2xl" shadow={true}>
        <Typography variant="h4" color="blue-gray" className="text-center">
          Register Akun
        </Typography>
        <Typography color="gray" className="mt-1 font-normal text-center">

        </Typography>
        <form
          className="mt-8 mb-2 w-80 max-w-screen-lg sm:w-96"
          onSubmit={handleRegister}
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
            {fieldErrors.username && (
              <Typography color="red" variant="small" className="mt-1">
                {fieldErrors.username}
              </Typography>
            )}

            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Email
            </Typography>
            <Input
              size="lg"
              placeholder="name@mail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="!border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              required
            />
            {fieldErrors.email && (
              <Typography color="red" variant="small" className="mt-1">
                {fieldErrors.email}
              </Typography>
            )}

            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Password
            </Typography>
            <Input
              type="password"
              size="lg"
              placeholder="********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="!border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              required
            />
            
            <Typography variant="h6" color="blue-gray" className="-mb-3">
              Password Confirm
            </Typography>
            <Input
              type="password"
              size="lg"
              placeholder="*********"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="!border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              required
            />
            {fieldErrors.password && (
              <Typography color="red" variant="small" className="mt-1">
                {fieldErrors.password}
              </Typography>
            )}
          </div>
          {fieldErrors.form && (
            <Typography color="red" className="mt-4 text-center font-normal">
              {fieldErrors.form}
            </Typography>
          )}
          {successMessage && (
            <Typography color="green" className="mt-4 text-center font-normal">
              {successMessage}
            </Typography>
          )}
          <Checkbox
            required
            label={
              <Typography
                variant="small"
                color="gray"
                className="flex items-center font-normal"
              >
                I agree to the
                <a
                  href="#"
                  className="transition-colors font-bold hover:text-gray-900"
                >
                  &nbsp;Terms and Conditions
                </a>
              </Typography>
            }
            containerProps={{ className: "-ml-2.5" }}
          />
          <Button type="submit" className="mt-6" fullWidth>
            Sign Up
          </Button>
          <Typography color="gray" className="mt-4 text-center font-normal">
            Punya Akun?{" "}
            <a href="/" className="font-medium text-gray-900">
              Sign In
            </a>
          </Typography>
        </form>
      </Card>
    </div>
  );
}
