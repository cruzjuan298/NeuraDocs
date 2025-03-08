
import { Home, Database, X } from "lucide-react"; 
import "../styles/sidebar.css";

const Sidebar = ({ isOpen, setIsOpen }) => {
    return (
        <div id="sidebar-div" className={isOpen ? "" : "collapsed"}>
            <button id="sidebar-button" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? <X size={20} /> : "☰"}
            </button>

            <nav id="sidebar-nav">
                <a id="sidebar-a" href="/"> 
                    <Home size={24} />
                    {isOpen && <span>Home</span>}
                </a>
                <a href="/databases">
                    <Database size={24} />
                    {isOpen && <span>Previous Databases</span>}
                </a>
            </nav>
        </div>
    )
}
export default Sidebar