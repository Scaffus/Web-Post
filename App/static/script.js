document.getElementById('register').onclick = function checkPasswords() {
    let password = document.getElementById('password').innerHTML
    let repeated_password = document.getElementById('repeatPassword').innerHTML
    alert(password, repeated_password)
}