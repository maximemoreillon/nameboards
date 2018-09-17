from flask import Flask, session, redirect, url_for, escape, request, render_template
from flaskext.mysql import MySQL
from flask_socketio import SocketIO, send, emit
import json
import sys

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Websockets config
socketio = SocketIO(app)

# MySQL configuration
MySQL_table = "nameboards"
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = "moreillon"
app.config['MYSQL_DATABASE_PASSWORD'] = "00174000"
app.config['MYSQL_DATABASE_DB'] = 'nameboards'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
# End of MySQL configuration


################
# HTTP routing #
################

@app.route('/')
def index():
    if 'group_name' in session:

        # Group name is gotten from session
        group_name = session['group_name']

        # Query to get all members
        SQL_query = "SELECT * FROM `%s` WHERE group_name='%s'"
        cursor.execute(SQL_query % (MySQL_table, group_name))
        members = cursor.fetchall()

        # Provide an option for big wall mounted displays (board)
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
        SQL_query = "SELECT DISTINCT group_name FROM `%s`;"
        cursor.execute(SQL_query % (MySQL_table))

        return render_template('select_group.html', group_names=cursor.fetchall() )

@app.route('/delete_group', methods=['POST', 'GET'])
def delete_group():

    # WARNING: This might not require its own route

    if request.method == 'POST':
        SQL_query = "DELETE FROM `%s` WHERE group_name='%s';"
        cursor.execute(SQL_query % (MySQL_table, request.form['group_name']))
        conn.commit()

    # No matter what, return to group selection
    return redirect(url_for('select_group'))


@app.route('/edit_members', methods=['POST', 'GET'])
def edit_members():
    if 'group_name' in session:
        group_name = session['group_name']

        if request.method == 'POST':
            # Post requests are for edition of the members, GET requests are for the UI
            if 'add_member' in request.form:
                SQL_query = "INSERT INTO `%s` (member_name, group_name, presence) VALUES ('Unnamed member', '%s', 0);"
                cursor.execute(SQL_query % (MySQL_table, group_name))
                conn.commit()

                # Sending an empty message to tell clients to refresh
                JSON_message = {}
                socketio.emit('refresh', JSON_message, broadcast=True)

            elif 'delete_member' in request.form:
                SQL_query = "DELETE FROM `%s` WHERE id='%s';"
                cursor.execute(SQL_query % (MySQL_table, request.form['id']))
                conn.commit()

                # Sending an empty message to tell clients to refresh
                JSON_message = {}
                socketio.emit('refresh', JSON_message, broadcast=True)

            elif 'edit_member' in request.form:
                SQL_query = "UPDATE `%s` SET member_name='%s' WHERE id='%s';"
                cursor.execute(SQL_query % (MySQL_table, request.form['member_name'], request.form['id']))
                conn.commit()

                # Update all clients through WS
                JSON_message = {}
                JSON_message['id'] = request.form['id']
                JSON_message['member_name'] = request.form['member_name']
                socketio.emit('update_member', JSON_message, broadcast=True)

            # The redirect will be in GET request
            return redirect(url_for('edit_members'))

        else:
            SQL_query = "SELECT * FROM `%s` WHERE group_name='%s'"
            cursor.execute(SQL_query % (MySQL_table, group_name))
            return render_template('edit_members.html', group_name=group_name, members=cursor.fetchall())
    else:
        # If session not set, go to select group page
        return redirect(url_for('select_group'))





@app.route('/update_presence', methods=['GET'])
def update_presence():

    # This is the API, toggles the state of someone through HTTP request

    member_name = request.args['member_name']
    group_name = request.args['group_name']
    presence = request.args['presence']

    SQL_query = "UPDATE `%s` SET presence='%s' WHERE member_name='%s' AND group_name='%s';"
    cursor.execute(SQL_query % (MySQL_table, presence, member_name, group_name))
    conn.commit()


    SQL_query = "SELECT id FROM `%s` WHERE group_name='%s' AND member_name='%s';"
    cursor.execute(SQL_query % (MySQL_table, group_name, member_name))
    member_ids = cursor.fetchall()

    # Update all clients using WS
    JSON_message = {}
    for member_id in member_ids:
        JSON_message['id'] = member_id[0]
        JSON_message['presence'] = presence
        print(JSON_message,sys.stdout)

        socketio.emit('update_member', JSON_message, broadcast=True)

    return redirect(url_for('index'))


######
# WS #
######

@socketio.on('update_member')
def handle_json(JSON_message):
    print('received json for update member: ' + str(JSON_message), sys.stdout)

    member_id = JSON_message['id']

    # THIS IS NOT GOING TO HANDLE JSON CONTAINING MULTIPLE INFO
    if 'presence' in JSON_message:
        member_presence = JSON_message['presence']
        SQL_query = "UPDATE `%s` SET presence='%s' WHERE id='%s';";
        cursor.execute(SQL_query % (MySQL_table, member_presence, member_id))

    if 'arrival' in JSON_message:
        member_arrival = JSON_message['arrival']
        SQL_query = "UPDATE `%s` SET arrival='%s' WHERE id='%s';";
        cursor.execute(SQL_query % (MySQL_table, member_arrival, member_id))

    if 'location' in JSON_message:
        member_location = JSON_message['location']
        SQL_query = "UPDATE `%s` SET location='%s' WHERE id='%s';";
        cursor.execute(SQL_query % (MySQL_table, member_location, member_id))

    conn.commit()

    # Update all clients
    emit('update_member', JSON_message, broadcast=True)
