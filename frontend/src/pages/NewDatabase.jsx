import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import useFiles from "../hooks/useFiles.js";
import FileUpload from "../components/FileUpload.jsx";
import SearchFile from "../components/SearchFile.jsx";
import "../styles/newdatabase.css";

const NewDataBase = ({ isOpen }) => {
    const { id } = useParams(); //getting the database ID from the URL, deconstructioning the id property from the object
    const navigate = useNavigate();
    const location = useLocation();
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const { retrieveDb, error } = useFiles(id);
    const { focus } = location.state || {}
    
    const handleFileUpload = (file) => {
        setUploadedFiles(prevFiles => [...prevFiles, 
            { name: file.name, size : file.size}
        ]); 
    }

    useEffect(() => {
        const loadDb = async () => {
            if (!focus) return;

            const files = await retrieveDb(id);

            if (!files || !files.doc_names) {
                console.warn("Error in retrieving Db info");
                return
            }
            
            setUploadedFiles(files.doc_names.map(name => ({name, size: "Unknown"})));
            navigate(location.pathname, {replace: true, state : {} }) // clears the navigation state after first load 
        }
        loadDb()
    }, [focus, retrieveDb, navigate, location.pathname])

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