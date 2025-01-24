function showMainPage() {
    document.getElementById('mainpage-btn').classList.add('active');
    document.getElementById('accpage-btn').classList.remove('active');
    document.getElementById('main-content').style.display = 'block';
    document.getElementById('account-content').style.display = 'none';
}

function showAccountPage() {
    document.getElementById('accpage-btn').classList.add('active');
    document.getElementById('mainpage-btn').classList.remove('active');
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('account-content').style.display = 'block';
}

function saveProfile(event) {
    event.preventDefault();
    // Add your save profile logic here
    alert('Profile changes saved successfully!');
}

//change password here

function showDeleteConfirmation() {
    document.getElementById('delete-modal').style.display = 'block';
}

function hideDeleteConfirmation() {
    document.getElementById('delete-modal').style.display = 'none';
}

function deleteAccount() {
    // Add your delete account logic here
    alert('Account deleted successfully!');
    hideDeleteConfirmation();
}

function logOut() {
    // Send a request to the logout route
    fetch('/logout')
        .then(response => {
            // Redirect to the main page
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Logout error:', error);
            alert('An error occurred during logout');
        });
}

// Close modal if clicked outside
window.onclick = function(event) {
    const modal = document.getElementById('delete-modal');
    if (event.target === modal) {
        hideDeleteConfirmation();
    }
}

function showRandoms(){
    document.getElementById('Randoms').classList.add('active');
    document.getElementById('Favorites').classList.remove('active')
    document.getElementById('rands').style.display = 'grid'
    document.getElementById('favs').style.display = 'none'
}

function showFavorites(){
    document.getElementById('Favorites').classList.add('active');
    document.getElementById('Randoms').classList.remove('active');
    document.getElementById('favs').style.display = 'grid';
    document.getElementById('rands').style.display = 'none'
}

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages
    const alerts = document.querySelectorAll('.alert');
    
    // Log number of alerts found (helps with debugging)
    console.log(`Number of alerts found: ${alerts.length}`);
    
    alerts.forEach(alert => {
        // Automatically hide alerts after 5 seconds
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });

    // Add close button functionality to dismiss alerts
    const closeButtons = document.querySelectorAll('.alert .close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').style.display = 'none';
        });
    });
});