document.addEventListener("DOMContentLoaded", () => {
    const rsvpForm = document.getElementById("rsvp-form");
    const checkInForm = document.getElementById("check-in-form");

    if (rsvpForm) {
        rsvpForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const code = document.getElementById("rsvp-code").value.trim();

            if (code.length !== 4) {
                document.getElementById("error-msg").textContent = "Invalid Code! Must be 4 characters.";
                return;
            }

            // Send code to backend
            fetch('/verify-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    window.location.href = `/rsvp.html?code=${code}`;
                } else {
                    document.getElementById("error-msg").textContent = "Invalid Code. Try Again!";
                }
            });
        });
    }

    if (checkInForm) {
        checkInForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const code = document.getElementById("verify-code").value.trim();

            fetch('/verify-guest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            })
            .then(response => response.json())
            .then(data => {
                if (data.valid) {
                    document.getElementById("check-in-msg").textContent = `Welcome, ${data.name}! Your seat number is ${data.seat}.`;
                } else {
                    document.getElementById("check-in-msg").textContent = "Invalid Code! Please try again.";
                }
            });
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    const rsvpCode = urlParams.get('code');

    const yesBtn = document.querySelector(".yes-btn");
    const noBtn = document.querySelector(".no-btn");

    if (yesBtn && noBtn) {
        yesBtn.addEventListener("click", () => sendRSVP('yes'));
        noBtn.addEventListener("click", () => sendRSVP('no'));
    }

    function sendRSVP(response) {
        fetch('/submit-rsvp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: rsvpCode, response })
        })
        .then(() => {
            alert(response === 'yes' ? "Thank you for confirming!" : "Sorry to see you go.");
            window.location.href = "index.html";
        });
    }
});
