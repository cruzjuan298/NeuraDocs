import React from "react";
import ReactDom from "react-dom/client"
import './App.css'
import FileUpload from "./components/FileUpload";

function App(){
  return (
    <div>
      <h1 id="app-h1">File Upload</h1>
      <FileUpload />
    </div>
  )
}

export default App