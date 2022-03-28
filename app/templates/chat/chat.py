import os
import time
from flask import Blueprint, g, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import socketio, pusher_client, moment
from app.models import Chat, Msg, database
from flask_socketio import emit, join_room, leave_room, send
import datetime

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

@chatroom.route("/pusher", methods=['GET', 'POST'])
@login_required
def pusher():
    msgs = Msg
    username = request.form.get('username')
    message = request.form.get('message')
    
    Msg.create(
                username=username,
                message=message
            )
    
    pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})

    
    return render_template("chat/pusher.html", msgs=msgs, current_user=current_user)

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    emit('status', {'msg': current_user.username + ' has entered the room.'})


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    emit('message', {'msg': current_user.username + ': ' + message['msg']})


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    emit('status', {'msg': current_user.username + ' has left the room.'})


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)
    




