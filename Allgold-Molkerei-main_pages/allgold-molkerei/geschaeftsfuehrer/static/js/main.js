/**
 * 
 */

function createVerkaufsstelle(){
	
	var liste = document.getElementById("liste");
	
	var card = document.createElement("div");
	card.setAttribute("class", "card");
	
	var name = document.createElement("b");
	name.textContent = "Name:";
	card.appendChild(name);
	
	var br = document.createElement("br");
	card.appendChild(br);
	
	var id = document.createElement("b");
	id.textContent = "ID:";
	card.appendChild(id);
	
	var br2 = document.createElement("br");
	card.appendChild(br2);
	
	var button = document.createElement("button");
	button.setAttribute("class", "card-button");
	button.textContent = "Uebersicht";
	card.appendChild(button);
	
	var button2 = document.createElement("button");
	button2.setAttribute("class", "card-button");
	button2.textContent = "Verkaufszahlen";
	card.appendChild(button2);
	
	
	liste.appendChild(card);
}

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