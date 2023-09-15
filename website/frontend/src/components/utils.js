import axios from "axios";

const baseURL = "http://localhost:5000"; // Assurez-vous que l'URL correspond à votre backend

const postAxios = async (route, data) => {
    try {
        const response = await axios.post(`${baseURL}${route}`, data, {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods":
                    "GET,PUT,POST,DELETE,PATCH,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": true,
            },
        });

        return response.data;
    } catch (error) {
        throw error;
    }
};

export default postAxios;
