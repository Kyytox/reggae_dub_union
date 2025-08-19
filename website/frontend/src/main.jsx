import React from "react";
import ReactDOM from "react-dom/client";
import { AuthProvider } from "./components/AuthContext";
import { ThemeProvider, createTheme } from "@mui/material/styles";
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
