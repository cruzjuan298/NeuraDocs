import { useState, useCallback } from "react";
import config from "../config";

export default function useRetrieve() {
    const [dbs, setDbs] = useState([])
    const [error, setError] = useState(null)
    const apiUrl = `${config.api.baseUrl}${config.api.endpoints.retrieveDbs}`

    const retrieveAllDbs = useCallback(async () => {
        setError(null)

        try{
            const response = await fetch(apiUrl, {
                method: "GET",
                headers : config.api.headers,
            })

            if (!response.ok) {
                const errorData = await response.json();
                setError(errorData)
                throw new Error(`Http error. Status: ${response.status}`)
            }  

            const data = await response.json()

            if (data.success && data.dbs){
                console.log(data)
                setDbs(data.dbs)
            } else {
                console.log("API call was not successful or data is missing")
                setDbs([])
            }

        } catch (error){
            console.error("An error occured while retrieveAllDbs: ", error)
            setError(error)
            setDbs([])
        }

    }, [apiUrl])
    return {dbs, setDbs, error, retrieveAllDbs}
}