import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import IconButton from "@mui/material/IconButton";
import WarningIcon from "@mui/icons-material/Warning";
import Box from "@mui/material/Box";

import { AuthContext } from "../components/AuthContext";
import { postAxios } from "../requests/UtilsAxios";
import "../App.css";

function SignupPage() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  // Var for password visibility
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const sxTextField = {
    width: "100%",
    marginTop: "2rem",
  };

  // Var for form
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // Var for form errors
  const [usernameError, setUsernameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPasswordError, setConfirmPasswordError] = useState("");

  // Var for form Response
  const [ResponseSuccess, setResponseSuccess] = useState("");
  const [ResponseError, setResponseError] = useState("");

  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleClickShowConfirmPassword = () =>
    setShowConfirmPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  // TODO: Add form validation
  const handleSubmit = async (event) => {
    event.preventDefault();

    // reset errors
    setUsernameError("");
    setEmailError("");
    setPasswordError("");
    setConfirmPasswordError("");
    setResponseError("");
    var topValid = true;

    // control username
    if (!username) {
      setUsernameError("Username is required");
      topValid = false;
    }

    // control email
    if (!email) {
      setEmailError("Email is required");
      topValid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError("Email is invalid");
      topValid = false;
    }

    // control password
    if (!password) {
      setPasswordError("Password is required");
      topValid = false;
    }

    // control confirm password
    if (!confirmPassword) {
      setConfirmPasswordError("Confirm password is required");
      topValid = false;
    }

    // control password and confirm password
    if (password !== confirmPassword) {
      setConfirmPasswordError("Passwords do not match");
      topValid = false;
    }

    if (topValid) {
      console.log("Form submitted");

      // call backend flask api /Signup
      const data = {
        username: username,
        email: email,
        password: password,
      };

      try {
        const response = await postAxios("/signup", data);
        console.log(response);

        if (response === "User already exists") {
          setResponseError("User already exists");
        } else {
          setResponseSuccess("User created");
          setResponseError("");
          login(response.id, response.token);

          // redirect to home after 3 seconds
          setTimeout(() => {
            navigate("/");
          }, 2500);
        }
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <div className="main-content-auth">
      <Box
        sx={{
          display: "flex",
          flexWrap: "nowrap",
          flexDirection: "column",
          width: "25rem",
          padding: "4rem",
          paddingTop: "2rem",
          marginTop: "5rem",
          borderRadius: "1rem",
          backgroundColor: "#18181b",
        }}
        id="box-Signup"
      >
        <h2 className="text-xl font-bold" id="h2-Signup">
          Signup
        </h2>
        <TextField
          required
          id="email"
          label="Email"
          variant="standard"
          sx={sxTextField}
          onChange={(e) => setEmail(e.target.value)}
          error={!!emailError}
          helperText={emailError}
        />

        <TextField
          required
          autoFocus
          id="username"
          label="Username"
          variant="standard"
          sx={sxTextField}
          onChange={(e) => setUsername(e.target.value)}
          error={!!usernameError}
          helperText={usernameError}
        />

        <TextField
          required
          id="password"
          label="Password"
          variant="standard"
          sx={sxTextField}
          type={showPassword ? "text" : "password"}
          onChange={(e) => setPassword(e.target.value)}
          error={!!passwordError}
          helperText={passwordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <TextField
          required
          id="confirm-password"
          label="Confirm Password"
          variant="standard"
          sx={sxTextField}
          type={showConfirmPassword ? "text" : "password"}
          onChange={(e) => setConfirmPassword(e.target.value)}
          error={!!confirmPasswordError}
          helperText={confirmPasswordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowConfirmPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <Button variant="contained" onClick={handleSubmit} sx={{ mt: 5 }}>
          Sign Up
        </Button>

        {ResponseError && (
          <div className="text-black flex justify-center text-m mt-4 p-2 bg-red-400 rounded">
            <WarningIcon />
            {ResponseError}
          </div>
        )}

        {ResponseSuccess && (
          <div className="text-black flex justify-center text-m mt-4 p-2 bg-green-400 rounded">
            {ResponseSuccess}
          </div>
        )}
      </Box>
    </div>
  );
}

export default SignupPage;
