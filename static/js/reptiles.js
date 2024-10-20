document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('reptilForm');
    const consultaForm = document.getElementById('consultaForm');
    const reptilesTable = document.getElementById('reptilesTable').getElementsByTagName('tbody')[0];
    const reptilDetalle = document.getElementById('reptilDetalle');
    const imagenInput = document.getElementById('imagen');

    function mostrarAlerta(mensaje, tipo) {
        Swal.fire({
            icon: tipo,
            title: mensaje,
            showConfirmButton: false,
            timer: 5000 // Ocultar alerta después de 5 segundos
        });
    }

    async function actualizarTablaReptiles() {
        try {
            const response = await fetch('/reptiles/lista');
            const reptiles = await response.json();
            reptilesTable.innerHTML = ''; // Limpiar tabla antes de agregar filas
            reptiles.forEach(reptil => {
                const row = reptilesTable.insertRow();
                row.insertCell().textContent = reptil.nombre_cientifico;
                row.insertCell().textContent = reptil.nombre;
                row.insertCell().textContent = reptil.veneno;

                // Mostrar imagen
                const imgCell = row.insertCell();
                if (reptil.imagen) {
                    const img = document.createElement('img');
                    img.src = `data:image/png;base64,${reptil.imagen}`;
                    img.style.maxWidth = '150px';
                    imgCell.appendChild(img);
                } else {
                    imgCell.textContent = 'Sin imagen';
                }

                // Botón de eliminar
                const eliminarBtn = document.createElement('button');
                eliminarBtn.textContent = 'Eliminar';
                eliminarBtn.className = 'btn btn-danger btn-sm';
                eliminarBtn.addEventListener('click', () => eliminarReptil(reptil.nombre_cientifico));
                row.insertCell().appendChild(eliminarBtn);
            });
        } catch (error) {
            console.error('Error:', error);
            mostrarAlerta('Error al cargar la lista de reptiles.', 'error');
        }
    }

    async function eliminarReptil(nombreCientifico) {
        try {
            const response = await fetch(`/reptiles/nombre/${nombreCientifico}`, {
                method: 'DELETE'
            });
            const result = await response.json();
            if (response.ok) {
                mostrarAlerta(result.mensaje, 'success');
                actualizarTablaReptiles(); // Actualizar la tabla después de eliminar
            } else {
                mostrarAlerta(result.mensaje, 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarAlerta('Error al eliminar el reptil.', 'error');
        }
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        const nombreCientifico = document.getElementById('nombre_cientifico').value;
        const nombre = document.getElementById('nombre').value;
        const veneno = document.getElementById('veneno').value;

        // Leer imagen y convertir a Base64
        let imagenBase64 = '';
        if (imagenInput.files.length > 0) {
            const file = imagenInput.files[0];
            const reader = new FileReader();
            reader.onloadend = function () {
                imagenBase64 = reader.result.split(',')[1]; // Eliminar el prefijo "data:image/png;base64,"
                enviarDatos();
            };
            reader.readAsDataURL(file);
        } else {
            enviarDatos();
        }

        function enviarDatos() {
            const data = {
                nombre_cientifico: nombreCientifico,
                nombre: nombre,
                veneno: veneno,
                imagen: imagenBase64
            };

            fetch('/registro_reptil', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.mensaje === 'Reptil agregado correctamente') {
                    mostrarAlerta(result.mensaje, 'success');
                    form.reset(); // Limpiar el formulario
                    actualizarTablaReptiles(); // Actualizar la tabla después de agregar
                } else {
                    mostrarAlerta(result.mensaje, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                mostrarAlerta('Error al agregar el reptil.', 'error');
            });
        }
    });

    consultaForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Evitar el envío tradicional del formulario

        const nombreCientifico = document.getElementById('consulta_nombre_cientifico').value;

        try {
            const response = await fetch(`/reptiles/nombre/${nombreCientifico}`);
            const result = await response.json();
            if (response.ok) {
                reptilDetalle.innerHTML = `
                    <h3>Detalles del Reptil</h3>
                    <p><strong>Nombre Científico:</strong> ${result.nombre_cientifico}</p>
                    <p><strong>Nombre:</strong> ${result.nombre}</p>
                    <p><strong>Veneno:</strong> ${result.veneno}</p>
                    <p><strong>Imagen:</strong></p>
                    ${result.imagen ? `<img src="data:image/png;base64,${result.imagen}" style="max-width: 300px;">` : 'Sin imagen'}
                `;
                mostrarAlerta('Reptil encontrado.', 'success');
            } else {
                reptilDetalle.innerHTML = '';
                mostrarAlerta('Reptil no encontrado.', 'warning');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarAlerta('Error al consultar el reptil.', 'error');
        }
    });

    // Cargar la lista de reptiles al cargar la página
    actualizarTablaReptiles();
});
