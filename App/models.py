from datetime import datetime
from re import S

class Post:
    
    def __init__(self, id, title, content, author, date, image):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self.image = image
    
    def __repr__(self):
        return (f'<"{self.title}" by {self.author}, id {self.id}>')

class Message:
    
    def __init__(self, content, type):
        self.content = content
        self.types = {
            'error': 'alert alert-danger',
            'warning': 'alert alert-warning',
            'success': 'alert alert-success',
            'primary': 'alert alert-primary',
            'secondary': 'alert alert-secondary'
        }
        self.type = self.types[type]

class User:
    
    def __init__(self, username, mail, profile_picture = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dovercourt.org%2Fwp-content%2Fuploads%2F2019%2F11%2F610-6104451_image-placeholder-png-user-profile-placeholder-image-png.jpg&f=1&nofb=1'):
        self.username = username
        self.mail = mail
        self.profile_picture = profile_picture
    
    def __repr__(self):
        return (f'<{self.username}>')