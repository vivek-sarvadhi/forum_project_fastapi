from fastapi import Response, status, HTTPException, Depends, APIRouter, Form, File, UploadFile, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy import func
from fastapi_pagination import Page, LimitOffsetPage, paginate, add_pagination
import shutil
from typing import Optional

router = APIRouter(
    prefix = "/comment",
    tags=['comment']
)


@router.post("/")
def create_comment(body: str = Form(...), comment_file: UploadFile = File(...), post_id: int = Form(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    with open("media/comment_file/"+comment_file.filename, "wb") as image:
        shutil.copyfileobj(comment_file.file, image)
    url = str("media/comment_file/"+comment_file.filename)
    new_comment = models.Comment(user_id=current_user.id, body=body, comment_file=url, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get('/')
def get_comment(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.parent_id == None).all()
    return comment


@router.post("/reaply")
def reaply_comment(body: str = Form(...), comment_file: UploadFile = File(...), parent_id: int = Form(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    with open("media/comment_file/"+comment_file.filename, "wb") as image:
        shutil.copyfileobj(comment_file.file, image)
    url = str("media/comment_file/"+comment_file.filename)
    new_comment = models.Comment(user_id=current_user.id, body=body, comment_file=url, parent_id=parent_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
