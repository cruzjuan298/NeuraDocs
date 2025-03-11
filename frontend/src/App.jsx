import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Databases from "./pages/Databases"
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import './App.css'
import NewDataBase from "./pages/NewDatabase";

function App(){
  const [isOpen, setIsOpen] = useState(false);

  const [databases, setDatabases] = useState([]);
  
  // adding a new database by updating the database state to include the new one
  const createDatabase = () => { 
    const newId = `db-${Date.now()}`;  // creating unique id for new databases
    setDatabases([...databases, {id : newId, name: `Database ${databases.length + 1}`}]);
    return newId;
  }

  return (
    <Router>
      <div className="app-container">
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        <div className={`main-content ${isOpen ? "shifted" : ""}`}>
          <Routes>
            <Route path="/" element={<Home createDatabase={createDatabase} />} />
            <Route path="/database" element={<Databases databases={databases} />} />
            <Route path="/new-database/:id" element={<NewDataBase />} />
          </Routes> 
        </div>
      </div>
    </Router>
  );

}

export default App