# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Either in here, or in consumers, we need to limit chat attendees to their own groups.
# Also, should have way to see if online, and maybe who is in chat?
# Prepend each message with the username?

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
