import axios from "axios";

const baseURL = "http://localhost:5000";

export async function postAxios(route, data) {
  try {
    const response = await axios.post(`${baseURL}${route}`, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
      body: data,
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}

export async function getAxios(route) {
  try {
    const response = await axios.get(`${baseURL}${route}`, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
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
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
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
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
        Authorization: "Bearer " + sessionStorage.getItem("token"),
      },
    });

    return response.data;
  } catch (error) {
    throw error;
  }
}
