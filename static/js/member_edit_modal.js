function open_member_edit_modal(cell) {

  var modal = document.getElementById("member_edit_modal");
  var member_name_input = document.getElementById("member_name_input");
  var member_id_input = document.getElementById("member_id_input");

  modal.style.display = "block";

  member_name_input.value = cell.innerText;
  member_id_input.value = cell.parentNode.id;

}


function close_member_edit_modal() {
  var modal = document.getElementById("member_edit_modal");
  modal.style.display = "none";
}


window.onclick = function(event) {
  // Close modal if clicked somewhere else

  var modal = document.getElementById("member_edit_modal");

  if (event.target == modal) {
    modal.style.display = "none";
  }
}
