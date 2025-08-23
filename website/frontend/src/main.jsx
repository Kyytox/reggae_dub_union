import React from "react";
import ReactDOM from "react-dom/client";
import { AuthProvider } from "./components/AuthContext";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { outlinedInputClasses } from "@mui/material/OutlinedInput";
import { green, yellow } from "@mui/material/colors";
import App from "./App.jsx";
import "./index.css";

const theme = createTheme({
  palette: {
    primary: {
      main: green[700],
    },
    secondary: {
      main: yellow[200],
    },
  },
  components: {
    MuiTextField: {
      styleOverrides: {
        root: {
          "--TextField-textColor": "#ffffff",
          "--TextField-brandBorderColor": "#B2BAC2",
          "--TextField-brandBorderHoverColor": "#B2BAC2",
          "--TextField-brandBorderFocusedColor": "#989898",
          "& label.Mui-focused": {
            color: "var(--TextField-brandBorderFocusedColor)",
            textColor: "white",
          },
          "& label": {
            color: "var(--TextField-brandBorderFocusedColor)",
            textColor: "white",
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        notchedOutline: {
          borderColor: "var(--TextField-brandBorderColor)",
        },
        root: {
          [`&:hover .${outlinedInputClasses.notchedOutline}`]: {
            borderColor: "var(--TextField-brandBorderHoverColor)",
          },
          [`&.Mui-focused .${outlinedInputClasses.notchedOutline}`]: {
            borderColor: "var(--TextField-brandBorderHoverColo)",
          },
          color: "var(--TextField-textColor)",
        },
      },
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  // <React.StrictMode>
  <ThemeProvider theme={theme}>
    <AuthProvider>
      <App />
    </AuthProvider>
  </ThemeProvider>,
  // </React.StrictMode>
);
