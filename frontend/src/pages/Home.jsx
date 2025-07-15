import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Database } from "lucide-react";
import "../styles/home.css"
import useInsert from "../hooks/useInsert.js";

const Home = ({ createDatabase }) => {
    const { insertDb, error } = useInsert()
    const navigate = useNavigate();

    const handleCreateDatabase = () => {
        const newDatabaseId = createDatabase();
        insertDb(newDatabaseId.toString());
        navigate(`/new-database/${newDatabaseId}`);
    }


    return (
        <div className="home-container">
            <h1>RAG based documentation system</h1>
            <p>Create databases for your documents and manage them with ease.</p>
            
            <div className="home-actions">
                <h3>Get Started: </h3>
                <button className="create-db-button" onClick={handleCreateDatabase} >
                    <Database className="db-icon" size={24} />
                    Create New Database
                </button>
                <Link to="/database" className="view-db-button" >
                    View Databases
                </Link>
            </div>
        </div>
    );
};

export default Home;