// Check for a valid session
function checkSession() {
    // Example: Get the session from cookies or localStorage
    const session = document.cookie.split('; ').find(row => row.startsWith('session='));
    
    if (session) {
        // If a valid session is found, hide login/register buttons and show the logout button
        document.getElementById('loginBtn').style.display = 'none';
        document.getElementById('registerBtn').style.display = 'none';
        document.getElementById('logoutBtn').style.display = 'inline-block';
    } else {
        // If no valid session, show login/register and hide logout
        document.getElementById('loginBtn').style.display = 'inline-block';
        document.getElementById('registerBtn').style.display = 'inline-block';
        document.getElementById('logoutBtn').style.display = 'none';
    }
}

// Run the session check when the page loads
window.onload = checkSession;