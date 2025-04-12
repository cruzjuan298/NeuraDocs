import { Link } from "react-router-dom"; 
import { Home, Database, X } from "lucide-react"; 
import "../styles/sidebar.css";

// takes in a state as a function argument to depict wether or not the side bar appears
const Sidebar = ({ isOpen, setIsOpen }) => {
    return (
        <div id="sidebar-div" className={isOpen ? "" : "collapsed"}>
            <button id="sidebar-button" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? <X size={20} /> : "☰"}
            </button>

            <nav id="sidebar-nav">
                <Link to="/"> 
                    <Home size={24} />
                    {isOpen && <span>Home</span>}
                </Link>
                <Link to="/database">
                    <Database size={24} />
                    {isOpen && <span>Previous Databases</span>}
                </Link>
            </nav>
        </div>
    )
}
export default Sidebar