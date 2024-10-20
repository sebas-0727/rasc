$(document).ready(function () {
    const cargarEspecies = () => {
        $.ajax({
            url: '/especies',
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log('Datos de especies recibidos:', data);

                const especiesHtml = `
                    <div class="card">
                        <div class="card-header" id="headingEspecies">
                            <h5 class="mb-0">
                                <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseEspecies" aria-expanded="true" aria-controls="collapseEspecies">
                                    Seleccionar especie en común 
                                </button>
                            </h5>
                        </div>

                        <div id="collapseEspecies" class="collapse show" aria-labelledby="headingEspecies" data-parent="#acordeonEspecies">
                            <div class="card-body">
                                <div class="row">
                                    ${data.map(especie => `
                                        <div class="col-md-3 mb-3 text-center">
                                            <img src="data:image/png;base64,${especie.imagen}" alt="${especie.nombre}" class="img-thumbnail especie-img" data-especie-id="${especie.numero}">
                                            <p class="mt-2">${especie.nombre}</p>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                $('#acordeonEspecies').html(especiesHtml);

                $('.especie-img').click(function () {
                    const especieId = $(this).data('especie-id');

                    if ($(this).hasClass('selected')) {
                        $(this).removeClass('selected');
                        $('#especieSeleccionada').val('');
                    } else {
                        $('.especie-img').removeClass('selected');
                        $(this).addClass('selected');
                        $('#especieSeleccionada').val(especieId);
                    }

                    console.log('Especie seleccionada:', especieId || 'Ninguna');
                });
            },
            error: function (_xhr, status, error) {
                console.error('Error al obtener especies:', status, error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error loading species. Please try again later.',
                });
            }
        });
    };

    $('#formularioReporte').submit(function (e) {
        e.preventDefault();
        var formData = new FormData(this);

        const especieSeleccionada = $('#especieSeleccionada').val();
        formData.append('rep_especie_id', especieSeleccionada);

        console.log('Datos del formulario a enviar:', Object.fromEntries(formData));

        $.ajax({
            url: '/registrar_reporte',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log('Reporte registrado con éxito:', response);
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Report successfully registered!',
                });
                $('#formularioReporte')[0].reset();
                $('#imagenPreview').hide();
                $('.especie-img').removeClass('selected');
                $('#especieSeleccionada').val('');
            },
            error: function (_xhr, status, error) {
                console.error('Error al registrar el reporte:', status, error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error registering the report. Check the console for details.',
                });
            }
        });
    });

    // Manejar la selección de archivo para la imagen
    $('#imagen').change(function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                $('#imagenPreview').attr('src', e.target.result).fadeIn(500); // Animación de entrada
            };
            reader.readAsDataURL(file);
        } else {
            $('#imagenPreview').hide();
        }
    });

    // Cargar especies al iniciar
    cargarEspecies();

    // Actualizar datos cada 5 minutos (300000 ms)
    setInterval(cargarEspecies, 300000);
});
