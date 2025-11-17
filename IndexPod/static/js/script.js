function spawn_thumbnail_btn(name, thumbnail_link, video_link) {
    const container = document.getElementById("thumbnail-container");
    if (!container) return;

    const thumbnailDiv = document.createElement("div");
    thumbnailDiv.className = "thumbnail";

    const title = document.createElement("h3");
    title.textContent = name.charAt(0).toUpperCase() + name.slice(1);

    const link = document.createElement("a");
    link.href = window.location.protocol + "//" + window.location.hostname + ":30076/playvideo/" + name;

    const img = document.createElement("img");
    img.src = thumbnail_link;
    img.className = "thumbnail-image";
    
    link.appendChild(img);  
    thumbnailDiv.appendChild(title);
    thumbnailDiv.appendChild(link);
    container.appendChild(thumbnailDiv)
}

function request_videolist(word) {
    const url = "/search/" + encodeURIComponent(word)
    const container = document.getElementById("thumbnail-container");
    if (container) container.innerHTML = "";
    fetch(url, {
        method: "GET",
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            const row = data[i];
            spawn_thumbnail_btn(row.name, row.thumbnail_link, row.video_link);
        }
    })
    .catch(error => {
        console.error("Request failed:", error);
    });
}

const button = document.getElementById("searchButton");
const input = document.getElementById("searchInput");

function on_searchButton_click() {
    request_videolist(input.value)
}

button.addEventListener("click", on_searchButton_click)

// Below is for video player template

function createVideoPlayer(titleText, videoUrl) {
    const heading = document.createElement('h1');
    heading.textContent = titleText;

    const video = document.createElement('video');
    video.width = 640;
    video.height = 360;
    video.controls = true;

    const source = document.createElement('source');
    source.src = videoUrl;
    source.type = 'video/mp4';
    video.appendChild(source);

    document.body.appendChild(heading);
    document.body.appendChild(video);
}