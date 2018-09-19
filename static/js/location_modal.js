function open_location_edit_modal(cell) {

  var modal = document.getElementById("location_edit_modal");
  var location_input = document.getElementById("location_input");
  var location_id_input = document.getElementById("location_id_input");

  //location_input.value=cell.innerText;
  location_id_input.value=cell.parentNode.id;

  modal.style.display = "block";
}

function submit_location() {

  // Get the various elements
  var modal = document.getElementById("location_edit_modal");
  var location_input = document.getElementById("location_input");
  var location_id_input = document.getElementById("location_id_input");

  // Fill the input with the current value
  modal.style.display = "block";


  // Create a JSON message and send it through WS
  JSON_message = {};

  JSON_message.id = location_id_input.value;
  JSON_message.location = location_input.value;

  socket.emit('update_member', JSON_message);

  // close the modal
  modal.style.display = "none";
}

function submit_location_enter() {
  if(event.key === 'Enter') {
    submit_location();
  }
}
