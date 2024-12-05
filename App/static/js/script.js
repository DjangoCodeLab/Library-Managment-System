document.addEventListener('DOMContentLoaded',()=>{
    const searchInputs = document.querySelectorAll('.search-input');
    const resultsContainer = document.getElementById('book-results');
    let debounceTimer;
    searchInputs.forEach(input=>{
        input.addEventListener('input',()=>{
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                performSearch();
            }, 200);

        })
    })

    const performSearch = ()=>{
        const formData = new FormData(document.getElementById('search-form'));
        const searchParams = new URLSearchParams(formData).toString();
        fetch(`?${searchParams}`)
        .then(response =>response.text())
        .then(data=>{
            const parser = new DOMParser();
            const doc = parser.parseFromString(data,'text/html');
            const newResults = doc.querySelector('#book-results').innerHTML;
            resultsContainer.innerHTML = newResults;
        })
    }
})


