import os
import time
from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import socketio
from app.models import Chat, database
from flask_socketio import emit, join_room, leave_room, send

chatroom = Blueprint('chatroom', __name__)

ROOMS = ["Deep House", "Slap House", "Pop", "Rock", "Hip Hop", "Techno", "House", "Dance", "Drum & Bass", "Dubstep", 
        "Trance", "Reggae", "Jazz", "Classical", "Blues", "Country", "Folk", "Soul", "Indie", "Electronic", "Other"]


@chatroom.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    chats = Chat
    return render_template("chat/chat.html", username=current_user.username, chats=chats)

@chatroom.route("/chat2", methods=['GET', 'POST'])
@login_required
def chat2():
    return render_template("chat/chat2.html")


@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)

    
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
    
    
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)



