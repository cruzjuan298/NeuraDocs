import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { Database } from "lucide-react";
import "../styles/home.css"

const Home = ({ createDatabase }) => {
    const navigate = useNavigate();

    const handleCreateDatabase = () => {
        const newDatabaseId = createDatabase();
        insertDb(newDatabaseId.toString());
        navigate(`/new-database/${newDatabaseId}`);
    }

    const insertDb = async (db_id) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/create/createDB", {
                method : "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    dbId: db_id,
                    db_name: `Database ${db_id.split('-')[1]}`
                })
            })

            const data = await response.json()

            if (data === null ){
                console.log("Error inserting DB")
            }
            console.log("insertDB data: " ,data)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className="home-container">
            <h1>Welcome to NeuraDocs</h1>
            <p>Create databases for your documents and manage them with ease.</p>
            
            <div className="home-actions">
                <h3>Get Started: </h3>
                <button className="create-db-button" onClick={handleCreateDatabase} >
                    <Database size={24} />
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