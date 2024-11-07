async function send_async_request(url, method, data = null) {
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

async function get_search_suggestions() {
    const search_suggestions = await send_async_request(
        url=`https://yandex.ru/suggest/suggest-ya.cgi?srv=serp_ru_desktop&wiz=TrWth&yu=5128758181730367992&lr=10278&uil=ru&fact=1&v=4&show_experiment=222&show_experiment=224&use_verified=1&safeclick=1&skip_clickdaemon_host=1&rich_nav=1&verified_nav=1&rich_phone=1&use_favicon=1&nav_favicon=1&mt_wizard=1&history=1&nav_text=1&maybe_ads=1&icon=1&hl=1&n=10&portal=1&platform=desktop&mob=0&extend_fw=1&suggest_entity_desktop=1&entity_enrichment=1&entity_max_count=5&svg=1&part=${inputValue}&pos=2&prev-query=${previousInputValue}&hs=0&suggest_reqid=512875818173036799298141657463014`,
        method='GET',
    )    

    return search_suggestions
}