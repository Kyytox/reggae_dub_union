import axios from "axios";
import config from "../config";

const baseURL = config.baseURL;

export async function postAxios(route, data) {
  try {
    const response = await axios.post(`${baseURL}${route}`, {
      headers: {
        "Content-Type": "application/json",
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
        Authorization: "Bearer " + sessionStorage.getItem("token"),
      },
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}
