const canvas = document.querySelector("canvas");
const c = canvas.getContext("2d");

canvas.width = innerWidth;
canvas.height = innerHeight;
c.lineJoin = "round";
c.lineCap = "round";

let lastX = 0;
let lastY = 0;
let isDraw = false;

let color = document.getElementsByName("color")[0].value;
let size = document.querySelector("select").value;

canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mousedown", (event) => {
    isDraw = true;
    lastX = event.offsetX;
    lastY = event.offsetY;
});
canvas.addEventListener("mouseup", () => isDraw = false);
canvas.addEventListener("mouseout", () => isDraw = false);

canvas.addEventListener('touchstart', event => {
    lastX = event.touches[0].pageX;
    lastY = event.touches[0].pageY;
    color = document.getElementsByName("color")[0].value;
    size = document.querySelector("select").value;
});

canvas.addEventListener('touchmove', event => {
    event.preventDefault();
    c.strokeStyle = color;
    c.lineWidth = size;
    c.beginPath();
    c.moveTo(lastX, lastY);
    c.lineTo(event.touches[0].pageX, event.touches[0].pageY);
    c.stroke();

    lastX = event.touches[0].pageX;
    lastY = event.touches[0].pageY;
});

function draw(event) {
    if (!isDraw)
        return;

    color = document.getElementsByName("color")[0].value;
    size = document.querySelector("select").value;
    c.strokeStyle = color;
    c.lineWidth = size;
    c.beginPath();
    c.moveTo(lastX, lastY);
    c.lineTo(event.offsetX, event.offsetY);
    c.stroke();

    lastX = event.offsetX;
    lastY = event.offsetY;
};


addEventListener("resize", () => {
    canvas.width = innerWidth;
    canvas.height = innerHeight;
});