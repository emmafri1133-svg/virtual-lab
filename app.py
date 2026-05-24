from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Virtual Electronics Lab</title>

    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: linear-gradient(135deg, #eef7f0, #eaf3ff);
        }

        header {
            background: linear-gradient(135deg, #12343b, #2f7d59);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .container {
            max-width: 1100px;
            margin: 30px auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 25px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        h2 {
            color: #2f7d59;
        }

        input, select {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 15px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #2f7d59;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background: #246346;
        }

        .results {
            margin-top: 20px;
        }

        .result {
            background: #eef7f0;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #2f7d59;
        }

        .led-box {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 20px auto;
            background: red;
            opacity: {{ led_opacity }};
            box-shadow: 0 0 {{ glow }}px rgba(255,0,0,0.8);
            transition: all 0.4s ease;
        }

        .status {
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            background: #f0f5f2;
        }

        @media(max-width:800px){
            .container{
                grid-template-columns:1fr;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>Virtual Electronics Lab</h1>
    <p>Ohm’s Law Interactive Simulator</p>
</header>

<div class="container">

    <div class="card">
        <h2>Control Panel</h2>

        <form method="POST">

            <label>Voltage (V)</label>
            <input type="number" name="voltage" value="{{ voltage }}" step="0.1">

            <label>Resistance (Ω)</label>
            <input type="number" name="resistance" value="{{ resistance }}" step="1">

            <label>Power</label>
            <select name="power">
                <option value="on">ON</option>
                <option value="off">OFF</option>
            </select>

            <button type="submit">Run Simulation</button>
        </form>
    </div>

    <div class="card">

        <h2>Simulation Output</h2>

        <div class="led-box"></div>

        <div class="results">
            <div class="result">Voltage: {{ voltage }} V</div>
            <div class="result">Current: {{ current_ma }} mA</div>
            <div class="result">Power: {{ power_mw }} mW</div>
        </div>

        <div class="status">
            {{ observation }}
        </div>

    </div>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def lab():
    voltage = 9.0
    resistance = 500.0
    power_on = True

    if request.method == "POST":
        voltage = float(request.form["voltage"])
        resistance = float(request.form["resistance"])
        power_on = request.form.get("power") == "on"

    if not power_on:
        current = 0
    else:
        current = voltage / resistance if resistance != 0 else 0

    power = voltage * current
    current_ma = current * 1000
    power_mw = power * 1000

    # LED logic
    if not power_on:
        observation = "Circuit is OFF."
        brightness = 0

    elif voltage < 2:
        observation = "Voltage too low. LED is OFF."
        brightness = 0

    elif current_ma < 8:
        observation = "LED is dim (low current)."
        brightness = 0.3

    elif current_ma <= 25:
        observation = "LED is in safe operating range."
        brightness = 0.7

    else:
        observation = "Warning: Too much current! LED may burn."
        brightness = 1

    return render_template_string(
        HTML,
        voltage=round(voltage, 2),
        resistance=round(resistance, 2),
        current_ma=round(current_ma, 2),
        power_mw=round(power_mw, 2),
        observation=observation,
        led_opacity=0.2 + brightness * 0.8,
        glow=10 + brightness * 50
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
