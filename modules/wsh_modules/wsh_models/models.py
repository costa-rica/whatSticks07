from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, \
    Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from wsh_config import ConfigDev, ConfigProd
from flask_login import UserMixin, LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json


config = ConfigDev()

Base = declarative_base()
engine = create_engine(config.SQL_URI, echo = False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
sess = Session()

login_manager= LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(any_name_for_id_obj):# any_name_for_id_obj can be any name because its an arg that is the user id.
    # This is probably created somewhere inside flask_login when the user gets logged in. But i've not been able to track it.
    return sess.query(Users).filter_by(id = any_name_for_id_obj).first()
    

class Users(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email = Column(Text, unique = True, nullable = False)
    password = Column(Text, nullable = False)
    lat = Column(Float(precision=4, decimal_return_scale=None))
    lon = Column(Float(precision=4, decimal_return_scale=None))
    oura_token_id = relationship("Oura_token", backref="oura_token_id", lazy=True)
    oura_sleep = relationship('Oura_sleep_descriptions', backref='oura_sleep', lazy=True)
    loc_day = relationship('User_location_day', backref='user_loc_day', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def get_reset_token(self, expires_sec=1800):
        s=Serializer(config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return sess.query(Users).get(user_id)

    def __repr__(self):
        return f'Users(id: {self.id}, email: {self.email})'


class User_location_day(Base):
    __tablename__ = 'user_location_day'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location_id = Column(Integer, nullable = False)#TODO: should this remain nullable=False?
    date = Column(Text)
    local_time = Column(Text)
    row_type = Column(Text)#user entered or scheduler entered row?
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'User_location_day(id: {self.id}, user_id: {self.user_id},' \
            f'date: {self.date})'


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer,  primary_key = True)
    city = Column(Text)
    region = Column(Text)
    country = Column(Text)
    lat = Column(Float(precision=4, decimal_return_scale=None))
    lon = Column(Float(precision=4, decimal_return_scale=None))
    tz_id = Column(Text)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    # oura_sleep = relationship('Oura_sleep_descriptions', backref='oura_sleep', lazy=True)
    weather_hist = relationship('Weather_history', backref = 'weath_hist', lazy = True)

    def __repr__(self):
        return f'Locations(id: {self.id}, city: {self.city}, lat: {self.lat}, ' \
            f'lon: {self.lon})'


class Oura_token(Base):
    __tablename__ = 'oura_token'
    id = Column(Integer, primary_key = True )
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(Text)
    oura_sleep = relationship('Oura_sleep_descriptions', backref='Oura_sleep_descrip', lazy=True)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'Oura_token(id: {self.id}, token: {self.token})'


class Weather_history(Base):
    __tablename__ = 'weather_history'
    id = Column(Integer,primary_key = True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable = False)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)
    datetime = Column(Text)
    datetimeEpoch = Column(Integer)
    tempmax = Column(Float)
    tempmin = Column(Float)
    temp = Column(Float)
    feelslikemax = Column(Float)
    feelslikemin = Column(Float)
    feelslike = Column(Float)
    dew = Column(Text)
    humidity = Column(Text)
    precip = Column(Text)
    precipprob = Column(Text)
    precipcover = Column(Text)
    preciptype = Column(Text)
    snow = Column(Text)
    snowdepth = Column(Text)
    windgust = Column(Text)
    windspeed = Column(Text)
    winddir = Column(Text)
    pressure = Column(Text)
    cloudcover = Column(Text)
    visibility = Column(Text)
    solarradiation = Column(Text)
    solarenergy = Column(Text)
    uvindex = Column(Text)
    sunrise = Column(Text)
    sunriseEpoch = Column(Text)
    sunset = Column(Text)
    sunsetEpoch = Column(Text)
    moonphase = Column(Text)
    conditions = Column(Text)
    description = Column(Text)
    icon = Column(Text)
    
    

    def __repr__(self):
        return f"Weather_history(id: {self.id}, datetime: {self.datetime}, " \
            f"location_id: {self.location_id}, temp: {self.temp})"



class Oura_sleep_descriptions(Base):
    __tablename__ = 'oura_sleep_descriptions'
    id = Column(Integer, primary_key = True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
    token_id=Column(Integer, ForeignKey('oura_token.id'), nullable=False)
    summary_date = Column(Text)
    period_id = Column(Integer)
    is_longest = Column(Integer)
    timezone = Column(Integer)
    location = Column(Integer)#haven't found in oura data yet
    bedtime_end = Column(Text)
    bedtime_start = Column(Text)
    breath_average = Column(Float)
    duration = Column(Integer)
    total = Column(Integer)
    awake = Column(Integer)
    rem = Column(Integer)
    deep = Column(Integer)
    light = Column(Integer)
    midpoint_time = Column(Integer)
    efficiency = Column(Integer)
    restless = Column(Integer)
    onset_latency = Column(Integer)
    rmssd = Column(Integer)
    score = Column(Integer)
    score_alignment = Column(Integer)
    score_deep = Column(Integer)
    score_disturbances = Column(Integer)
    score_efficiency = Column(Integer)
    score_latency = Column(Integer)
    score_rem = Column(Integer)
    score_total = Column(Integer)
    temperature_deviation = Column(Float)
    bedtime_start_delta = Column(Integer)
    bedtime_end_delta = Column(Integer)
    midpoint_at_delta = Column(Integer)
    temperature_delta = Column(Float)
    hr_lowest = Column(Integer)
    hr_average = Column(Float)
    # temperature_trend_deviation=Column(Float)

    time_stamp_utc = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Oura_sleep_descriptions(id: {self.id}, user_id: {self.user_id}," \
            f"summary_date:{self.summary_date}," \
            f"score: {self.score}, score_total: {self.score_total}," \
            f"hr_lowest: {self.hr_lowest}, hr_average: {self.hr_average}," \
            f"bedtime_start: {self.bedtime_start}, bedtime_end: {self.bedtime_end}," \
            f"duration: {self.duration}, onset_latency: {self.onset_latency})"





#Build db
if 'users' in inspect(engine).get_table_names():
    print('db already exists')
else:
    Base.metadata.create_all(engine)
    print('NEW db created.')