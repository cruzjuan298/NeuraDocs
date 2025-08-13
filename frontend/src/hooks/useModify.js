import config from "../config";
import { useState,useCallback } from "react";

export default function useModify(){
    const [error, setError] = useState(null)
    
    const apiUrl = `${config.api.baseUrl}`

    const deleteDb = useCallback( async (dbId) => {
        try {
            const endpointPath = config.api.endpoints.deleteDb(dbId);
            const response = await fetch(`${apiUrl}${endpointPath}`, {
                method: "DELETE",
                headers : config.api.headers
            })
            
            if (!response.ok) {
                const errorData = await response.json();
                setError(errorData.nessage)
                throw new Error(`Http error. Status: ${response.status}`);
            }

            const data = await response.json()

            if (!data.success){
                console.error("Error in trying to delete db: ", data.message)
                return {"success" : false}
            }            
            return {"success" : true}

        } catch (error) {
            setError(error)
            console.error(error)
            return {"success" : false}
        }

    }, [apiUrl])

    const modifyName = useCallback( async (dbId, newName) => {
        try {
            const endpointPath = config.api.endpoints.modifyName(dbId, newName);

            const response = await fetch(`${apiUrl}${endpointPath}`, {
                method: "PATCH",
                headers : config.api.headers
            });
            
            if (!response.ok){
                errorData = await response.json()
                setError(errorData.message)
                console.error(`Http error occured while trying to modfify the db name: ${response.status}`)

            }

            const data = await response.json();

            if (!data.success) {
                console.error("Error updating database name:", data.message);
                return {"success" : false};
            }

            return {"success" : true}
        } catch (error) {
            console.error("Error updating database name:", error);
            setError(error)
            return {"success" : false}
        }
    }, []);

    return {error, deleteDb, modifyName}
}