import React from "react";
import ReactDom from "react-dom/client"
import './App.css'
import FileUpload from "./components/FileUpload";
import SearchFile from "./components/SearchFile";
import Sidebar from "./components/Sidebar";

function App(){
  return (
    <div class="flex">
      <Sidebar />
      <h1 id="app-h1">File Upload</h1>
      <FileUpload />
      <SearchFile /> 
    </div>
  )
}

export default App