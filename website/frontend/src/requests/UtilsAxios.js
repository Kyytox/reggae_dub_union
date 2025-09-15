import axios from "axios";

// const baseURL = "http://localhost:5001";
const baseURL = "/api";

export async function postAxios(route, data) {
  try {
    const response = await axios.post(`${baseURL}${route}`, {
      headers: {
        "Content-Type": "application/json",
        // "Access-Control-Allow-Origin": "*",
        // "Access-Control-Allow-Credentials": true,
      },
      body: data,
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}

export async function getAxios(route, data = {}) {
  try {
    const response = await axios.get(`${baseURL}${route}`, {
      headers: {
        "Content-Type": "application/json",
        // "Access-Control-Allow-Origin": "*",
        // "Access-Control-Allow-Credentials": true,
      },
      params: data,
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}

export async function postAxiosAuth(route, data) {
  try {
    const response = await axios.post(
      `${baseURL}${route}`,
      data, // body
      {
        headers: {
          "Content-Type": "application/json",
          // "Access-Control-Allow-Origin": "*",
          // "Access-Control-Allow-Credentials": true,
          Authorization: "Bearer " + sessionStorage.getItem("token"),
        },
      },
    );
    return response.data;
  } catch (error) {
    throw error;
  }
}

export async function getAxiosAuth(route, id) {
  try {
    const response = await axios.get(`${baseURL}${route}/${id}`, {
      headers: {
        "Content-Type": "application/json",
        // "Access-Control-Allow-Origin": "*",
        // "Access-Control-Allow-Credentials": true,
        Authorization: "Bearer " + sessionStorage.getItem("token"),
      },
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}
