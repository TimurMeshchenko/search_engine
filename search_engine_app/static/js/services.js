async function enable_input_suggestions() {
    const search_input = document.querySelector('.search-input');
    const search_input_div = document.querySelector('.search-input-div');
    const search_suggestions = document.querySelector('.search-suggestions');
    const popup_overlay = document.querySelector('.popup-overlay');

    search_input.addEventListener('input', add_search_suggestions) 
    
    search_input.addEventListener('focus', () => {
        if (search_suggestions.childElementCount > 0) {
            search_input_div.classList.add('search-input-focused');
            search_suggestions.style.display = 'flex';
            
            if (popup_overlay) {
                popup_overlay.style.display = 'flex';
            }
        }
    });
    
    search_input.addEventListener('blur', () => {
        search_input_div.classList.remove('search-input-focused');
        search_suggestions.style.display = 'none';
        
        if (popup_overlay) {
            popup_overlay.style.display = 'none';
        }        
    });    

    search_input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const input_value = event.target.value;  
            const input_value_joined = input_value.split(' ').join('+');

            window.location.href = `${base_url}/search/?text=${input_value_joined}`;;
        }
    });    
}

async function add_search_suggestions(event) {
    const input_value = event.target.value;
    
    if (!previous_input_value) {
        previous_input_value = input_value
    }

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
    const search_suggestions = document.querySelector('.search-suggestions');
    search_suggestions.innerHTML = '';
    
    if (
        !response_search_suggestions || 
        response_search_suggestions.length < 1 ||
        !Array.isArray(response_search_suggestions[1])
    ) {
        return null
    }

    response_search_suggestions[1].forEach(search_suggestion_array => {
        const search_suggestion = search_suggestion_array[1];
        const search_suggestion_joined = search_suggestion.split(' ').join('+');
        const suggestion_link = document.createElement('a');
    
        suggestion_link.classList.add('search-suggestion');
        suggestion_link.href = `${base_url}/search/?text=${search_suggestion_joined}`;
        suggestion_link.textContent = search_suggestion;
        search_suggestions.appendChild(suggestion_link);
    });

    const search_input_div = document.querySelector('.search-input-div');
    const popup_overlay = document.querySelector('.popup-overlay');

    if (popup_overlay) {
        popup_overlay.style.display = 'flex';
    }
    
    search_suggestions.style.display = 'flex';
    search_input_div.classList.add('search-input-focused');
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
