async function fetchPage(url) {
    let headers = new Headers()
    headers.append("X-Requested-With", "XMLHttpRequest")
    return fetch(url, {headers})
}

console.log(window.location.pathname)

document.addEventListener("DOMContentLoaded", () => {
    let footer = document.querySelector("footer");
    let scroller = document.querySelector("main ul")
    
    let get_query = new URLSearchParams(window.location.search)
    let counter = 2;

    let observer = new IntersectionObserver( async (entries) => {
        entry = entries[0]
        if (entry.intersectionRatio > 0) {
            let url = `${window.location.pathname}?page=${counter}`;
            let req = await fetchPage(url);
            if (req.ok) {
                const body = await req.text();
                if (body == '')
                    observer.disconnect();
                scroller.innerHTML += body;
                ++counter;
            } else {
                observer.disconnect();
            }
        }
    });
    
    observer.observe(footer);
});
