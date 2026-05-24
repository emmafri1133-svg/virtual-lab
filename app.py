from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Advanced Circuit Simulator</title>

<style>
body {
    margin:0;
    font-family:Arial;
    background: linear-gradient(135deg,#eef7f0,#eaf3ff);
}

.dark {
    background:#0f172a;
    color:white;
}

header {
    padding:15px;
    text-align:center;
    background:linear-gradient(135deg,#12343b,#2f7d59);
    color:white;
}

.container {
    display:grid;
    grid-template-columns:1fr 2fr;
    gap:20px;
    padding:20px;
}

.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 10px 30px rgba(0,0,0,0.1);
}

.dark .card {
    background:#1e293b;
}

.circuit {
    position:relative;
    height:450px;
    border-radius:15px;
    border:2px solid #ccc;
    background:
        linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px),
        linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
        #f8fafc;
    background-size:25px 25px;
}

/* COMPONENTS */
.component {
    position:absolute;
    padding:10px;
    border-radius:10px;
    cursor:grab;
    text-align:center;
    color:white;
    font-weight:bold;
}

.battery {
    background:linear-gradient(135deg,#3b82f6,#1d4ed8);
}

.resistor {
    background:repeating-linear-gradient(
        90deg,#d97706 0 8px,#facc15 8px 16px
    );
    color:black;
}

.led {
    width:65px;
    height:65px;
    border-radius:50%;
    background: radial-gradient(circle,#ff4d4d,#990000);
    box-shadow:0 0 {{glow}}px rgba(255,0,0,0.9);
    animation:pulse 1.2s infinite;
}

/* LED pulse */
@keyframes pulse {
    0% { transform:scale(1); }
    50% { transform:scale(1.1); }
    100% { transform:scale(1); }
}

/* NODES */
.node {
    width:12px;
    height:12px;
    background:black;
    border-radius:50%;
    position:absolute;
    cursor:pointer;
}

/* WIRES */
.wire {
    position:absolute;
    height:4px;
    background: linear-gradient(90deg,#00f2ff,#0ea5e9,#00f2ff);
    background-size:200% 100%;
    animation:flow 1s linear infinite;
    transform-origin:left center;
}

@keyframes flow {
    0% { background-position:0% 0; }
    100% { background-position:200% 0; }
}

button {
    padding:10px;
    margin-top:5px;
    width:100%;
    border:none;
    border-radius:8px;
    background:#2f7d59;
    color:white;
    cursor:pointer;
}

button:hover {
    transform:scale(1.05);
}
</style>

</head>

<body>

<header>
<h1>Advanced Circuit Simulator</h1>
<button onclick="toggleDark()">Dark Mode</button>
<button onclick="saveCircuit()">Save</button>
<button onclick="loadCircuit()">Load</button>
<button onclick="solveCircuit()">Solve</button>
</header>

<div class="container">

<div class="card">
Voltage
<input id="voltage" type="number" value="9">
<p id="result">Build a circuit</p>
</div>

<div class="card">
<div class="circuit" id="circuit">

<div class="component battery" style="top:40px;left:40px;">
Battery
<div class="node" id="b1" style="top:-6px;left:20px;" onclick="connect(this)"></div>
<div class="node" id="b2" style="bottom:-6px;left:20px;" onclick="connect(this)"></div>
</div>

<div class="component resistor" style="top:150px;left:200px;">
R1
<div class="node" id="r1a" style="top:-6px;left:25px;" onclick="connect(this)"></div>
<div class="node" id="r1b" style="bottom:-6px;left:25px;" onclick="connect(this)"></div>
</div>

<div class="component led" style="top:250px;left:400px;">
<div class="node" id="l1" style="top:-6px;left:25px;" onclick="connect(this)"></div>
<div class="node" id="l2" style="bottom:-6px;left:25px;" onclick="connect(this)"></div>
</div>

</div>
</div>

</div>

<script>
// DARK MODE
function toggleDark(){
    document.body.classList.toggle("dark");
}

// DRAG + SNAP GRID
let selected=null;
const grid=25;

document.querySelectorAll('.component').forEach(el=>{
    el.onmousedown=()=>selected=el;
});

document.onmouseup=()=>selected=null;

document.onmousemove=e=>{
    if(selected){
        let x=Math.round((e.pageX-50)/grid)*grid;
        let y=Math.round((e.pageY-80)/grid)*grid;
        selected.style.left=x+"px";
        selected.style.top=y+"px";
    }
};

// CONNECTION SYSTEM
let connections=[];
let firstNode=null;

function connect(node){
    if(!firstNode){
        firstNode=node;
        node.style.background="yellow";
    } else {
        let rectA=firstNode.getBoundingClientRect();
        let rectB=node.getBoundingClientRect();

        let distance=Math.hypot(
            rectA.left-rectB.left,
            rectA.top-rectB.top
        );

        if(distance<60){
            connections.push([firstNode.id,node.id]);
            drawWire(firstNode,node);
        } else {
            alert("Move nodes closer!");
        }

        firstNode.style.background="black";
        firstNode=null;
    }
}

// DRAW WIRE
function drawWire(a,b){
    let wire=document.createElement("div");
    wire.className="wire";

    let r1=a.getBoundingClientRect();
    let r2=b.getBoundingClientRect();

    let x1=r1.left+r1.width/2;
    let y1=r1.top+r1.height/2;
    let x2=r2.left+r2.width/2;
    let y2=r2.top+r2.height/2;

    let length=Math.hypot(x2-x1,y2-y1);
    let angle=Math.atan2(y2-y1,x2-x1)*180/Math.PI;

    wire.style.width=length+"px";
    wire.style.left=x1+"px";
    wire.style.top=y1+"px";
    wire.style.transform="rotate("+angle+"deg)";

    document.body.appendChild(wire);
}

// SAVE / LOAD
function saveCircuit(){
    localStorage.setItem("circuit",JSON.stringify(connections));
    alert("Saved");
}

function loadCircuit(){
    let data=JSON.parse(localStorage.getItem("circuit"));
    if(data){
        connections=data;
        alert("Loaded");
    }
}

// SOLVER (basic)
function solveCircuit(){
    let voltage=parseFloat(document.getElementById("voltage").value);

    let nodes=connections.flat();

    if(!nodes.includes("b1") || !nodes.includes("b2")){
        document.getElementById("result").innerText="Incomplete circuit";
        return;
    }

    let resistance=100;
    let current=voltage/resistance;

    document.getElementById("result").innerText=
        "Current: "+current.toFixed(3)+" A";
}
</script>

</body>
</html>
"""

@app.route("/")
def lab():
    return render_template_string(
        HTML,
        glow=40
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
