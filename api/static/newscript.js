/*
const dictionary = ['earth','plane','crane','audio','house'];
const state={
    secret: dictionary[Math.floor(Math.random()*dictionary.length)],
        grid:Array(5)
        .fill()
        .map(()=> Array(5).fill('')),
        currentRow:0,
        currentCol:0,
    };


    function scrambleWord(word){
        let chars=word.split("");
        chars.sort(()=>0.5-Math.random());
        var fword=chars.join("");
        return fword;
    }
*/


// for a given row and col and the corletter flag from api route change the box css
function checkWord(i,j,corletter){

            
            if (!((i==1 && j == 1) || (i==3 && j == 3) ||(i==1 && j == 3) || (i==3 && j == 1))) {
            var box = document.getElementById(`box${i}${j}`);
            if (!box) {
            }   

            if (corletter==1){
                box.classList.add('right');
                box.classList.remove('wrong');
                box.classList.remove("default");
            }
            else if (corletter==2){
                box.classList.add("wrong");
                box.classList.remove("right");
                box.classList.remove("default");

            }
            else{
                box.classList.add("default");
                box.classList.remove("right");
                box.classList.remove("wrong");

            }
        }
}

//alternate function to directly change css of box given the letcheck flag from api route
async function checkWordBox(boxdive,corletter){

            
    
    var box = boxdive;
    if (!box) {
    }   

    if (corletter==1){
        box.classList.add('right');
        box.classList.remove('wrong');
        box.classList.remove("default");
    }
    else if (corletter==2){
        box.classList.add("wrong");
        box.classList.remove("right");
        box.classList.remove("default");

    }
    else{
        box.classList.add("default");
        box.classList.remove("right");
        box.classList.remove("wrong");

    }
}

//fetch the scrambled letters
async function fetchletter(k, l) {
    var url = "/letters/" + (k+1).toString() + "/" + (l+1).toString();
    try {
        let response = await fetch(url);
        let data = await response.json(); 
        return data.letter; 
    } catch (error) {  
        console.error(error);
    }
}

//fetch the check flag for a particular letter and given row and col
async function checkletter(letter2,k, l) {
    var url = "/correct/"+letter2 +'/'+ (k+1).toString() + "/" + (l+1).toString();
    try {
        let response = await fetch(url); 
        let data = await response.json(); 
        return data.letter; 
    } catch (error) {
        console.error(error);
    }
}


//main grid layout constructor
async function drawGrid(container,row1,cols1){

    const grid =document.createElement("div");
    grid.className='grid'; //create class grid div
    /*console.log(sWord);
    var sArray=sWord.split("");*/
    const gridSize=5
 
    for (let i=0;i<cols1;i++){
        for (let j=0;j<row1;j++){
                var lett= await fetchletter(i,j); 
                var letflag= await checkletter(lett,i,j);
                console.log("checkword");
                console.log(letflag);
                drawBox(grid,i,j,lett,letflag);
        }
    }
    container.appendChild(grid);
    }


    //construct a box within grid
    async function drawBox(container,row,col,letter="",corletter){
        const box=document.createElement('div');
        box.className='box';
        if ((row==1 && col == 1) || (row==3 && col == 3) ||(row==1 && col == 3) || (row==3 && col == 1)) {
            box.className='box disabled';
        }  
        box.id=`box${row}${col}`;
        box.textContent=letter;
        container.appendChild(box);
        checkWordBox(box,corletter);
        box.addEventListener('click', async function() {
            // If no item is selected, select the first one
            if(swapCount===0){
                alert("You are done");
            }
            else if (!firstSelected) {
              firstSelected = this;
              rowc=row;
              colc=col;
              this.classList.add('selected'); // Highlight the first selected item
            // If an item is already selected, select the second one and swap
            console.log(firstSelected.innerHTML);
            }
            else {
              const secondSelected = this;
              this.classList.add('selected');
              // Swap the innerHTML of the two selected columns
              const temp = firstSelected.innerHTML;
              console.log(temp);
              firstSelected.innerHTML = secondSelected.innerHTML;
              secondSelected.innerHTML = temp;
        
              // Remove the selected class after swapping
              firstSelected.classList.remove('selected');
              secondSelected.classList.remove('selected');
               // Reset the next selection
              swapCount=swapCount-1; //swap counter
              var swid=document.getElementById("swapCID");
              swid.innerHTML=`Number of Swaps Left:${swapCount}`;
              var curlett=firstSelected.innerHTML;
              var corlettern = await checkletter(curlett,rowc,colc);
              console.log(curlett);
              console.log(corlettern);

              checkWord(rowc,colc,corlettern);
              var curlett=secondSelected.innerHTML;              
              var corlettern = await checkletter(curlett,row,col);
              console.log(curlett);
              console.log(corlettern);
              checkWord(row,col,corlettern);
              firstSelected = null;
            }
          });
    
        return box;
        
    }

  
/*
async function getData(k,l) {
    const url = "/letters/"+k.toString()+"/"+l.toString();
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const json = await response.json();
      return json;
    } catch (error) {
      console.error(error.message);
    }

}
'''
*/




var wordList=Array();


function startup(){
    const game=document.getElementById('game');
    var counterdiv=document.createElement("div");
    counterdiv.className='swapC';
   
    game.appendChild(counterdiv);
    counterdiv.id='swapCID';
    counterdiv.innerHTML=`Number of Swaps Left:${swapCount}`;
   
    drawGrid(game,5,5);



    }

    //initialize the game variable
    var rowc=0;
    var colc=0;
    var lettersf='';
    var swapCount=20;
    var firstSelected=null;
    startup();

