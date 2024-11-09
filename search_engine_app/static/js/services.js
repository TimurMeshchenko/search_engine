async function enable_input_suggestions() {
    const search_input = document.querySelector('.search-input');

    search_input.addEventListener('input', add_search_suggestions)    
}

async function add_search_suggestions(event) {
    const input_value = event.target.value
    
    if (!previous_input_value) {
        previous_input_value = input_value
    }

    const base_url = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
    const data = {
        'input_value': input_value,
        'previous_input_value': previous_input_value,
    }            
    previous_input_value = input_value
    const response_search_suggestions = await send_async_request(
        `${base_url}/api/get_search_suggestions/`,
        'POST',
        data
    )
    console.log(response_search_suggestions) // DELETE

    const suggestions_container = document.querySelector('.search-suggestions');
    suggestions_container.innerHTML = '';
    
    if (
        !response_search_suggestions || 
        response_search_suggestions.length < 1 ||
        !Array.isArray(response_search_suggestions[1])
    ) {
        return null
    }

    response_search_suggestions[1].forEach(search_suggestion_array => {
        const search_suggestion = search_suggestion_array[1];
        const suggestion_link = document.createElement('a');
        suggestion_link.classList.add('search-suggestion');
        suggestion_link.href = `${base_url}/search/${search_suggestion}/`;
        suggestion_link.textContent = search_suggestion;
        suggestions_container.appendChild(suggestion_link);
    });
}

async function send_async_request(url, method, data=null) {
    try {
        const headers = {
            "Content-Type": "application/json",
        }
        const request_data = {
            method: method,
            headers: headers,
        }

        if (data) {
            request_data['body'] = JSON.stringify(data)
        }

        const response = await fetch(url, request_data);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error posting data:", error);
    }
}
