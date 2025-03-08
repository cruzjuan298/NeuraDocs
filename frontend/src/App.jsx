import React, { useState } from "react";
import ReactDom from "react-dom/client"
import './App.css'
import FileUpload from "./components/FileUpload";
import SearchFile from "./components/SearchFile";
import Sidebar from "./components/Sidebar";

function App(){
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="app-container">
      <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />
    <div className={`main-content ${isOpen ? "shifted" : ""}`}>
      <h1 id="app-h1">File Upload</h1>
      <FileUpload />
      <SearchFile /> 
    </div>
    </div>
  )
}

export default App