import { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/database.css";

const Databases = ({ databases }) => {
    const [editingId, setEditingId] = useState(null);
    const [newName, setNewName] = useState("");
    
    const handleEdit = (db) => {
        setEditingId(db.db_id);
        setNewName(db.name);
    };

    const handleSave = async (dbId) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/modify/update-db-name?db_id=${dbId}&new_name=${encodeURIComponent(newName)}`, {
                method: "PATCH"
            });
            
            const data = await response.json();
            if (data.error) {
                console.error("Error updating database name:", data.error);
                return;
            }
            
            // Update the local state
            const updatedDatabases = databases.map(db => 
                db.id === dbId ? { ...db, name: newName } : db
            );
            // You'll need to pass this back to the parent component to update the state
            // For now, we'll just refresh the page
            window.location.reload();
        } catch (error) {
            console.error("Error updating database name:", error);
        }
        setEditingId(null);
    };

    return (
        <div className="databases-container">
            <h1>Your Databases</h1>
            {databases.length === 0 ? (
                <p>No databases created yet. </p>
            ) : (
                <ul className="database-list">
                    {databases.map((db) => (
                        <li key={db.db_id} className="database-item">
                            {editingId === db.db_id ? (
                                // edit db name here
                                <div className="edit-container">
                                    <input
                                        type="text"
                                        value={newName}
                                        onChange={(e) => setNewName(e.target.value)}
                                        className="edit-input"
                                    />
                                    <button onClick={() => handleSave(db.id)} className="save-button">
                                        Save
                                    </button>
                                    <button onClick={() => setEditingId(null)} className="cancel-button">
                                        Cancel
                                    </button>
                                </div>
                            ) : (
                                <div className="database-link-container">
                                    <Link to={`/new-database/${db.db_id}`} state={{ focus : true}} className="database-link">
                                        {db.name}
                                    </Link>
                                    <button onClick={() => handleEdit(db)} className="edit-button">
                                        Edit
                                    </button>
                                </div>
                            )}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Databases;