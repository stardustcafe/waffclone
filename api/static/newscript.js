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
        console.log(fword);
        return fword;
    }

    
async function checkWord(){
        for (let j=0;j<5;j++){
        for (let i=0;i<5;i++){
            
            if (!((i==1 && j == 1) || (i==3 && j == 3) ||(i==1 && j == 3) || (i==3 && j == 1))) {
            var box = document.getElementById(`box${i}${j}`);
            if (!box) {
                console.error(`No element found for box${i}${j}`);
                continue; // Skip this iteration if the box is null
            }   
            var letter1 = box.textContent;
            var corletter= await checkletter(letter1,i,j);
            console.log(letter1);
            console.log(corletter);
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
            console.log("found the right") 
        }
        }
    }

    }
async function drawBox(container,row,col,letter=""){
    const box=document.createElement('div');
    box.className='box';
    if ((row==1 && col == 1) || (row==3 && col == 3) ||(row==1 && col == 3) || (row==3 && col == 1)) {
        box.className='box disabled';
    }  
    box.id=`box${row}${col}`;
    box.textContent=letter;
    container.appendChild(box);
    
    box.addEventListener('click', function() {
        // If no item is selected, select the first one
        if(swapCount===0){
            alert("You are done");
        }
        else if (!firstSelected) {
          firstSelected = this;
          this.classList.add('selected'); // Highlight the first selected item
        // If an item is already selected, select the second one and swap
        console.log(firstSelected.innerHTML);
        checkWord();
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
          firstSelected = null; // Reset for the next selection
          swapCount=swapCount-1;
          var swid=document.getElementById("swapCID");
          swid.innerHTML=`Number of Swaps Left:${swapCount}`;
        }
        checkWord();     
      });

    return box;
    
}
async function fetchletter(k, l) {
    var url = "/letters/" + (k+1).toString() + "/" + (l+1).toString();
    try {
        let response = await fetch(url); // Await the fetch
        let data = await response.json(); // Await the JSON conversion
        return data.letter; // Assuming the response has a 'letter' field
    } catch (error) {
        console.error(error);
    }
}


async function checkletter(letter2,k, l) {
    var url = "/correct/"+letter2 +'/'+ (k+1).toString() + "/" + (l+1).toString();
    try {
        let response = await fetch(url); // Await the fetch
        let data = await response.json(); // Await the JSON conversion
        return data.letter; // Assuming the response has a 'letter' field
    } catch (error) {
        console.error(error);
    }
}



async function drawGrid(container,row1,cols1){

    const grid =document.createElement("div");
    grid.className='grid';
    /*console.log(sWord);
    var sArray=sWord.split("");*/
    for (let i=0;i<cols1;i++){
        for (let j=0;j<row1;j++){


                var lett= await fetchletter(i,j);
                drawBox(grid,i,j,lett);                
        }
    }
    container.appendChild(grid);
    checkWord();
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


function validCrossword(words) {
  const grid = Array.from({ length: 5 }, () => Array(5).fill(''));

  // Fill across words in rows 1, 3, and 5
  grid[0] = words[0].split('');
  grid[2] = words[1].split('');
  grid[4] = words[2].split('');

  // Fill down words in columns 1, 3, and 5
  for (let i = 0; i < 5; i++) {
      grid[i][0] = words[3][i];
      grid[i][2] = words[4][i];
      grid[i][4] = words[5][i];
  }

  // Ensure that the black squares at (2,2), (2,4), (4,2), and (4,4) stay valid
  if (!grid[1][1] && !grid[1][3] && !grid[3][1] && !grid[3][3]) {
      return true;
  }
  return false;
}


var wordList=Array();


function startup(){
    const game=document.getElementById('game');
    var counterdiv=document.createElement("div");
    counterdiv.className='swapC';
   
    game.appendChild(counterdiv);
    counterdiv.id='swapCID';
    counterdiv.innerHTML=`Number of Swaps Left:${swapCount}`;
    console.log(state.secret);
    const sWord=scrambleWord(state.secret);

    drawGrid(game,5,5);



    }
    var lettersf='';
    var swapCount=20;
    var firstSelected=null;
    console.log(fetchletter(1,1));
    startup();

