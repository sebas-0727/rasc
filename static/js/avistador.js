document.addEventListener('DOMContentLoaded', function() {
    const registroForm = document.getElementById('registroForm');

    registroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        registrarAvistador();
    });

    async function registrarAvistador() {
        const nombres = document.getElementById('nombres').value;
        const ficha = document.getElementById('ficha').value;
        const correo = document.getElementById('correo').value;

        try {
            const response = await fetch('/registrar_avistador', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nombres, ficha, correo }),
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const data = await response.json();
                if (data.error) {
                    console.error('Error:', data.error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Failed to register avistador. Please try again.',
                    });
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Avistador registered successfully!',
                    });
                }
            }
        } catch (error) {
            console.error('Error en registrarAvistador:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'An error occurred. Please try again later.',
            });
        }
    }
});
