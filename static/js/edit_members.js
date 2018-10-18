function open_member_edit_modal(id) {

  var modal = document.getElementById("member_edit_modal");

  var member_name_input = document.getElementById("member_name_input");
  var member_id_input = document.getElementById("member_id_input");
  var delete_member_id_input = document.getElementById("delete_member_id_input");

  var row = document.getElementById(id);

  member_name_input.value = row.cells[0].innerText;
  member_id_input.value = id;
  delete_member_id_input.value = id;

  modal.style.display = "block";

}

function submit_edit_member_form(){
  var edit_member_form = document.getElementById("edit_member_form");
  edit_member_form.submit();
}

function submit_delete_member_form(id) {
  var delete_member_form = document.getElementById("delete_member_form");
  delete_member_form.submit();
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
