function select_group() {
  var select_group_name_input = document.getElementById("select_group_name_input");
  var group_select = document.getElementById("group_select");
  var select_group_form = document.getElementById("select_group_form");

  select_group_name_input.value = group_select.value;
  select_group_form.submit();
}

function submit_create_group_form(){
  var create_group_form = document.getElementById("create_group_form");
  create_group_form.submit();
}

function open_create_group_modal(cell) {

  var create_group_modal = document.getElementById("create_group_modal");

  create_group_modal.style.display = "block";
}

function open_delete_group_modal(cell) {

  var delete_group_modal = document.getElementById("delete_group_modal");
  var delete_group_name_input = document.getElementById("delete_group_name_input");
  var group_select = document.getElementById("group_select");

  delete_group_name_input.value = group_select.value;

  delete_group_modal.style.display = "block";
}

function submit_delete_group_form() {

  var delete_group_form = document.getElementById("delete_group_form");
  delete_group_form.submit();
}



// Closign modals
function close_modals() {

  document.getElementById("create_group_modal").style.display = "none";
  document.getElementById("delete_group_modal").style.display = "none";
}

window.onclick = function(event) {
  // Close modal if clicked somewhere else

  var delete_group_modal = document.getElementById("delete_group_modal");
  var create_group_modal = document.getElementById("create_group_modal")

  if (event.target == delete_group_modal || event.target == create_group_modal) {
    delete_group_modal.style.display = "none";
    create_group_modal.style.display = "none";
  }
}
