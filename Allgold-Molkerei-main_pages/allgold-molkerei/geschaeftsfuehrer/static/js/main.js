

function toggleBurgerMenu(){
	var links = document.getElementById("burger-menu");
	if(links.style.display === "inline"){
		links.style.display = "none";
	}
	else{
		links.style.display = "inline"
	}
}

function search(){
    var input = document.getElementById("search");
    var cards = document.getElementsByClassName("card");
    var name = document.getElementById("name");
    name.style.display="none";
    if(input == ""){
        cards.style.display = "inline-block";
         name.style.display="none";
    }
    for(let i = 0; i<cards.length; i++){
        let name = cards[i].getElementById("name").innertText;
        if(name != input){
            name.style.display="none";
            card[i].style.display = "none";
        }
    }
}

function createChart(canvasID){

}