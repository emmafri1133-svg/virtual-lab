from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Circuit Game</title>

<style>
body {
    margin:0;
    font-family:Arial;
    background:linear-gradient(135deg,#1e293b,#0f172a);
    color:white;
}

header {
    padding:15px;
    text-align:center;
    background:#0f172a;
}

.container {
    display:grid;
    grid-template-columns:1fr 2fr;
    gap:20px;
    padding:20px;
}

.card {
    background:#1e293b;
    padding:20px;
    border-radius:12px;
}

button {
    padding:10px;
    margin:5px;
    border:none;
    border-radius:8px;
    background:#22c55e;
    color:white;
    cursor:pointer;
}

/* CIRCUIT */
.circuit {
    position:relative;
    height:450px;
    border:2px solid #334155;
}

/* COMPONENTS */
.component {
    position:absolute;
    padding:10px;
    border-radius:10px;
    cursor:grab;
}

.battery { background:#3b82f6; }
.resistor { background:#facc15; }
.led {
    width:60px;height:60px;
    border-radius:50%;
    background:red;
    animation:pulse 1s infinite;
}

@keyframes pulse {
    0%{transform:scale(1)}
    50%{transform:scale(1.1)}
    100%{transform:scale(1)}
}

/* NODES */
.node {
    width:10px;height:10px;
    background:white;
    border-radius:50%;
    position:absolute;
}

/* WIRES */
.wire {
    position:absolute;
    height:4px;
    background:linear-gradient(90deg,#0ea5e9,#22d3ee,#0ea5e9);
    background-size:200%;
    animation:flow 1s linear infinite;
}

@keyframes flow {
    0%{background-position:0%}
    100%{background-position:200%}
}

/* POPUP */
#popup {
    position:fixed;
    top:40%;
    left:50%;
    transform:translate(-50%,-50%);
    background:#22c55e;
    padding:30px;
    border-radius:12px;
    display:none;
}

/* LEVEL MENU */
#menu {
    text-align:center;
}
</style>

</head>

<body>

<header>
<h1>⚡ Circuit Builder Game</h1>
<div>Score: <span id="score">0</span></div>
</header>

<div id="menu">
<h2>Select Level</h2>
<button onclick="startLevel(1)">Level 1</button>
<button onclick="startLevel(2)">Level 2</button>
<button onclick="startLevel(3)">Level 3</button>
</div>

<div class="container" id="game" style="display:none;">

<div class="card">
<h3 id="levelText"></h3>
Voltage <input id="voltage" value="9">
<p id="result"></p>
<button onclick="solveCircuit()">Solve</button>

<h4>Achievements</h4>
<ul id="achievements"></ul>
</div>

<div class="card">
<div class="circuit" id="circuit">

<div class="component battery" style="top:40px;left:40px;">
<div class="node" id="b1" style="top:-5px;left:20px;" onclick="connect(this)"></div>
<div class="node" id="b2" style="bottom:-5px;left:20px;" onclick="connect(this)"></div>
</div>

<div class="component resistor" style="top:150px;left:200px;">
<div class="node" id="r1" style="top:-5px;left:20px;" onclick="connect(this)"></div>
<div class="node" id="r2" style="bottom:-5px;left:20px;" onclick="connect(this)"></div>
</div>

<div class="component led" style="top:250px;left:400px;">
<div class="node" id="l1" style="top:-5px;left:20px;" onclick="connect(this)"></div>
<div class="node" id="l2" style="bottom:-5px;left:20px;" onclick="connect(this)"></div>
</div>

</div>
</div>

</div>

<div id="popup">LEVEL COMPLETE 🎉</div>

<script>
let selected=null;
let connections=[];
let firstNode=null;

let level=1;
let score=0;
let startTime;

// DRAG
document.querySelectorAll('.component').forEach(el=>{
    el.onmousedown=()=>selected=el;
});
document.onmouseup=()=>selected=null;
document.onmousemove=e=>{
    if(selected){
        selected.style.left=(Math.round(e.pageX/25)*25)+'px';
        selected.style.top=(Math.round(e.pageY/25)*25)+'px';
    }
};

// LEVEL SYSTEM
function startLevel(l){
    level=l;
    document.getElementById("menu").style.display="none";
    document.getElementById("game").style.display="grid";
    startTime=Date.now();

    let text = [
        "Level 1: Light LED",
        "Level 2: Safe current",
        "Level 3: Dim LED"
    ];

    document.getElementById("levelText").innerText=text[l-1];
}

// CONNECTION
function connect(node){
    if(!firstNode){
        firstNode=node;
        node.style.background="yellow";
    } else {
        connections.push([firstNode.id,node.id]);
        drawWire(firstNode,node);
        firstNode.style.background="white";
        firstNode=null;
    }
}

function drawWire(a,b){
    let wire=document.createElement("div");
    wire.className="wire";

    let r1=a.getBoundingClientRect();
    let r2=b.getBoundingClientRect();

    let x1=r1.left, y1=r1.top;
    let x2=r2.left, y2=r2.top;

    let length=Math.hypot(x2-x1,y2-y1);
    let angle=Math.atan2(y2-y1,x2-x1)*180/Math.PI;

    wire.style.width=length+"px";
    wire.style.left=x1+"px";
    wire.style.top=y1+"px";
    wire.style.transform="rotate("+angle+"deg)";

    document.body.appendChild(wire);
}

// SOLVER + SCORE
function solveCircuit(){
    let voltage=parseFloat(document.getElementById("voltage").value);
    let timeTaken=(Date.now()-startTime)/1000;

    let current=voltage/100;
    let current_ma=current*1000;

    let success=false;

    if(level==1) success=true;
    if(level==2 && current_ma<=25) success=true;
    if(level==3 && current_ma<8) success=true;

    if(success){
        let points=100;
        if(timeTaken<10) points+=50;

        score+=points;
        document.getElementById("score").innerText=score;

        showPopup();
        addAchievement(timeTaken);

    } else {
        document.getElementById("result").innerText="❌ Wrong";
    }
}

// POPUP
function showPopup(){
    let p=document.getElementById("popup");
    p.style.display="block";
    setTimeout(()=>p.style.display="none",2000);
}

// ACHIEVEMENTS
function addAchievement(time){
    let list=document.getElementById("achievements");

    if(time<10){
        list.innerHTML += "<li>⚡ Fast Builder</li>";
    }

    list.innerHTML += "<li>🏆 Level Complete</li>";
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
