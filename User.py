class User:
    def __init__(self, socket_id):
        self.socket_id = socket_id
        self.room = 0
        self.room_id = 0
        self.isready = False
        self.name = ''

    def setName(self, name):
        self.name = name

    def setRoom(self, room):
        self.room = room

    def setRoomID(self, room_id):
        self.room_id = room_id

    def setReady(self):
        self.isready = True
    
    def setUnready(self):
        self.isready = False