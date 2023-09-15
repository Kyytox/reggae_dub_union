import React, { useState } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import IconButton from "@mui/material/IconButton";
import "./auth.css";
import postAxios from "./utils";

function Register() {
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const sxTextField = {
        width: "100%",
        marginTop: "2rem",
    };

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [usernameError, setUsernameError] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [confirmPasswordError, setConfirmPasswordError] = useState("");

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
        setPasswordError("");
        setConfirmPasswordError("");
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

            // call backend flask api /register
            const data = {
                username: username,
                password: password,
            };

            try {
                const response = await postAxios("/register", data);
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        }
    };

    return (
        <Box
            sx={{
                display: "flex",
                flexWrap: "nowrap",
                flexDirection: "column",
                width: "25rem",
                padding: "4rem",
                paddingTop: "3rem",
                border: "1px solid black",
                borderRadius: "1rem",
                backgroundColor: "gray",
            }}
            id="box-register"
        >
            <h2 className="text-xl font-bold" id="h2-register">
                Register
            </h2>
            <TextField
                required
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
                                {showPassword ? (
                                    <VisibilityOff />
                                ) : (
                                    <Visibility />
                                )}
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
                                {showConfirmPassword ? (
                                    <VisibilityOff />
                                ) : (
                                    <Visibility />
                                )}
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
            />
            <Button
                variant="contained"
                onClick={handleSubmit}
                sx={{ mt: 5, ml: 1 }}
            >
                Register
            </Button>
        </Box>
    );
}

export default Register;
