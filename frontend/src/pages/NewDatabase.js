import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload.js";
import SearchFile from "../components/SearchFile.js";
import "../styles/newdatabase.css";

const NewDataBase = ({ isOpen }) => {
    const { id } = useParams(); //getting the database ID from the URL, deconstructioning the id property from the object
    const navigate = useNavigate();
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const handleFileUpload = (file) => {
        setUploadedFiles(prevFiles => [...prevFiles, file]); 
    }

    return (
        <div className={`newDatabase-container ${isOpen ? "shifted" : ""}`}>
            {/* Navbar section */} 
            <div className="navbar">
                <button onClick={() => navigate("/database")} className="back-button">⬅ Back to Databases</button>
                <h1 className="database-title">Database {id}</h1>
            </div>
            <div className="database-content">
            {/* File upload section */}
                <FileUpload onUpload={handleFileUpload} className="file-upload-newdatabase" />

            {/* Upload Files section */}
                <div className="uploaded-files">
                    <h2>Uploaded Files</h2>
                    {uploadedFiles.length === 0 ? 
                    (<p>No Files Uploaded</p>) :
                        <ul>
                            {uploadedFiles.map((file, index) => {
                                return (
                                <li key={index}>
                                    {file.name} - {file.size} bytes
                                </li>
                                );
                            })}
                        </ul>
                    }
                </div>
            </div>
        </div>
    )

}

export default NewDataBase;