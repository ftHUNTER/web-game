group_name = "";
const chatSocket = new WebSocket('ws://' + 'localhost:8000' + '/ws/game/');
const canvas = document.getElementById("Game");
const context = canvas.getContext('2d');

const paddleWidth = 5, paddleHeight = 70;
const player1 = { x: 5, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, color: '#FFF' };
const player2 = { x: canvas.width - paddleWidth - 5, y: canvas.height / 2 - paddleHeight / 2, width: paddleWidth, height: paddleHeight, color: '#FFF' };

const ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 8, speed: 4, velocityX: 4, velocityY: 4, color: 'withe' };

function draw() {

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "rgba(0, 0, 0, 0.2)";
    context.fillRect(0, 0, canvas.width, canvas.height);


    context.fillStyle = player1.color;
    context.fillRect(player1.x , player1.y, player1.width, player1.height);

    context.fillStyle = player2.color;
    context.fillRect(player2.x, player2.y , player2.width, player2.height);

    context.fillStyle = ball.color;
    context.beginPath();
    context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2, false);
    context.fill();

    context.beginPath();
    context.setLineDash([4, 2]);
    context.moveTo(canvas.width / 2, 0);
    context.lineTo(canvas.width / 2, 350);
    context.lineWidth = 2;
    context.strokeStyle = "white";
    context.stroke();
}
stepX = 1
stepY = 1

function MoveBall() 
{
    const data = {TITLE : "move_ball",}
    chatSocket.send(JSON.stringify(data));
}

const keys = {
    up: false,
    down: false,
};

window.addEventListener("keydown", function (event) {
    if (event.key === 'ArrowUp') keys.up = true;
    if (event.key === 'ArrowDown') keys.down = true;
});

window.addEventListener("keyup", function (event) {
    if (event.key === 'ArrowUp') keys.up = false;
    if (event.key === 'ArrowDown') keys.down = false;
});


function MovePlayer()
{
    if (keys.up == true  )
    {        
        const data =  {TITLE : "move_player", player_direction : "up"}
        chatSocket.send(JSON.stringify(data))
    }
    if (keys.down == true ) 
    {
        const data =  {TITLE : "move_player", player_direction : "down"}
        chatSocket.send(JSON.stringify(data))
    }
}

function gameLoop() {
    MovePlayer();
    MoveBall();
    draw();
    requestAnimationFrame(gameLoop);
}

function waiting()
{
    console.log("Im waiting")
    const x = document.getElementById("test")
    x.innerHTML = "wait.........."
}

function nowait()
{
    const x = document.getElementById("test")
    x.innerHTML = ""
}

chatSocket.onopen =  function(event) {
    waiting();
};

chatSocket.onmessage = function(e) 
{
    const data = JSON.parse(e.data);
    if(data.TITLE == "start")
    {
        group_name = data.message;
        nowait();
        const info = {
            "TITLE" : "info",
            "canvas_width" : canvas.width , 
            "canvas_height" : canvas.height,
            "paddleWidth" : paddleWidth,
            "paddleHeight" : paddleHeight,
            "player1" : player1, 
            "player2" : player2,
            "ball" : ball,
        }
        chatSocket.send(JSON.stringify(info))
        gameLoop();
    }
    else if(data.TITLE == "move_ball")
    {
        ball.x = data.ballX
        ball.y = data.ballY
        
    }
    else if(data.TITLE == "move_player")
    {
        if(data.player == "player1")
            player1.y = data.position
        else
            player2.y = data.position

    }
    
    
};