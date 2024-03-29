from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, BigInteger
from sqlalchemy.orm import relationship

Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'
    gameid = Column(Integer, primary_key=True)
    appid = Column(BigInteger)
    gamename = Column(Text)
    gameevents = relationship('GameEvents', backref='game', lazy='dynamic')
    about_the_game = Column(Text)
    achievements = Column(Text)
    background = Column(Text)
    categories = Column(Text)
    content_descriptors = Column(Text)
    controller_support = Column(Text)
    detailed_description = Column(Text)
    developers = Column(Text)
    dlc = Column(Text)
    genres = Column(Text)
    header_image = Column(Text)
    is_free = Column(Text)
    legal_notice = Column(Text)
    linux_requirements = Column(Text)
    mac_requirements = Column(Text)
    metacritic = Column(Text)
    movies = Column(Text)
    package_groups = Column(Text)
    pc_requirements = Column(Text)
    platforms = Column(Text)
    publishers = Column(Text)
    recommendations = Column(Text)
    release_date = Column(Text)
    required_age = Column(Text)
    reviews = Column(Text)
    screenshots = Column(Text)
    short_description = Column(Text)
    support_info = Column(Text)
    supported_languages = Column(Text)
    type = Column(Text)
    website = Column(Text)


class GameEvents(Base):
    __tablename__ = 'gameevents'
    gameeventsid = Column(Integer, primary_key=True)
    gameeventname = Column(Text)
    gameid = Column(Integer, ForeignKey('game.gameid'))
    gameeventdate = Column(DateTime)
    current_players = Column(Integer)
    userid = Column(Integer, ForeignKey('user.userid'))


class User(Base):
    __tablename__ = 'user'
    userid = Column(Integer, primary_key=True)
    steam_id = Column(BigInteger)
    communityvisibilitystate = Column(Integer)
    profilestate = Column(Integer)
    personaname = Column(Text)
    lastlogoff = Column(Integer)
    profileurl = Column(Text)
    avatarfull = Column(Text)
    personastate = Column(Integer)
    primaryclanid = Column(BigInteger)
    timecreated = Column(BigInteger)
    personastateflags = Column(Integer)
    loccountrycode = Column(String)
    locstatecode = Column(Integer)
    gameevents = relationship('GameEvents', backref='user', lazy='dynamic')
