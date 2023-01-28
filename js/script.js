window.onload = () => {
// get lightbox and all zoomT images
let all = document.getElementsByClassName("zoomT"),
lightbox = document.getElementById("lightbox");
// show image in lightbox
if (all.length>0) { for (let i of all) {
i.onclick = () => {
let clone = i.cloneNode();
clone.className = "";
lightbox.innerHTML = "";
lightbox.appendChild(clone);
lightbox.className = "show";
};
}}
// close lightbox
lightbox.onclick = () => lightbox.className = "";
};