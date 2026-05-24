from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Advanced Virtual Electronics Lab</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    background: linear-gradient(135deg,#eef7f0,#eaf3ff);
}

header {
    text-align:center;
    padding:20px;
    background:#12343b;
    color:white;
}

.container {
    max-width:1200px;
    margin:auto;
    padding:20px;
    display:grid;
    grid-template-columns:1fr 2fr;
    gap:20px;
}

.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0 10px 30px rgba(0,0,0,0.1);
}

input,select,button {
    width:100%;
    padding:10px;
    margin-top:10px;
}

button {
    background:#2f7d59;
    color:white;
    border:none;
}

.circuit {
    position:relative;
    height:350px;
    background:#f9fdf9;
    border:2px solid #ccc;
}

/* wires */
.wire { position:absolute; background:#555; }
.top { top:20%; left:20%; right:20%; height:6px; }
.bottom { bottom:20%; left:20%; right:20%; height:6px; }
.left { left:20%; top:20%; bottom:20%; width:6px; }
.right { right:20%; top:20%; bottom:20%; width:6px; }

/* components */
.part {
    position:absolute;
    background:white;
    border-radius:8px;
    text-align:center;
    font-size:12px;
}

.battery { top:5%; left:45%; width:100px; height:50px; border:2px solid blue; }
.resistor { top:18%; left:45%; width:120px; height:40px; background:#f3c66d; }
.ammeter { bottom:5%; left:45%; width:100px; height:50px; border:2px solid teal; }

.led {
    right:18%;
    top:50%;
    width:60px;
    height:60px;
    border-radius:50%;
    background:red;
    transform:translateY(-50%);
    opacity:{{led_opacity}};
    box-shadow:0 0 {{glow}}px red;
    transition:all 0.4s ease;
}

.results {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
    margin-top:15px;
}

.result {
    background:#eef7f0;
    padding:10px;
    text-align:center;
}

.status {
    margin-top:15px;
    padding:10px;
    background:#f0f5f2;
}

canvas {
    margin-top:20px;
    width:100%;
}

@media(max-width:800px){
    .container{grid-template-columns:1fr;}
}
</style>

</head>

<body>

<header>
<h1>Advanced Electronics Lab</h1>
<p>Interactive Circuit Simulator</p>
</header>

<div class="container">

<div class="card">
<h2>Controls</h2>

<form method="POST">
Voltage (V)
<input type="number" name="voltage" value="{{voltage}}" step="0.1">

Resistance (Ω)
<input type="number" name="resistance" value="{{resistance}}">

Power
<select name="power">
<option value="on">ON</option>
<option value="off">OFF</option>
</select>

<button>Run Simulation</button>
</form>
</div>

<div class="card">

<h2>Circuit</h2>

<div class="circuit">
<div class="wire top"></div>
<div class="wire bottom"></div>
<div class="wire left"></div>
<div class="wire right"></div>

<div class="part battery">Battery<br>{{voltage}}V</div>
<div class="part resistor">Resistor<br>{{resistance}}Ω</div>
<div class="part ammeter">Ammeter<br>{{current_ma}}mA</div>

<div class="led"></div>
</div>

<div class="results">
<div class="result">Voltage {{voltage}}V</div>
<div class="result">Current {{current_ma}}mA</div>
<div class="result">Power {{power_mw}}mW</div>
</div>

<div class="status">
{{observation}}
</div>

<canvas id="graph"></canvas>

</div>

</div>

<script>
const ctx = document.getElementById('graph').getContext('2d');

new Chart(ctx,{
type:'line',
data:{
labels:[0,2,4,6,8,10],
datasets:[{
label:'Current vs Voltage',
data:{{graph_data}},
borderWidth:2
}]
}
});
</script>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def lab():
    voltage = 9
    resistance = 500
    power_on = True

    if request.method == "POST":
        voltage = float(request.form["voltage"])
        resistance = float(request.form["resistance"])
        power_on = request.form.get("power") == "on"

    current = (voltage/resistance) if power_on else 0
    current_ma = current*1000
    power_mw = voltage*current*1000

    if not power_on:
        brightness = 0
        observation="Circuit OFF"
    elif voltage < 2:
        brightness = 0
        observation="Voltage too low"
    elif current_ma < 8:
        brightness = 0.3
        observation="Dim LED"
    elif current_ma <= 25:
        brightness = 0.7
        observation="Normal operation"
    else:
        brightness = 1
        observation="Too much current!"

    graph_data = [round((v/resistance)*1000,2) for v in [0,2,4,6,8,10]]

    return render_template_string(
        HTML,
        voltage=voltage,
        resistance=resistance,
        current_ma=round(current_ma,2),
        power_mw=round(power_mw,2),
        observation=observation,
        led_opacity=0.2+brightness*0.8,
        glow=10+brightness*50,
        graph_data=graph_data
    )

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
