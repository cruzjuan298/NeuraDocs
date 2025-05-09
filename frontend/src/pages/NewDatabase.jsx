import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload.jsx";
import SearchFile from "../components/SearchFile.jsx";
import "../styles/newdatabase.css";

const NewDataBase = ({ isOpen }) => {
    const { id } = useParams(); //getting the database ID from the URL, deconstructioning the id property from the object
    const navigate = useNavigate();
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const handleFileUpload = (file) => {
        setUploadedFiles(prevFiles => [...prevFiles, 
            { name: file.name, size : file.size}
        ]); 
    }

    useEffect(() => {
        retrieveDatabases();
    }, [id])

    const retrieveDatabases = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/retrieve/retrieveDatabase?db_id=${id}`, {
                method: "GET"
            })

            const data = await response.json()
            
            if (data !== null){
                console.log("retrieve Data: ", data);
                setUploadedFiles(data.doc_names.map(name => ({name, size: "Unknown"})));
                console.log(uploadedFiles)
            } 
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className={`newDatabase-container ${isOpen ? "shifted" : ""}`}>
            {/* Navbar section */} 
            <div className="navbar">
                <button onClick={() => navigate("/database")} className="back-button">⬅ Back to Databases</button>
                <h1 className="database-title">Database {id}</h1>
            </div>
            <div className="database-content">
            {/* Search file uplaod  */}
                <SearchFile db_id={id}/>
            {/* File upload section */}
                <FileUpload onUpload={handleFileUpload} dbId={id} className="file-upload-newdatabase" />

            {/* Upload Files section */}
                <div className="uploaded-files">
                    <h2>Uploaded Files</h2>
                    {uploadedFiles.length === 0 ? 
                    (<p>No Files Uploaded</p>) :
                        <ul>
                            {uploadedFiles.map((file, index) => {
                                return (
                                <li key={index}>
                                    {file.name} - {file.size}
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