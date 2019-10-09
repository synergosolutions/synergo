const canvas = document.querySelector("canvas");
const c = canvas.getContext("2d")

let score = 0;
let grid = 16;
let dx = grid;
let dy = 0;
let count = 0;

let snake = {
    x: 160,
    y: 160,

    cells: [],
    maxCells: 4
};

let appleX = 320;
let appleY = 320;

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("touchstart", touchHandler, false);
document.addEventListener("touchmove", touchHandler, false);


function touchHandler(e) {
    if(e.touches) {
        if ((e.touches[0].pageX >= snake.x) && dx == 0) {
            dx = grid;
            dy = 0;
        } else if ((e.touches[0].pageX < snake.x) && dx == 0) {
            dx = -grid;
            dy = 0;
        } else if ((e.touches[0].pageY < snake.y) && dy == 0) {
            dx = 0;
            dy = -grid;
        } else if ((e.touches[0].pageY >= snake.y) && dy == 0) {
            dx = 0
            dy = grid;
        }

        e.preventDefault();
    }
}

function keyDownHandler(e) {
    if ((e.key == "Right" || e.key == "ArrowRight") && dx == 0) {
        dx = grid;
        dy = 0;
    } else if ((e.key == "Left" || e.key == "ArrowLeft") && dx == 0) {
        dx = -grid;
        dy = 0;
    } else if ((e.key == "Up" || e.key == "ArrowUp") && dy == 0) {
        dx = 0;
        dy = -grid;
    } else if ((e.key == "Down" || e.key == "ArrowDown") && dy == 0) {
        dx = 0;
        dy = grid;
    }
}

function getRandom(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function drawSnake() {
    c.fillStyle = "green";
    snake.cells.forEach(function(cell, index){
        c.fillRect(cell.x, cell.y, grid-1, grid-1);

        if (cell.x == appleX && cell.y == appleY) {
            snake.maxCells++;
            score++;

            appleX = getRandom(0, 25) * grid;
            appleY = getRandom(0, 25) * grid;
        }

        // collision
        for (let i = index + 1; i < snake.cells.length; i++) {
            if (cell.x == snake.cells[i].x && cell.y == snake.cells[i].y) {
                alert("Game Over");
                document.location.reload();
            }
        }
    })
}

function drawApple() {
    c.fillStyle = "red";
    c.fillRect(appleX, appleY, grid-1, grid-1);
}

function drawScore() {
    c.font = "16px sans-serif";
    c.fillStyle = "black";
    c.fillText("Score: "+score, 8, 20);
}

function draw() {
    // slowing game
    requestAnimationFrame(draw);
    if (++count < 4) {
        return;
    }
    count = 0;
    c.clearRect(0, 0, canvas.width, canvas.height);

    snake.x += dx;
    snake.y += dy;

    if (snake.x < 0) {
        snake.x = canvas.width - grid;
    } else if (snake.x >= canvas.width) {
        snake.x = 0;
    }

    if (snake.y < 0) {
        snake.y = canvas.height - grid;
    } else if (snake.y >= canvas.height) {
        snake.y = 0;
    }

    snake.cells.unshift({x: snake.x, y: snake.y});

    if (snake.cells.length > snake.maxCells) {
        snake.cells.pop();
    }

    drawScore();
    drawApple();
    drawSnake();


}

draw();