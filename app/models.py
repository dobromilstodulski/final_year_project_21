from peewee import *
import datetime
from flask_login import UserMixin, AnonymousUserMixin, login_user
#from flask_bcrypt import generate_password_hash
from werkzeug.security import generate_password_hash

database = SqliteDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = database


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    fullname = CharField()
    password = CharField()
    email = CharField(unique=True)
    gender = CharField()
    birthday = CharField()
    description = TextField(null=True, default=None)
    profile_picture = CharField(null=True, default=None)
    join_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-join_date',)

    def get_posts(self):
        return Post.select().where(Post.user == self).order_by(Post.pub_date.desc())

    def get_songs(self):
        return Song.select().where(Song.user == self).order_by(Song.timestamp.desc())

    def get_post_feed(self):
        return Post.select().order_by(Post.pub_date.desc())

    def get_private_post_feed(self):
        return Post.select().where(
            # all posts from people Im following
            (Post.user << self.following())
        ).order_by(Post.pub_date.desc())

    def following(self):
        '''The users that we are following.'''
        return (
            User.select().join(Relationship, on=Relationship.to_user).where(
                Relationship.from_user == self)
        )

    def followers(self):
        '''Get users following the current user'''
        return(
            User.select().join(Relationship, on=Relationship.from_user).where(
                Relationship.to_user == self)
        )

    def hasUserLiked(self, post_id):
        query = Post.select().join(
            Like, on=Like.post_id
        ).where(
            Like.user_id == self,
            Like.post_id == post_id
        )
        try:
            ret = query[0].id
            return 1
        except:
            return 0

    def hasUserFavourited(self, song_id):
        query = Song.select().join(
            Favourite, on=Favourite.song_id
        ).where(
            Favourite.user_id == self,
            Favourite.post_id == song_id
        )
        try:
            ret = query[0].id
            return 1
        except:
            return 0

    @classmethod
    def create_user(cls, username, fullname, email, password, gender, birthday, description, profile_picture):
        try:
            with database.transaction():
                cls.create(
                    username=username,
                    fullname=fullname,
                    email=email,
                    password=generate_password_hash(password),
                    gender=gender,
                    birthday=birthday,
                    description=description,
                    profile_picture=profile_picture)
        except IntegrityError:
            raise ValueError("User already exists")


class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        # `indexes` is a tuple of 2-tuples, where the 2-tuples are
        # a tuple of column names to index and a boolean indicating
        # whether the index is unique or not.
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('from_user', 'to_user'), True),
        )


class Post(BaseModel):
    user = ForeignKeyField(model=User, related_name='posts')
    content = TextField()
    media = CharField(null=True)
    isMedia = BooleanField(default=0)
    numLikes = IntegerField(default=0)
    numComments = IntegerField(default=0)
    pub_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-pub_date',)


class Song(BaseModel):
    user = ForeignKeyField(User, backref='songs')
    artwork = CharField()
    artist = CharField()
    title = CharField()
    feature = CharField(null=True)
    genre = CharField()
    description = TextField(null=True)
    tags = CharField(null=True)
    source = CharField()
    date_uploaded = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-date_uploaded',)


class Message(BaseModel):
    sender_id = ForeignKeyField(User, backref='sent_messages')
    recipient_id = ForeignKeyField(User, backref='received_messages')
    body = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-timestamp',)


class Chat(BaseModel):
    user_id = ForeignKeyField(User, backref='chats')
    body = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-timestamp',)
        

class Msg(BaseModel):
    username = ForeignKeyField(User, backref='chats')
    message = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-timestamp',)


class Comment(BaseModel):
    user_id = ForeignKeyField(model=User, related_name='user_likes', null=True)
    post_id = ForeignKeyField(model=Post, related_name='post_likes', null=True)
    song_id = ForeignKeyField(model=Song, related_name='song_likes', null=True)
    comment = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database
        order_by = ('-timestamp',)


class Like(BaseModel):
    user_id = ForeignKeyField(User, related_name='user_likes', null=True)
    post_id = ForeignKeyField(Post, related_name='post_likes', null=True)


class Favourite(BaseModel):
    user_id = ForeignKeyField(User, related_name='user_likes', null=True)
    song_id = ForeignKeyField(Song, related_name='song_likes', null=True)


class Location(BaseModel):
    city = CharField()
    state = CharField()
    country = CharField()


class Group(BaseModel):
    _type = CharField()
    description = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)


def initialize():
    database.connect()
    database.create_tables([User, Post, Song, Message, Comment, Chat, Msg,
                           Like, Favourite, Location, Group, Relationship], safe=True)
    database.close()
