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

function changePassword(event) {
    event.preventDefault();
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (newPassword !== confirmPassword) {
        alert('New passwords do not match!');
        return;
    }
    
    // Add your password change logic here
    alert('Password updated successfully!');
    document.getElementById('password-form').reset();
}

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
    // Add your logout logic here
    alert('Logged out successfully!');
}

// Close modal if clicked outside
window.onclick = function(event) {
    const modal = document.getElementById('delete-modal');
    if (event.target === modal) {
        hideDeleteConfirmation();
    }
}