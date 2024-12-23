// Validation for Sign-Up Form
function validateSignUp(event) {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if (!email.includes("@")) {
        alert("Invalid email address!");
        event.preventDefault();
    }
    if (password.length < 6) {
        alert("Password must be at least 6 characters!");
        event.preventDefault();
    }
}
document.querySelector("form")?.addEventListener("submit", validateSignUp);

function addToCart(bookId) {
    fetch('/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: bookId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success message
        location.reload(); // Reload the page to update cart information
    })
    .catch(error => console.error('Error:', error));
}

