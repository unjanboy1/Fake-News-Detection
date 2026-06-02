function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();

    let btn = document.getElementById("analyze-btn");
    let loader = document.getElementById("loader");
    let btnText = btn.querySelector('.btn-text');
    let chatBox = document.getElementById("chat-box");

    if (message === "" || message.split(' ').length < 20) {
        alert("Enter at least 20 words.");
        return;
    }

    btnText.style.display = "none";
    loader.style.display = "block";
    btn.disabled = true;

    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {

        btnText.style.display = "block";
        loader.style.display = "none";
        btn.disabled = false;

        if (data.error) {
            alert(data.error);
            return;
        }

        chatBox.innerHTML = "";

        let resultColor = data.label.includes("FAKE") ? "#ff0000" : "#00ff88";

        let card = document.createElement("div");
        card.className = "message";

        card.innerHTML = `
            <div>RESULT: <span style="color:${resultColor}">${data.label}</span></div>
            <div class="confidence-bar" style="color:${resultColor}">
                FAKE: ${data.fake}% | REAL: ${data.real}%
            </div>
        `;

        chatBox.appendChild(card);
    });
}