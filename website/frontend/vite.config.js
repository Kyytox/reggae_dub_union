import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // allowedHosts: ["www.reggaedubunion.fr", "reggaedubunion.fr"],
    host: "0.0.0.0",
    port: ["5173:80"],
  },
});
