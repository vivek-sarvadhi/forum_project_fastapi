from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, utils, config
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

router = APIRouter(
    prefix = "/users",
    tags=['User']
)


html = """
<p>Hi this test mail, thanks for using Fastapi-mail</p> 
"""

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    message = MessageSchema(
        subject="account created successfully",
        recipients=[user.email], 
        body=html,
        # subtype="html"
        )
    fm = FastMail(config.conf)
    await fm.send_message(message, template_name='email.html')
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exists")
    return user