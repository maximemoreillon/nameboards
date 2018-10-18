from flask import Flask, session, redirect, url_for, escape, request, render_template
from flaskext.mysql import MySQL
from flask_socketio import SocketIO, send, emit
import json
import credentials
import sys

# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Websockets config
socketio = SocketIO(app)

# MySQL config
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = credentials.MySQL_username
app.config['MYSQL_DATABASE_PASSWORD'] = credentials.MySQL_password
app.config['MYSQL_DATABASE_DB'] = 'nameboards'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


################
# HTTP routing #
################

@app.route('/')
def index():
    if 'group_name' in session:

        # Group name is gotten from session
        group_name = session['group_name']

        # Query to get all members
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM nameboards WHERE group_name=%s""", group_name)
        members = cursor.fetchall()

        cursor.close()
        conn.close()


        # Provide an option for wall mounted displays (board)
        display_style = "desktop"
        if 'board' in request.args:
            display_style = "board"

        return render_template('show_members.html', display_style=display_style, group_name=group_name, members=members)

    else:
        # If the group is not selected, redirect to group selection
        return redirect(url_for('select_group'))


@app.route('/select_group', methods=['POST', 'GET'])
def select_group():
    if request.method == 'POST':
        # The group has been chosen and now set as session variable
        session['group_name'] = request.form['group_name']

        return redirect(url_for('index'))
    else:
        # The group hasn't been chosen
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT group_name FROM nameboards""")
        group_names = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('select_group.html', group_names=group_names )


@app.route('/delete_group', methods=['POST', 'GET'])
def delete_group():

    if request.method == 'POST':

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM nameboards WHERE group_name=%s""", request.form['group_name'])
        conn.commit()
        cursor.close()
        conn.close()

    # No matter what, return to group selection
    return redirect(url_for('select_group'))


@app.route('/edit_members', methods=['GET'])
def edit_members():
    if 'group_name' in session:
        group_name = session['group_name']

        # Query all members
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM nameboards WHERE group_name=%s""", group_name)
        members = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('edit_members.html', group_name=group_name, members=members)
    else:
        # If session not set, go to select group page
        return redirect(url_for('select_group'))


@app.route('/add_member', methods=['GET'])
def add_member():
    if 'group_name' in session:
        group_name = session['group_name']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO nameboards (member_name, group_name, presence) VALUES ('Unnamed member', '%s', 0)""", group_name)
        conn.commit()

        cursor.close()
        conn.close()

        # Sending an empty message to tell clients to refresh
        # TODO: Refresh only the correct group
        JSON_message = {}
        socketio.emit('refresh', JSON_message, broadcast=True)

        # The redirect will be in GET request
        return redirect(url_for('edit_members'))
    else:
        # If session not set, go to select group page
        return redirect(url_for('select_group'))


@app.route('/delete_member', methods=['POST'])
def delete_member():
    if 'group_name' in session:
        group_name = session['group_name']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""DELETE FROM nameboards WHERE id=%s""", request.form['id'] )
        conn.commit()

        cursor.close()
        conn.close()

        # Sending an empty message to tell clients to refresh
        # TODO: Refresh only the correct group
        JSON_message = {}
        socketio.emit('refresh', JSON_message, broadcast=True)

        # The redirect will be in GET request
        return redirect(url_for('edit_members'))

    else:
        # If session not set, go to select group page
        return redirect(url_for('select_group'))


@app.route('/edit_member', methods=['POST'])
def edit_member():

    # Todo: There should be a WS method for this too

    if 'group_name' in session:
        group_name = session['group_name']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""UPDATE nameboards SET member_name=%s WHERE id=%s""", (request.form['member_name'], request.form['id']) )
        conn.commit()

        cursor.close()
        conn.close()

        # Update all clients through WS
        JSON_message = {}
        JSON_message['id'] = request.form['id']
        JSON_message['member_name'] = request.form['member_name']
        socketio.emit('update_member', JSON_message, broadcast=True)

        # The redirect will be in GET request
        return redirect(url_for('edit_members'))

    else:
        # If session not set, go to select group page
        return redirect(url_for('select_group'))

@app.route('/update_presence', methods=['GET'])
def update_presence():

    # This is the API, toggles the state of someone through HTTP request

    #TODO Input sanitation

    # Read the request
    member_name = request.args['member_name']
    group_name = request.args['group_name']
    presence = request.args['presence']

    # Update the DB according to the request
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("""UPDATE nameboards SET presence=%s WHERE member_name=%s AND group_name=%s""", (presence, member_name, group_name))
    conn.commit()

    # Get the ID of the members that have been updated
    cursor.execute("""SELECT id FROM nameboards WHERE group_name=%s AND member_name=%s""", (group_name, member_name))
    member_ids = cursor.fetchall()

    cursor.close()
    conn.close()

    # Update all clients using WS
    for member_id in member_ids:
        JSON_message = {}
        JSON_message['id'] = member_id[0]
        JSON_message['presence'] = presence
        socketio.emit('update_member', JSON_message, broadcast=True)

    return presence


######
# WS #
######

@socketio.on('update_member')
def handle_json(JSON_message):

    # Extract member ID from WS message
    member_id = JSON_message['id']

    conn = mysql.connect()
    cursor = conn.cursor()

    # Get current attributes of a member
    cursor.execute("""SELECT member_name, presence, arrival, location FROM nameboards WHERE id=%s""", member_id)
    result = cursor.fetchone()
    row_headers = [x[0] for x in cursor.description]
    current_attributes = dict(zip(row_headers,result))

    # Substitute the attributes by the JSON_message's attributes
    for attribute in JSON_message:
        if attribute != "id":
            current_attributes[attribute] = JSON_message[attribute]

    # Update the member with its new information
    cursor.execute("""UPDATE nameboards SET member_name=%s,presence=%s,location=%s,arrival=%s WHERE id=%s""", (
        current_attributes['member_name'], current_attributes['presence'], current_attributes['location'], current_attributes['arrival'], member_id))

    conn.commit()
    cursor.close()
    conn.close()

    # Update all clients
    emit('update_member', JSON_message, broadcast=True)



################################
## Execution as python script ##
################################

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
