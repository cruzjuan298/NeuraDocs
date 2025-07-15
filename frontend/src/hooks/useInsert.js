import { useCallback, useState } from "react"
import { API_CONFIG } from "../config/api"

export default function useInsert() {
   const [error, setError] = useState(null);
    const apiUrl = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.createDb}`

    const insertDb = useCallback(async (dbIdToInsert) => {
        if (!apiUrl) {
            console.warn("Error in trying to insert a db with a invalid DbId format");
            return;
        }

        setError(null);

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers : API_CONFIG.headers,
                body: JSON.stringify({
                    dbId : dbIdToInsert,
                    dbName: `Database ${dbIdToInsert.split('-')[1]}`
                })
            })

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Http error. Status: ${response.status}`);
            }

            const data = await response.json()

            if (data === null) {
                console.error("Error in inserting DB");
            }
            console.log("Inserted data: ", data)
        } catch (error){
            setError(error)
            console.error(error)
        }
    }, [apiUrl])

    return {insertDb, error}
}