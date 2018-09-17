var socket = io.connect('http://' + document.domain + ':' + location.port);


socket.on('connect', function() {

  var disconnected_modal = document.getElementById('disconnected_modal');
  if(disconnected_modal !== null){
    disconnected_modal.style.display="none";
  }
});

socket.on('disconnect', function(){
  var disconnected_modal = document.getElementById('disconnected_modal');
  if(disconnected_modal !== null){
    disconnected_modal.style.display="block";
  }
});


socket.on('update_member', function (JSON_message) {

  member_id = JSON_message.id;
  member_presence = JSON_message.presence;
  member_location = JSON_message.location;
  member_arrival = JSON_message.arrival;
  member_name = JSON_message.member_name;

  // There should be a more elegant way to find the right row
  var row = document.getElementById(member_id);

  // Check if ID is actually within the table
  if (row !== null) {

    // This does not work in old IE browsers
    //var member_name_cell = row.getElementsByClassName("member_name_cell")[0];
    //var presence_cell = row.getElementsByClassName("presence_cell")[0];
    //var arrival_cell = row.getElementsByClassName("arrival_cell")[0];
    //var location_cell = row.getElementsByClassName("location_cell")[0];

    var arrival_cell = row.cells[0];
    var member_name_cell = row.cells[1];
    var location_cell = row.cells[2];
    var presence_cell = row.cells[3];

    // Deal with presence
    if (typeof member_presence !== 'undefined') {
      presence_cell.innerText = member_presence;

      // Not very elegant
      if(member_presence == 1) {
        member_name_cell.className = "member_name_cell";
      }
      else if(member_presence == 0){
        member_name_cell.className = "member_name_cell absent";
      }
    }

    if (typeof member_arrival !== 'undefined') {
      arrival_cell.innerText = member_arrival;
    }

    if (typeof member_location !== 'undefined') {
      location_cell.innerText = member_location;
    }

    if (typeof member_name !== 'undefined') {
      member_name_cell.innerText = member_name;
    }
  }
});


socket.on('refresh', function (JSON_message) {
  location.reload();
});
