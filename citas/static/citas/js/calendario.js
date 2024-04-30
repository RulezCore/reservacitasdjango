// Obtener elementos del DOM
window.onload = () => {
  const calendarContainer = document.getElementById('calendar-container');
  const openCalendarButton = document.getElementById('openCalendarButton');
  const selectedDateInput = document.getElementById('selectedDateInput');
  const selectedHourInput = document.getElementById('selectedHourInput');
  const selectedDateLabel = document.getElementById('selectedDate');
  const hourSelector = document.getElementById('hourSelector');
  const citaForm = document.getElementById('citaForm');

    // Variables para la fecha y hora seleccionadas
  let selectedDate = null;
  let selectedHour = null;

  // // Función para crear el calendario
  // function createCalendar(year, month) {
  //     // ... (implementar la lógica para crear el calendario como en el ejemplo anterior)
  // }

  // // Función para mostrar el calendario
  // function showCalendar() {
  //     // ... (implementar la lógica para mostrar el calendario en el contenedor)
  // }

  // // Función para deshabilitar sábados y domingos
  // function disableWeekends(calendarDays) {
  //     calendarDays.forEach(day => {
  //         const dayNumber = parseInt(day.textContent);
  //         if (dayNumber === 6 || dayNumber === 0) {
  //             day.classList.add('disabled');
  //             day.style.cursor = 'not-allowed';
  //             day.addEventListener('click', () => {
  //                 alert('No se pueden seleccionar sábados ni domingos.');
  //             });
  //         }
  //     });
  // }

  // // Función para seleccionar un día
  // function selectDay(dayNumber) {
  //     // ... (implementar la lógica para seleccionar el día, actualizar la fecha seleccionada y la interfaz)
  // }

  // // Función para mostrar el selector de horas
  // function showHourSelector(selectedDate) {
  //     // ... (implementar la lógica para consultar y mostrar las horas disponibles para la fecha seleccionada)
  // }

  // // Función para seleccionar una hora
  // function selectHour(selectedHour) {
  //     // ... (implementar la lógica para seleccionar la hora, actualizar la hora seleccionada y la interfaz)
  // }

  // // Evento para abrir el calendario
  // openCalendarButton.addEventListener('click', () => {
  //     showCalendar();
  // });

  // // Evento para seleccionar un día en el calendario
  // calendarContainer.addEventListener('click', (event) => {
  //     const clickedElement = event.target;
  //     if (clickedElement.classList.contains('calendar-day') && !clickedElement.classList.contains('disabled')) {
  //         const dayNumber = parseInt(clickedElement.textContent);
  //         selectDay(dayNumber);
  //     }
  // });

  // // Evento para cambiar la hora seleccionada
  // hourSelector.addEventListener('change', () => {
  //     selectedHour = hourSelector.value;
  //     selectedHourInput.value = selectedHour;
  //     updateSelectedDateTimeLabel();
  // });

  // // Evento para enviar el formulario
  // citaForm.addEventListener('submit', (event) => {
  //     event.preventDefault();

  //     if (selectedDate && selectedHour) {
  //         // Validar datos adicionales del formulario si es necesario
  //         // ...

  //         // Enviar los datos del formulario (implementar la lógica para enviar los datos)
  //         // ...

  //         // Mostrar mensaje de éxito
  //         alert('Cita solicitada correctamente.');

  //         // Limpiar la selección de fecha y hora
  //         selectedDate = null;
  //         selectedHour = null;
  //         selectedDateInput.value = '';
  //         selectedHourInput.value = '';
  //         updateSelectedDateTimeLabel();
  //         hourSelector.options.length = 0;
  //         calendarContainer.innerHTML = ''; // Limpiar el calendario
  //     } else {
  //         alert('Por favor, seleccione una fecha y hora.');
  //     }
  // });

  // // Función para actualizar la etiqueta de fecha y hora seleccionadas
  // function updateSelectedDateTimeLabel() {
  //     if (selectedDate && selectedHour) {
  //         const formattedDate = formatDate(selectedDate);
  //         selectedDateLabel.textContent = `${formattedDate} a las ${selectedHour}`;
  //     } else {
  //         selectedDateLabel.textContent = '';
  //     }
  // }

  // // Inicializar el calendario al cargar la página
  // createCalendar(new Date().getFullYear(), new Date().getMonth());

  // // Funciones de formato de fecha y hora (implementarlas según tus necesidades)
  // function formatDate(date) {
  //     // ...
  // }

  // function formatTime(hour) {
  //     // ...
  // }

  openCalendarButton.addEventListener('click', (event) => {
    // Prevenir el envío del formulario
    event.preventDefault();
    console.log('boton');

    // Implementar la lógica para abrir el calendario
    showCalendar(); // Ejemplo de función para mostrar el calendario
  });

};


