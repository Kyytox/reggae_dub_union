const environments = {
  development: {
    baseURL: "http://localhost:5001/api",
  },
  production: {
    baseURL: "/api",
  },
};

const currentEnv = import.meta.env.MODE || "development";
const config = environments[currentEnv];

export default config;
