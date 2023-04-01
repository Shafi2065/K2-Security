document.querySelector('form').addEventListener('submit', function(event) {
  var usernameInput = document.querySelector('#username');
  var usernameValue = usernameInput.value;
  var passwordInput = document.querySelector('#password');
  var passwordValue = passwordInput.value;
  var invalidFeedback = document.querySelector('.invalid-feedback');
  
  // Check if username contains "@"
  if (!usernameValue.includes('@')) {
    invalidFeedback.innerText = 'Must include "@" symbol';
    alert('Invalid email address. Please enter an email address containing "@"');
    usernameInput.classList.add('is-invalid');
    event.preventDefault();
    return;
  }

  // Check if anything is entered after "@"
  var emailParts = usernameValue.split('@');
  if (emailParts[1].length === 0) {
    invalidFeedback.innerText = 'Please enter a valid email address';
    usernameInput.classList.add('is-invalid');
    alert('Invalid email address. Please enter characters after "@"');
    event.preventDefault();
    return;
  }

  // Check password for minimum requirements
  var hasCapital = /[A-Z]/.test(passwordValue);
  var hasNumber = /\d/.test(passwordValue);
  var hasSpecial = /[\W_]/.test(passwordValue);
  var hasLength = passwordValue.length >= 8;

  if (!hasCapital || !hasNumber || !hasSpecial || !hasLength) {
    invalidFeedback.innerText = 'Password must contain at least 8 characters with 1 capital letter, 1 special symbol, and a mix of letters and numbers';
    passwordInput.classList.add('is-invalid');
    alert('Invalid password. Please enter a password with at least 8 characters, 1 capital letter, 1 special symbol, and a mix of letters and numbers');
    event.preventDefault();
    return;
  }

  // Remove validation errors if present
  else {
    invalidFeedback.innerText = '';
    usernameInput.classList.remove('is-invalid');
    passwordInput.classList.remove('is-invalid');
  }
});
