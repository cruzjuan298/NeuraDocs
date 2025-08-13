export const API_CONFIG ={
    baseUrl: import.meta.env.VITE_PUBLIC_BASE_URL,
    timeout: 15000, // in ms
    headers: {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
    },
    endpoints : {
        upload : "/files/upload",
        retrieve: "/retrieve/retrieveDatabase?db_id=",
        createDb: "/create/createDB",
        retrieveDbs: "/retrieve/retrieveDatabase/all",
        deleteDb : (dbId) => `/delete/removeDb?db_id=${dbId}`,
        modifyName: (dbId, newName) => `/modify/update-db-name?db_id=${dbId}&new_name=${newName}`
    },
    apiVersion: "v0.1",
}