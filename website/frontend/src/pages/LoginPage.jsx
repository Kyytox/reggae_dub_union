import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import IconButton from "@mui/material/IconButton";
import WarningIcon from "@mui/icons-material/Warning";
import { AuthContext } from "../components/AuthContext";
import { postAxios } from "../requests/UtilsAxios";

function LoginPage() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);

  const sxTextField = {
    width: "100%",
    marginTop: "2rem",
  };

  // Var for form
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Var for form errors
  const [usernameError, setUsernameError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  // Var for form Response
  const [ResponseSuccess, setResponseSuccess] = useState("");
  const [ResponseError, setResponseError] = useState("");

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  // TODO: Add form validation
  const handleSubmit = async (event) => {
    event.preventDefault();

    // reset errors
    setUsernameError("");
    setPasswordError("");
    setResponseError("");
    var topValid = true;

    // control username
    if (!username) {
      setUsernameError("Username is required");
      topValid = false;
    }

    // control password
    if (!password) {
      setPasswordError("Password is required");
      topValid = false;
    }

    if (topValid) {
      console.log("Form submitted");

      // call backend flask api /Signup
      const data = {
        username: username,
        password: password,
      };

      try {
        const response = await postAxios("/login", data);
        console.log(response);

        if (response.isAuth === true) {
          login(response.id, response.token);
          setResponseSuccess("Login successful");

          setTimeout(() => {
            navigate("/");
          }, 1500);
        } else {
          setResponseError(response);
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
        id="box-Login"
      >
        <h2 className="text-xl font-bold" id="h2-Signup">
          Login
        </h2>
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
        <Button variant="contained" onClick={handleSubmit} sx={{ mt: 5 }}>
          Login
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

export default LoginPage;
