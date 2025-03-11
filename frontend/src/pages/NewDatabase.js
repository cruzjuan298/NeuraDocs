import React from "react";
import { useParams } from "react-router-dom";
import FileUpload from "../components/FileUpload.js";
import SearchFile from "../components/SearchFile.js";
import "../styles/newdatabase.css";

const NewDataBase = () => {
    const { id } = useParams(); //getting the database ID from the URL, deconstructioning the id property from the object

    return (
        <div className="newDatabase-container">
            <h1>Database {id}</h1>
            <FileUpload />
            <SearchFile />
        </div>
    )

}

export default NewDataBase;