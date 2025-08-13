import { useState } from "react";
import { Link } from "react-router-dom";
import useModify from "../hooks/useModify";
import "../styles/database.css";

const Databases = ({ databases, handleDelete, handleEditName }) => {
    const [editingId, setEditingId] = useState(null);
    const [editName, setEditName] = useState(null);
    const [newName, setNewName] = useState("");

    const handleEdit = (db) => {
        setEditingId(db.db_id);
        setEditName(db.name)
    };
    
    const handleCancel = () => {
        setEditName(null);
        setEditingId(null);
    }

    const handleSave = async (dbId, newName) => {
        await handleEditName(dbId, newName);
        handleCancel();
    }


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
                                        placeholder={editName}
                                        onChange={(e) => setNewName(e.target.value)}
                                        className="edit-input"
                                    />
                                    <button onClick={() => handleSave(db.db_id, newName)} className="modify-button" id="save-button">
                                        Save
                                    </button>
                                    <button onClick={handleCancel} className="modify-button" id="cancel-button">
                                        Cancel
                                    </button>
                                    <button onClick={() => handleDelete(db.db_id)} className="modify-button" id="delete-button">
                                        Delete
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