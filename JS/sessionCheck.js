function checkSession() {
    const session = document.cookie.split('; ').find(row => row.startsWith('session_id='));
    const user = document.cookie.split('; ').find(row => row.startsWith('user_id='));

    if (session && user) {
        document.getElementById('loginBtn').style.display = 'none';
        document.getElementById('registerBtn').style.display = 'none';
        document.getElementById('logoutBtn').style.display = 'inline-block';
    } else {
        document.getElementById('loginBtn').style.display = 'inline-block';
        document.getElementById('registerBtn').style.display = 'inline-block';
        document.getElementById('logoutBtn').style.display = 'none';
    }
}

window.onload = checkSession;
