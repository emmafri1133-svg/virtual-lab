from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Pro Circuit Simulator</title>

<style>
body {
    margin:0;
    font-family:Arial;
    background:#f0f4f8;
}

.dark {
    background:#121212;
    color:white;
}

header {
    padding:15px;
    text-align:center;
    background:#2f7d59;
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
    border-radius:10px;
}

.dark .card {
    background:#1e1e1e;
}

.circuit {
    position:relative;
    height:400px;
    border:2px dashed #aaa;
}

.component {
    position:absolute;
    padding:10px;
    border-radius:8px;
    cursor:grab;
    font-size:12px;
    text-align:center;
}

.battery { background:#4da3ff; }
.resistor { background:#f3c66d; }
.led {
    background:red;
    border-radius:50%;
    width:60px;
    height:60px;
    opacity:{{led_opacity}};
    box-shadow:0 0 {{glow}}px red;
}

/* connection nodes */
.node {
    width:10px;
    height:10px;
    background:black;
    position:absolute;
    border-radius:50%;
    cursor:pointer;
}

/* wire */
.wire {
    position:absolute;
    height:3px;
    background:black;
    transform-origin:left center;
}
</style>

</head>

<body>

<header>
<h1>Pro Circuit Simulator</h1>
<button onclick="toggleDark()">Dark Mode</button>
<button onclick="saveCircuit()">Save</button>
<button onclick="loadCircuit()">Load</button>
</header>

<div class="container">

<div class="card">
<form method="POST">
Voltage
<input type="number" name="voltage" value="{{voltage}}">
Resistance
<input type="number" name="resistance" value="{{resistance}}">
<button>Simulate</button>
</form>

<p>{{observation}}</p>
</div>

<div class="card">
<div class="circuit" id="circuit">

<div class="component battery" style="top:40px;left:40px;">
Battery
<div class="node" id="b1" style="top:-5px;left:20px;" onclick="connect(this)"></div>
<div class="node" id="b2" style="bottom:-5px;left:20px;" onclick="connect(this)"></div>
</div>

<div class="component resistor" style="top:150px;left:200px;">
Resistor
<div class="node" id="r1" style="top:-5px;left:30px;" onclick="connect(this)"></div>
<div class="node" id="r2" style="bottom:-5px;left:30px;" onclick="connect(this)"></div>
</div>

<div class="component led" style="top:250px;left:400px;">
<div class="node" id="l1" style="top:-5px;left:25px;" onclick="connect(this)"></div>
<div class="node" id="l2" style="bottom:-5px;left:25px;" onclick="connect(this)"></div>
</div>

</div>
</div>

</div>

<script>
// DARK MODE
function toggleDark(){
    document.body.classList.toggle("dark");
}

// DRAG
let selected=null;
document.querySelectorAll('.component').forEach(el=>{
    el.onmousedown=()=>selected=el;
});
document.onmouseup=()=>selected=null;
document.onmousemove=e=>{
    if(selected){
        selected.style.left=e.pageX-50+'px';
        selected.style.top=e.pageY-80+'px';
    }
};

// CONNECTION SYSTEM
let connections=[];
let firstNode=null;

function connect(node){
    if(!firstNode){
        firstNode=node;
        node.style.background="yellow";
    }else{
        connections.push([firstNode.id,node.id]);
        drawWire(firstNode,node);
        firstNode.style.background="black";
        firstNode=null;
    }
}

function drawWire(a,b){
    let wire=document.createElement("div");
    wire.className="wire";

    let x1=a.getBoundingClientRect().left;
    let y1=a.getBoundingClientRect().top;
    let x2=b.getBoundingClientRect().left;
    let y2=b.getBoundingClientRect().top;

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
    alert("Saved!");
}

function loadCircuit(){
    let data=JSON.parse(localStorage.getItem("circuit"));
    if(data){
        connections=data;
        alert("Loaded!");
    }
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def lab():
    voltage=9
    resistance=500

    if request.method=="POST":
        voltage=float(request.form["voltage"])
        resistance=float(request.form["resistance"])

    current=voltage/resistance if resistance else 0
    current_ma=current*1000

    if voltage<2:
        brightness=0
        observation="LED OFF"
    elif current_ma<8:
        brightness=0.3
        observation="Dim"
    elif current_ma<=25:
        brightness=0.7
        observation="Normal"
    else:
        brightness=1
        observation="Too much current!"

    return render_template_string(
        HTML,
        voltage=voltage,
        resistance=resistance,
        observation=observation,
        led_opacity=0.2+brightness*0.8,
        glow=10+brightness*50
    )

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
