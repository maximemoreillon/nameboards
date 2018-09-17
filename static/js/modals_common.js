function close_modals() {

  document.getElementById("arrival_edit_modal").style.display = "none";
  document.getElementById("location_edit_modal").style.display = "none";
}


window.onclick = function(event) {
  // Close modal if clicked somewhere else


  var arrival_edit_modal = document.getElementById("arrival_edit_modal");
  var location_edit_modal = document.getElementById("location_edit_modal")

  if (event.target == arrival_edit_modal || event.target == location_edit_modal) {
    arrival_edit_modal.style.display = "none";
    location_edit_modal.style.display = "none";
  }
}
