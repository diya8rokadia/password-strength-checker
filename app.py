import hashlib
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength & Breach Checker</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .strength-meter { height: 10px; border-radius: 5px; }
    </style>
</head>
<body class="bg-light">
<div class="container py-5">
    <h2 class="mb-4 text-center">🔒 Password Strength & Breach Checker</h2>
    <div class="card p-4 shadow-sm">
        <div class="mb-3">
            <label for="password" class="form-label">Enter Password:</label>
            <input type="password" id="password" class="form-control" placeholder="Type your password">
        </div>
        <div class="mb-3">
            <div id="strength-text"></div>
            <div class="strength-meter bg-secondary" id="strength-meter"></div>
        </div>
        <button class="btn btn-primary" onclick="checkPassword()">Check</button>
        <div class="mt-3" id="result"></div>
    </div>
</div>

<script>
async function checkPassword() {
    let password = document.getElementById("password").value;
    if (!password) {
        alert("Please enter a password");
        return;
    }
    let res = await fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: password })
    });
    let data = await res.json();

    let meter = document.getElementById("strength-meter");
    let text = document.getElementById("strength-text");

    meter.className = "strength-meter";
    meter.style.width = data.strength_score + "%";
    if (data.strength_score < 40) {
        meter.classList.add("bg-danger");
        text.innerText = "Weak Password";
    } else if (data.strength_score < 70) {
        meter.classList.add("bg-warning");
        text.innerText = "Moderate Password";
    } else {
        meter.classList.add("bg-success");
        text.innerText = "Strong Password";
    }

    let result = document.getElementById("result");
    if (data.breached) {
        result.innerHTML = `<div class='alert alert-danger'>⚠️ This password has been found in data breaches! (${data.breach_count} times)</div>`;
    } else {
        result.innerHTML = `<div class='alert alert-success'>✅ This password is safe (not found in known breaches)</div>`;
    }

    result.innerHTML += `<div><b>Suggestions:</b> ${data.suggestions.join(", ")}</div>`;
}
</script>
</body>
</html>
"""

def check_strength(password):
    score = 0
    suggestions = []
    if len(password) >= 8:
        score += 30
    else:
        suggestions.append("Use at least 8 characters")
    
    if any(c.islower() for c in password):
        score += 15
    else:
        suggestions.append("Add lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 15
    else:
        suggestions.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 15
    else:
        suggestions.append("Add numbers")
    
    if any(c in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|" for c in password):
        score += 25
    else:
        suggestions.append("Add special characters")
    
    return min(score, 100), suggestions

def check_breach(password):
    sha1pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1pwd[:5], sha1pwd[5:]
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code != 200:
        return False, 0
    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return True, int(count)
    return False, 0

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    password = data.get("password", "")
    strength_score, suggestions = check_strength(password)
    breached, breach_count = check_breach(password)
    return jsonify({
        "strength_score": strength_score,
        "suggestions": suggestions,
        "breached": breached,
        "breach_count": breach_count
    })

if __name__ == "__main__":
    app.run(debug=True)
