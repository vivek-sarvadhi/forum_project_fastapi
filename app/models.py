from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)


class EmailOTP(Base):
    __tablename__ = 'emailotps'

    id = Column(Integer, primary_key=True, nullable=False)
    otp = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    otp_check = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship('User')


class Forum(Base):
    __tablename__ = 'forums'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


tag_post_table = Table('association', Base.metadata, 
                    Column('tags_id', Integer, ForeignKey('tags.id')), 
                    Column('posts_id', Integer, ForeignKey('posts.id')))

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    post_id = relationship("Post", secondary=tag_post_table, back_populates="tag_id")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    forum_id = Column(Integer, ForeignKey('forums.id', ondelete="CASCADE"), nullable=True)
    prefix = Column(String, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    topic_file = Column(URLType, nullable=True)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    tag_id = relationship("Tag", secondary=tag_post_table, back_populates="post_id")

    owner = relationship('User')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, nullable=False)
    body = Column(String, nullable=True)
    comment_file = Column(URLType, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=True)
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete="CASCADE"), nullable=True)
    comment_point = Column(Integer, default=0, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



