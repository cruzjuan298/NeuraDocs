import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Databases from "./pages/Databases"
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import './App.css'

function App(){
  const [isOpen, setIsOpen] = useState(false);

  const [databases, setDatabases] = useState([]);
  
  // adding a new database by updating the database state to include the new one
  const addDatabase = () => { 
    const newDatabase = `Database ${databases.length + 1}`; 
    setDatabases([...databases, newDatabase]);
  }

  return (
    <Router>
      <div className="app-container">
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        <div className={`main-content ${isOpen ? "shifted" : ""}`}>
          <Routes>
            <Route path="/" element={<Home addDatabase={addDatabase} />} />
            <Route path="/database" element={<Databases databases={databases} />} />
          </Routes> 
        </div>
      </div>
    </Router>
  );

}

export default App