

let gameBoard = [];
let aiArray = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'];
let x = 0;
let V = 8;

function xGame() {
    gameBoard = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'];
    let mainDisplay = document.getElementById('displayNone');
    let buttonDisplay = document.getElementById('buttonDisplay');
    buttonDisplay.style.display = 'none';
    mainDisplay.style.display = 'inherit';
}
function oGame() {
    gameBoard = ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'];
    let mainDisplay = document.getElementById('displayNone');
    let buttonDisplay = document.getElementById('buttonDisplay');
    buttonDisplay.style.display = 'none';
    mainDisplay.style.display = 'inherit';
}
function twoPlayer() {
    gameBoard = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'];
    let mainDisplay = document.getElementById('displayNone2');
    let buttonDisplay = document.getElementById('buttonDisplay');
    buttonDisplay.style.display = 'none';
    mainDisplay.style.display = 'inherit';
}

function Render(ID) {
    if (ID == 'A1') {
        const A1 = document.getElementById('A1');
        if (gameBoard[x] == 'X') {
            A1.style.color = 'Red';
        } else {
            A1.style.color = 'Blue';
        }
        A1.innerHTML = gameBoard[x];
        A1.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('A1'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'A2') {
        const A2 = document.getElementById('A2');
        if (gameBoard[x] == 'X') {
            A2.style.color = 'Red';
        } else {
            A2.style.color = 'Blue';
        }
        A2.innerHTML = gameBoard[x];
        A2.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('A2'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'A3') {
        const A3 = document.getElementById('A3');
        if (gameBoard[x] == 'X') {
            A3.style.color = 'Red';
        } else {
            A3.style.color = 'Blue';
        }
        A3.innerHTML = gameBoard[x];
        A3.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('A3'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'B1') {
        const B1 = document.getElementById('B1');
        if (gameBoard[x] == 'X') {
            B1.style.color = 'Red';
        } else {
            B1.style.color = 'Blue';
        }
        B1.innerHTML = gameBoard[x];
        B1.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('B1'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'B2') {
        const B2 = document.getElementById('B2');
        if (gameBoard[x] == 'X') {
            B2.style.color = 'Red';
        } else {
            B2.style.color = 'Blue';
        }
        B2.innerHTML = gameBoard[x];
        B2.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('B2'), 1);
        console.log(aiArray);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'B3') {
        const B3 = document.getElementById('B3');
        if (gameBoard[x] == 'X') {
            B3.style.color = 'Red';
        } else {
            B3.style.color = 'Blue';
        }
        B3.innerHTML = gameBoard[x];
        B3.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('B3'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'C1') {
        const C1 = document.getElementById('C1');
        if (gameBoard[x] == 'X') {
            C1.style.color = 'Red';
        } else {
            C1.style.color = 'Blue';
        }
        C1.innerHTML = gameBoard[x];
        C1.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('C1'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'C2') {
        const C2 = document.getElementById('C2');
        if (gameBoard[x] == 'X') {
            C2.style.color = 'Red';
        } else {
            C2.style.color = 'Blue';
        }
        C2.innerHTML = gameBoard[x];
        C2.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('C2'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }
    }
    if (ID == 'C3') {
        const C3 = document.getElementById('C3');
        if (gameBoard[x] == 'X') {
            C3.style.color = 'Red';
        } else {
            C3.style.color = 'Blue';
        }
        C3.innerHTML = gameBoard[x];
        C3.disabled = true;
        checkWinner(gameBoard[x]);
        aiArray.splice(aiArray.indexOf('C3'), 1);
        V--;
        if (aiArray.length == 0) {
            return;
        } else {
            playingAI();
        }

    }
}
function compRender(ID) {
    if (ID == 'A1') {
        const A1 = document.getElementById('A1');
        if (gameBoard[x] == 'X') {
            A1.style.color = 'Red';
        } else {
            A1.style.color = 'Blue';
        }
        A1.innerHTML = gameBoard[x];
        A1.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'A2') {
        const A2 = document.getElementById('A2');
        if (gameBoard[x] == 'X') {
            A2.style.color = 'Red';
        } else {
            A2.style.color = 'Blue';
        }
        A2.innerHTML = gameBoard[x];
        A2.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'A3') {
        const A3 = document.getElementById('A3');
        if (gameBoard[x] == 'X') {
            A3.style.color = 'Red';
        } else {
            A3.style.color = 'Blue';
        }
        A3.innerHTML = gameBoard[x];
        A3.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'B1') {
        const B1 = document.getElementById('B1');
        if (gameBoard[x] == 'X') {
            B1.style.color = 'Red';
        } else {
            B1.style.color = 'Blue';
        }
        B1.innerHTML = gameBoard[x];
        B1.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'B2') {
        const B2 = document.getElementById('B2');
        if (gameBoard[x] == 'X') {
            B2.style.color = 'Red';
        } else {
            B2.style.color = 'Blue';
        }
        B2.innerHTML = gameBoard[x];
        B2.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'B3') {
        const B3 = document.getElementById('B3');
        if (gameBoard[x] == 'X') {
            B3.style.color = 'Red';
        } else {
            B3.style.color = 'Blue';
        }
        B3.innerHTML = gameBoard[x];
        B3.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'C1') {
        const C1 = document.getElementById('C1');
        if (gameBoard[x] == 'X') {
            C1.style.color = 'Red';
        } else {
            C1.style.color = 'Blue';
        }
        C1.innerHTML = gameBoard[x];
        C1.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'C2') {
        const C2 = document.getElementById('C2');
        if (gameBoard[x] == 'X') {
            C2.style.color = 'Red';
        } else {
            C2.style.color = 'Blue';
        }
        C2.innerHTML = gameBoard[x];
        C2.disabled = true;
        checkWinner(gameBoard[x]);
    }
    if (ID == 'C3') {
        const C3 = document.getElementById('C3');
        if (gameBoard[x] == 'X') {
            C3.style.color = 'Red';
        } else {
            C3.style.color = 'Blue';
        }
        C3.innerHTML = gameBoard[x];
        C3.disabled = true;
        checkWinner(gameBoard[x]);
    }
}



function inputDisable() {
    const A1 = document.getElementById('A1').innerHTML;
    const A2 = document.getElementById('A2').innerHTML;
    const A3 = document.getElementById('A3').innerHTML;
    const B1 = document.getElementById('B1').innerHTML;
    const B2 = document.getElementById('B2').innerHTML;
    const B3 = document.getElementById('B3').innerHTML;
    const C1 = document.getElementById('C1').innerHTML;
    const C2 = document.getElementById('C2').innerHTML;
    const C3 = document.getElementById('C3').innerHTML;

    A1.disabled = true;
    A2.disabled = true;
    A3.disabled = true;
    B1.disabled = true;
    B2.disabled = true;
    B3.disabled = true;
    C1.disabled = true;
    C2.disabled = true;
    C3.disabled = true;

}

function checkWinner(Player) {
    x++;
    const A1 = document.getElementById('A1').innerHTML;
    const A2 = document.getElementById('A2').innerHTML;
    const A3 = document.getElementById('A3').innerHTML;
    const B1 = document.getElementById('B1').innerHTML;
    const B2 = document.getElementById('B2').innerHTML;
    const B3 = document.getElementById('B3').innerHTML;
    const C1 = document.getElementById('C1').innerHTML;
    const C2 = document.getElementById('C2').innerHTML;
    const C3 = document.getElementById('C3').innerHTML;

    if (x == 9) {
        document.getElementById('results').innerHTML = 'Tie game!';
        inputDisable();
    }
    if (A1 == Player && A2 == Player && A3 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (B1 == Player && B2 == Player && B3 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (C1 == Player && C2 == Player && C3 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A1 == Player && B2 == Player && C3 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A1 == Player && B1 == Player && C1 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A2 == Player && B2 == Player && C2 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A3 == Player && B3 == Player && C3 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A3 == Player && B2 == Player && C1 == Player) {
        document.getElementById('results').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
}
function checkWinnerTwo(Player) {
    x++;
    const A1 = document.getElementById('A12').innerHTML;
    const A2 = document.getElementById('A22').innerHTML;
    const A3 = document.getElementById('A32').innerHTML;
    const B1 = document.getElementById('B12').innerHTML;
    const B2 = document.getElementById('B22').innerHTML;
    const B3 = document.getElementById('B32').innerHTML;
    const C1 = document.getElementById('C12').innerHTML;
    const C2 = document.getElementById('C22').innerHTML;
    const C3 = document.getElementById('C32').innerHTML;

    if (x == 9) {
        document.getElementById('results2').innerHTML = 'Tie game!';
        inputDisable();
    }
    if (A1 == Player && A2 == Player && A3 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (B1 == Player && B2 == Player && B3 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (C1 == Player && C2 == Player && C3 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A1 == Player && B2 == Player && C3 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A1 == Player && B1 == Player && C1 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A2 == Player && B2 == Player && C2 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A3 == Player && B3 == Player && C3 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
    if (A3 == Player && B2 == Player && C1 == Player) {
        document.getElementById('results2').innerHTML = 'Congrats, ' + Player + ' has won!';
        inputDisable();
    }
}

function resetGame() {
    document.getElementById('A1').innerHTML = "";
    document.getElementById('A2').innerHTML = "";
    document.getElementById('A3').innerHTML = "";
    document.getElementById('B1').innerHTML = "";
    document.getElementById('B2').innerHTML = "";
    document.getElementById('B3').innerHTML = "";
    document.getElementById('C1').innerHTML = "";
    document.getElementById('C2').innerHTML = "";
    document.getElementById('C3').innerHTML = "";
    document.getElementById('results').innerHTML = '';

    document.getElementById('A12').innerHTML = "";
    document.getElementById('A22').innerHTML = "";
    document.getElementById('A32').innerHTML = "";
    document.getElementById('B12').innerHTML = "";
    document.getElementById('B22').innerHTML = "";
    document.getElementById('B32').innerHTML = "";
    document.getElementById('C12').innerHTML = "";
    document.getElementById('C22').innerHTML = "";
    document.getElementById('C32').innerHTML = "";
    document.getElementById('results2').innerHTML = '';

    gameBoard = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'];
    let mainDisplay = document.getElementById('displayNone');
    let buttonDisplay = document.getElementById('buttonDisplay');
    buttonDisplay.style.display = 'none';
    mainDisplay.style.display = 'inherit';
}

function playingAI() {
    aiArray.sort(function() { return 0.5 - Math.random() });
    compRender(aiArray[V]);
    aiArray.pop();
    V--;
}


