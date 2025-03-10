import React from "react";
import "../styles/database.css";
import FileUpload from "../components/FileUpload.js";
import SearchFile from "../components/SearchFile.js";

const Databases = ({ databases }) => {
    return (
        <div className="databases-container">
            <h1>Your Databases</h1>
            {databases.length == 0 ? (
                <p>No databases created yet. </p>
            ) : (
                <ul>
                    {databases.map((db, index) => (
                        <li key={index}> {db} </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Databases;