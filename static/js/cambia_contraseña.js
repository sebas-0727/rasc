document.addEventListener('DOMContentLoaded', function() {
    const cambiarContraseñaForm = document.getElementById('cambiarContraseñaForm');

    if (cambiarContraseñaForm) {
        cambiarContraseñaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            actualizarContraseña();
        });
    }
});

function actualizarContraseña() {
    const correo = document.getElementById('correoActualizar').value;
    const nuevaContraseña = document.getElementById('nuevaContraseña').value;

    if (correo && nuevaContraseña) {
        fetch('/cambiar_contraseña', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                correo: correo,
                nueva_contraseña: nuevaContraseña
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                if (data.mensaje === 'Contraseña actualizada correctamente') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Password updated successfully!',
                        timer: 2000,
                        showConfirmButton: false
                    }).then(() => {
                        window.location.href = '/inicio_siga';
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: data.mensaje,
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error changing password. Please try again later.',
            });
        });
    } else {
        Swal.fire({
            icon: 'warning',
            title: 'Warning',
            text: 'Please fill in all the fields!',
        });
    }
}
