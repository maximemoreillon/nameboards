function toggle_presence(cell) {

  var row = cell.parentNode;
  var member_id = row.id;

  // Not supported by IE5
  //var presence = row.getElementsByClassName("presence_cell")[0].innerText;
  var presence = row.cells[3].innerText;

  JSON_message = {};

  JSON_message.id = member_id;
  JSON_message.presence = 1-presence;

  socket.emit('update_member', JSON_message);
}
