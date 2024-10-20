document.addEventListener('DOMContentLoaded', function() {
    const resultadosSIGA = document.getElementById('resultadosSIGA');
    const resultadosAvistadores = document.getElementById('resultadosAvistadores');
    const resultadosReportes = document.getElementById('resultadosReportes');

    function cargarRegistrosSIGA() {
        fetch('/siga_general')
        .then(response => response.json())
        .then(data => {
            if (data.siga && data.siga.length > 0) {
                let html = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre</th><th>Correo</th><th>Contraseña</th><th>Función</th><th>Ubicación</th><th>Activo</th></tr></thead><tbody>';
                data.siga.forEach(siga => {
                    const isActivo = Boolean(siga.activo);
                    const activoButton = `<button class="btn ${isActivo ? 'btn-success' : 'btn-secondary'} btn-sm" onclick="toggleActivo(${siga.id}, ${!isActivo}, this)">${isActivo ? 'Sí' : 'No'}</button>`;
                    html += `<tr>
                        <td>${siga.id}</td>
                        <td>${siga.nombre}</td>
                        <td>${siga.correo}</td>
                        <td>${siga.contraseña}</td>
                        <td>${siga.funcion}</td>
                        <td>${siga.u_asignado}</td>
                        <td>${activoButton}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                resultadosSIGA.innerHTML = html;
            } else {
                resultadosSIGA.innerHTML = '<p class="text-muted">No se encontraron registros SIGA.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultadosSIGA.innerHTML = '<p class="text-danger">Error al consultar los datos SIGA</p>';
        });
    }

    function cargarAvistadores() {
        fetch('/avistador_general')
        .then(response => response.json())
        .then(data => {
            if (data.avistadores && data.avistadores.length > 0) {
                let html = '<table class="table table-striped"><thead><tr><th>ID</th><th>Nombre Completo</th><th>Ficha</th><th>Correo</th><th>Avistamientos</th><th>Acciones</th></tr></thead><tbody>';
                data.avistadores.forEach(avistador => {
                    html += `<tr>
                        <td>${avistador.id}</td>
                        <td>${avistador.nombres}</td>
                        <td>${avistador.ficha}</td>
                        <td>${avistador.correo}</td>
                        <td>${avistador.conteo}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="eliminarAvistador(${avistador.id})">Eliminar</button>
                        </td>
                    </tr>`;
                });
                html += '</tbody></table>';
                resultadosAvistadores.innerHTML = html;
            } else {
                resultadosAvistadores.innerHTML = '<p class="text-muted">No se encontraron avistadores registrados.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultadosAvistadores.innerHTML = '<p class="text-danger">Error al consultar los datos de avistadores</p>';
        });
    }

    function cargarReportes() {
        fetch('/reportes_general')
        .then(response => response.json())
        .then(data => {
            if (data.reportes && data.reportes.length > 0) {
                let html = '<table class="table table-striped"><thead><tr><th>Zona</th><th>Hora</th><th>Reptil_Especie</th><th>Atacó</th><th>Imagen_Reporte</th><th>Observaciones</th></tr></thead><tbody>';
                data.reportes.forEach(reporte => {
                    const especieImagen = reporte.especie_imagen ? `<img src="data:image/jpeg;base64,${reporte.especie_imagen}" alt="Especie" style="max-width: 100px; max-height: 100px;">` : 'No disponible';
                    const reporteImagen = reporte.imagen ? `<img src="data:image/jpeg;base64,${reporte.imagen}" alt="Reporte" style="max-width: 100px; max-height: 100px;">` : 'No disponible';
                    html += `<tr>
                        <td>${reporte.zona}</td>
                        <td>${reporte.hora}</td>
                        <td>${especieImagen}</td>
                        <td>${reporte.ataco}</td>
                        <td>${reporteImagen}</td>
                        <td>${reporte.observaciones}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                resultadosReportes.innerHTML = html;
            } else {
                resultadosReportes.innerHTML = '<p class="text-muted">No se encontraron reportes.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultadosReportes.innerHTML = '<p class="text-danger">Error al consultar los datos de reportes</p>';
        });
    }

    window.toggleActivo = function(id, nuevoEstado, boton) {
        fetch(`/actualizar_activo/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ activo: nuevoEstado ? 1 : 0 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje === 'Estado de activo actualizado correctamente') {
                boton.textContent = nuevoEstado ? 'Sí' : 'No';
                boton.className = `btn ${nuevoEstado ? 'btn-success' : 'btn-secondary'} btn-sm`;
                boton.onclick = () => toggleActivo(id, !nuevoEstado, boton);
                
                Swal.fire({
                    icon: 'success',
                    title: nuevoEstado ? 'Usuario activado' : 'Usuario desactivado',
                    showConfirmButton: false,
                    timer: 1500
                });
                cargarRegistrosSIGA();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    window.eliminarAvistador = function(id) {
        Swal.fire({
            title: '¿Está seguro de que desea eliminar este avistador?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/eliminar_avistador/${id}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    Swal.fire({
                        icon: 'success',
                        title: data.mensaje,
                        showConfirmButton: false,
                        timer: 1500
                    });
                    cargarAvistadores();
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }

    // Cargar datos iniciales
    cargarRegistrosSIGA();
    cargarAvistadores();
    cargarReportes();

    // Actualizar datos cada 5 minutos (300000 ms) para reducir la carga
    setInterval(cargarRegistrosSIGA, 300000);
    setInterval(cargarAvistadores, 300000);
    setInterval(cargarReportes, 300000);
});
