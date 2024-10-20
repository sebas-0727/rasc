document.addEventListener('DOMContentLoaded', function () {
    // Manejo del formulario de registro SIGA
    const sigaForm = document.getElementById('sigaForm');
    sigaForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(sigaForm);
        const data = Object.fromEntries(formData);

        fetch('/registrar_siga', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else if (data.mensaje) {
                Swal.fire({
                    icon: 'info',
                    title: data.mensaje,
                    showConfirmButton: false,
                    timer: 5000
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error al registrar SIGA',
                text: 'Ha ocurrido un error. Por favor, inténtalo nuevamente.',
                showConfirmButton: true
            });
        });
    });

    // Manejo del formulario de inicio de sesión
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const nombre = document.getElementById('loginNombre').value;
        const contraseña = document.getElementById('loginContraseña').value;

        fetch('/iniciar_sesion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nombre, contraseña })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje === 'Inicio de sesión exitoso') {
                Swal.fire({
                    icon: 'success',
                    title: 'Acceso permitido. Bienvenido!',
                    showConfirmButton: false,
                    timer: 3000
                }).then(() => {
                    window.location.href = '/reptiles';
                });
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Error',
                    text: data.mensaje,
                    showConfirmButton: true
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error al iniciar sesión',
                text: 'Ha ocurrido un error. Por favor, inténtalo nuevamente.',
                showConfirmButton: true
            });
        });
    });

    // Configuración de los botones para mostrar/ocultar las contraseñas
    const toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = this.previousElementSibling;
            const toggleIcon = this.querySelector('i');
            togglePassword(passwordField, toggleIcon);
        });
    });
});

function togglePassword(passwordField, toggleIcon) {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    }
}
