import axios from "axios";

// Ubah fungsi AllEnums menjadi asinkron
export async function AllEnums() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/utils/enum/all', {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem('token')}`
            },
        });
        return response.data; // Mengembalikan data dari response
    } catch (error) {
        console.error("Error fetching data:", error);
        return null; // Atau bisa mengembalikan default value jika perlu
    }
}


export async function getUtilsdb() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/utils/db/all',{
            headers:{
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem('token')}`
            }
        })

        return response.data
    } catch (error) {
        console.error("Error fetching data:", error);
        return null;
    }
}

export async function getWellName() {
    try {
         const response = await axios.get('http://127.0.0.1:8000/dashboard/job-well-data')

         return response.data 
         
    } catch (error) {
        console.error("Error get Data Well And Start Date", error);
        return null
    }
}
 