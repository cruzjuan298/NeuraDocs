import { useState } from "react";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

const handleFileChange = (event) => {
    setFile(event.target.files[0])
}

const handleUpload = async () => {
    if (!file) {
        alert("Please select a file first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);


    try {
        const response = await fetch("http://127.0.0.1:8000/files/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        setMessage(data.message || "Upload successful!");

    } catch (error) {
        console.log("Erorr while uploading", error);
        setMessage("Failed to upload file.")
    }
  }
  return (
    <div>
        <h2>Upload a File</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
        {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload