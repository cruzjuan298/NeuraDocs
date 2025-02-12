import {useState} from "react";

const SearchFile = () => {
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
            const response = await fetch(`http://127.0.0.1:8000/query/search?query=${encodeURIComponent(query)}`, {
                method : "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({query : query}),
            })
            const data = await response.json();
            if (data.best_match) {
                setResponse(`Best Match : ${data.best_match.doc_name} (ID ${data.best_match.doc_id})`)
            } else {
                setResponse(data.error || "No match found.")
            }

        } catch (error) {
            console.log("Error trying to send query", error)
        }
    }

    return (
        <div id="search-box-div">
            <label id="search-box-label">Search for information from the file you just processed.</label>
            <input type="text" id="search-box-input" placeholder="Enter Text" onChange={handleChange}></input>
            <button onClick={handleClick}>Submit</button>
            {response && <p>{response}</p>}
        </div>
    )
}

export default SearchFile