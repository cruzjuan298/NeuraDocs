import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import FileUpload from "./components/FileUpload";
import SearchFile from "./components/SearchFile";
import Sidebar from "./components/Sidebar";
import Home from "./pages/home";
import './App.css'

function App(){
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Router>
      <div className="app-container">
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        <div className={`main-content ${isOpen ? "shifted" : ""}`}>
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes> 
        </div>
      </div>
    </Router>
  );

}

export default App