import {useState} from "react";
import "../styles/searchfile.css"

const SearchFile = ({ db_id }) => {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState("")
    const handleChange = (event) => {
        setQuery(event.target.value);
    }

    const handleClick =  async () => {
        if (!query) {
            alert("Please type something in");
            return;
        }
        try {
            const response = await fetch("http://127.0.0.1:8000/query/search", {
                method : "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    query : query, 
                    db_id : db_id
                }),
            })
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error("Server error:", errorText);
                alert("Server error, check console for details.");
                return;
            }

            const data = await response.json();
            console.log("Search response:", data); // Debug log

            if (data.error) {
                setResponse(`Error: ${data.error}`);
            } else if (data.best_match) {
                setResponse(`Best Match: ${data.best_match.best_match_doc_name} (ID ${data.document_match.doc_id}). Response: ${data.best_match.best_match_sentence}`);
            } else {
                setResponse("No match found.");
            }

        } catch (error) {
            console.error("Error trying to send query:", error);
            setResponse("Error occurred while searching. Please try again.");
        }
    }

    return (
        <div id="search-box-div">
            <label id="search-box-label">Search for information from your files</label>
            <div className="input-button-div">
                <input type="text" id="search-box-input" placeholder="Enter Text" onChange={handleChange}></input>
                <button onClick={handleClick}>Submit</button>
                {response && <p>{response}</p>}
            </div>
        </div>
    )
}

export default SearchFile