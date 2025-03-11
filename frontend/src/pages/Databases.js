import React from "react";
import { Link } from "react-router-dom";
import "../styles/database.css";

const Databases = ({ databases }) => {
    return (
        <div className="databases-container">
            <h1>Your Databases</h1>
            {databases.length == 0 ? (
                <p>No databases created yet. </p>
            ) : (
                <ul>
                    {databases.map((db) => (
                        <li key={db.id}> 
                            <Link to={`/new-database/${db.id}`}>{db.name}</Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Databases;