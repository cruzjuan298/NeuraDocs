import { useState, useCallback, useMemo} from "react"
import { API_CONFIG } from "../config/api"

export default function useFiles(dbIdParam) {
    const [error, setError] = useState(null);

    const apiUrl = useMemo(() => {
        if (!dbIdParam) {
            return null;
        }
        return `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.retrieve}${dbIdParam}`;
    }, [dbIdParam])

    const retrieveDb = useCallback(async () => {
        if (!apiUrl) {
            console.warn("Error while trying to retrieve with an invalid URL type");
            return;
        }

        setError(null);

        try {
            const response = await fetch(apiUrl, {
                method: "GET",
                headers: API_CONFIG.headers
            })

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Http error. Status: ${response.status}`)
            }

            const data = await response.json()
            
            if (data !== null){
                console.log("retrieve Data: ", data);
                return data
            } 
            return null
        } catch (error) {
            setError(error)
            console.log(error);
        }
    }, [apiUrl] )

    return { retrieveDb, error }
}