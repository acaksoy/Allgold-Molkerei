/**
 * 
 */
 function toggleBurgerMenu(){
    var links = document.getElementById("burger-menu");
    if(links.style.display === "inline"){
        links.style.display = "none";
    }
    else{
        links.style.display = "inline"
    }
}