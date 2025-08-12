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
        retrieveDbs: "/retrieve/retrieveDatabase/all"
    },
    apiVersion: "v0.1",
}