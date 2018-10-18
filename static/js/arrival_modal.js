function open_arrival_edit_modal(cell) {

  var modal = document.getElementById("arrival_edit_modal");
  var arrival_input = document.getElementById("arrival_input");
  var arrival_id_input = document.getElementById("arrival_id_input");

  // Fill the modal with the appropriate info
  arrival_input.value=cell.innerText;
  arrival_id_input.value=cell.parentNode.id;

  // Actually show the modal
  modal.style.display = "block";
}

function submit_arrival() {

  // Get the various elements
  var modal = document.getElementById("arrival_edit_modal");
  var arrival_input = document.getElementById("arrival_input");
  var arrival_id_input = document.getElementById("arrival_id_input");

  // Create a JSON message and send it through WS
  JSON_message = {};
  JSON_message.id = arrival_id_input.value;
  JSON_message.arrival = arrival_input.value;
  socket.emit('update_member', JSON_message);

  // close the modal
  modal.style.display = "none";
}

function submit_arrival_enter() {
  if(event.key === 'Enter') {
    submit_arrival();
  }
}
