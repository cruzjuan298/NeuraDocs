import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Databases from "./pages/Databases.jsx"
import Sidebar from "./components/Sidebar.jsx";
import Home from "./pages/Home.jsx";
import './App.css'
import NewDataBase from "./pages/NewDatabase.jsx";
import useRetrieve from "./hooks/useRetrieve.js";
import useModify from "./hooks/useModify.js";

function App(){
  const [isOpen, setIsOpen] = useState(false);
  const { dbs, setDbs, RetrieveError, retrieveAllDbs } = useRetrieve()
  const { modifyError, deleteDb, modifyName } = useModify()
  
  if (RetrieveError || modifyError) {
    return <h1>Error occurred while trying to retrieve your dbs. Start a new session.</h1>
  }

  useEffect(() => {
    retrieveAllDbs()
  }, [retrieveAllDbs])

  // adding a new database by updating the database state to include the new one
  const createDatabase = () => { 
    const id = Date.now()
    const dbId = `db-${id}`;  // creating unique id for new databases
    setDbs([...dbs, {db_id : dbId, name: `Database ${id}`}]);
    return dbId;
  }

  const handleDeleteDb = async (dbId) => {
    const result = await deleteDb(dbId)

    if (result.success) {
      setDbs(prevDbs => 
        prevDbs.filter(db => 
          db.db_id !== dbId))
    } else {
      console.error("Failed to delete the databse")
    }
  }

  const handleEditName = async (dbId, newName) => {
    const result = await modifyName(dbId, newName)

    if (result.success) {
      setDbs(prevDbs =>
        prevDbs.map(db =>
          db.db_id === dbId ? { ... db, name: newName} : db
      ));
    } else {
      console.error(`Failed to modify the name of the db with db id ${dbId}`);
    }
  }

  return (
    <Router>
      <div className="app-container">
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        <div className={`main-content ${isOpen ? "shifted" : ""}`}>
          <Routes>
            <Route path="/" element={<Home createDatabase={createDatabase} />} />
            <Route path="/database" element={<Databases databases={dbs} handleDelete={handleDeleteDb} handleEditName={handleEditName} />}/>
            <Route path="/new-database/:id" element={<NewDataBase isOpen={isOpen} />} />
          </Routes> 
        </div>
      </div>
    </Router>
  );

}

export default App