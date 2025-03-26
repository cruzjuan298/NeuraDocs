import { useState } from "react";
import "../styles/fileupload.css";

const FileUpload = ({ onUpload, dbId }) => {
    const [file, setFile] = useState(null); // used for sending parcel/checking if there is a file uploaded
    const [message, setMessage] = useState(""); // used to fetch the message from the api request

const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
}

const handleUpload = async () => {
    if (!file) {
        alert("Please select a file first!");
        return;
    }

    if (!dbId) {
        alert("Database ID is missing!");
        return 
    }
    const formData = new FormData();
    formData.append("file", file);
    formData.append("db_id", dbId);
    
    try {
        const response = await fetch("http://127.0.0.1:8000/files/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        setMessage(data.message || "Upload successful!");

        if (onUpload) {
            onUpload(file);
        }

    } catch (error) {
        console.log("Erorr while uploading", error);
        setMessage("Failed to upload file.")
    }
  }
  return (
    <div id="file-upload-div">
        <h2>Upload a File</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
        {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload