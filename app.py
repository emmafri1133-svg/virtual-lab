from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Virtual Electronics Lab</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            color: #172026;
            background: linear-gradient(135deg, #eef7f0, #eaf3ff);
        }

        header {
            padding: 25px;
            text-align: center;
            color: white;
            background: linear-gradient(135deg, #12343b, #2f7d59);
        }

        header h1 {
            margin: 0;
            font-size: 42px;
        }

        header p {
            font-size: 18px;
        }

        .container {
            max-width: 1100px;
            margin: 30px auto;
            padding: 20px;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 25px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.12);
        }

        h2 {
            color: #2f7d59;
            margin-top: 0;
        }

        label {
            font-weight: bold;
            display: block;
            margin-top: 15px;
        }

        input {
            width: 100%;
            padding: 12px;
            margin-top: 6px;
            font-size: 16px;
            border: 2px solid #d7e3d4;
            border-radius: 8px;
        }

        button {
            width: 100%;
            margin-top: 20px;
            padding: 14px;
            background: #2f7d59;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #246346;
        }

        .components {
            display: grid;
            gap: 12px;
            margin-top: 20px;
        }

        .component {
            display: flex;
            align-items: center;
            gap: 12px;
            background: #f5faf4;
            border: 1px solid #d7e3d4;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
        }

        .icon {
            width: 34px;
            height: 34px;
        }

        .battery {
            border: 4px solid #356d9f;
            border-radius: 5px;
        }

        .resistor {
            background: repeating-linear-gradient(
                90deg,
                #d9902f 0 8px,
                #f7cf72 8px 14px
            );
            border-radius: 5px;
        }

        .led {
            background: #c84e43;
            border-radius: 50%;
            box-shadow: 0 0 18px rgba(200,78,67,0.8);
        }

        .meter {
            border: 4px solid #147c85;
            border-radius: 50%;
        }

        .circuit {
            position: relative;
            height: 380px;
            border-radius: 15px;
            border: 2px solid #d7e3d4;
            background:
                linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px),
                linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
                #fbfdf9;
            background-size: 28px 28px;
            overflow: hidden;
        }

        .wire {
            position: absolute;
            background: #6d7a80;
        }

        .wire.top, .wire.bottom {
            height: 8px;
            left: 20%;
            right: 20%;
        }

        .wire.top {
            top: 25%;
        }

        .wire.bottom {
            bottom: 25%;
        }

        .wire.left, .wire.right {
            width: 8px;
            top: 25%;
            bottom: 25%;
        }

        .wire.left {
            left: 20%;
        }

        .wire.right {
            right: 20%;
        }

        .part {
            position: absolute;
            background: white;
            border-radius: 12px;
            font-weight: bold;
            text-align: center;
            display: grid;
            place-items: center;
            z-index: 2;
        }

        .battery-box {
            top: 10%;
            left: 50%;
            transform: translateX(-50%);
            width: 160px;
            height: 70px;
            border: 3px solid #356d9f;
        }

        .resistor-box {
            top: calc(25% - 24px);
            left: 50%;
            transform: translateX(-50%);
            width: 170px;
            height: 48px;
            background: #f3c66d;
            border: 3px solid #b36f1e;
        }

        .led-box {
            right: calc(20% - 32px);
            top: 50%;
            transform: translateY(-50%);
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #c84e43;
            opacity: {{ led_opacity }};
            box-shadow: 0 0 {{ glow }}px rgba(200,78,67,0.85);
        }

        .meter-box {
            bottom: 10%;
            left: 50%;
            transform: translateX(-50%);
            width: 160px;
            height: 70px;
            border: 3px solid #147c85;
        }

        .results {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .result {
            background: #f2f8f4;
            border-left: 6px solid #2f7d59;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
        }

        .result strong {
            display: block;
            font-size: 25px;
            margin-top: 8px;
        }

        .observation {
            margin-top: 20px;
            padding: 18px;
            border-radius: 12px;
            background: {{ bg }};
            border-left: 6px solid {{ color }};
            font-weight: bold;
            line-height: 1.6;
        }

        @media (max-width: 800px) {
            .grid, .results {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

<header>
    <h1>Virtual Electronics Lab</h1>
    <p>Interactive Ohm's Law Circuit Simulator</p>
</header>

<div class="container">
    <div class="grid">
        <div class="card">
            <h2>Control Panel</h2>

            <form method="POST">
                <label>Voltage Supply (V)</label>
                <input type="number" name="voltage" step="0.1" min="0" value="{{ voltage }}" required>

                <label>Resistance (Ohms)</label>
                <input type="number" name="resistance" step="1" min="1" value="{{ resistance }}" required>

                <button type="submit">Run Simulation</button>
            </form>

            <h2 style="margin-top:25px;">Components</h2>

            <div class="components">
                <div class="component"><div class="icon battery"></div> Battery</div>
                <div class="component"><div class="icon resistor"></div> Resistor</div>
                <div class="component"><div class="icon led"></div> LED</div>
                <div class="component"><div class="icon meter"></div> Ammeter</div>
            </div>
        </div>

        <div class="card">
            <h2>Virtual Circuit</h2>

            <div class="circuit">
                <div class="wire top"></div>
                <div class="wire bottom"></div>
                <div class="wire left"></div>
                <div class="wire right"></div>

                <div class="part battery-box">Battery<br>{{ voltage }} V</div>
                <div class="part resistor-box">Resistor<br>{{ resistance }} Ω</div>
                <div class="part led-box"></div>
                <div class="part meter-box">Ammeter<br>{{ current }} A</div>
            </div>

            <div class="results">
                <div class="result">
                    Voltage
                    <strong>{{ voltage }} V</strong>
                </div>

                <div class="result">
                    Current
                    <strong>{{ current_ma }} mA</strong>
                </div>

                <div class="result">
                    Power
                    <strong>{{ power_mw }} mW</strong>
                </div>
            </div>

            <div class="observation">
                {{ observation }}
            </div>
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

    if request.method == "POST":
        voltage = float(request.form["voltage"])
        resistance = float(request.form["resistance"])

    current = voltage / resistance
    power = voltage * current
    current_ma = current * 1000
    power_mw = power * 1000

    brightness = min(current_ma / 25, 1)

    if current_ma < 8:
        observation = "The LED is dim because the current is low. Increase voltage or reduce resistance."
        color = "#356d9f"
        bg = "#edf5fb"
    elif current_ma <= 25:
        observation = "The circuit is in a safe range for a typical LED."
        color = "#2f7d59"
        bg = "#edf7f0"
    else:
        observation = "Warning: Current is too high for a typical LED. Increase resistance."
        color = "#c84e43"
        bg = "#fff0ee"

    return render_template_string(
        HTML,
        voltage=round(voltage, 2),
        resistance=round(resistance, 2),
        current=round(current, 4),
        current_ma=round(current_ma, 2),
        power_mw=round(power_mw, 2),
        observation=observation,
        led_opacity=round(0.25 + brightness * 0.75, 2),
        glow=round(12 + brightness * 45),
        color=color,
        bg=bg
    )

if __name__ == "__main__":
    app.run(debug=True)