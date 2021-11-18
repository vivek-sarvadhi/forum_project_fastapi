from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2, config
from fastapi.security import OAuth2PasswordRequestForm
import random
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig


router = APIRouter(
    tags = ['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/forgotpassword')
async def forgotpassword(forget_password: schemas.UserForgotPassword, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == forget_password.email).first()
    if user:
        random_num = random.randint(100000,999999)
        otp = random_num
        message = MessageSchema(
            subject="send otp forgot password",
            recipients=[user.email], 
            body=otp,
            # subtype="html"
            )
        fm = FastMail(config.conf)
        await fm.send_message(message)
        new_post = models.EmailOTP(otp=otp, user_id=user.id)
        db.add(new_post)
        db.commit()
        return JSONResponse(content={"Status": status.HTTP_200_OK, "error": False, 'message': 'We have sent you a otp to reset your password'}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'email is not registered'}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/otpcheck')
def otpcheck(otp_check: schemas.UserOTPCheck, db: Session = Depends(database.get_db)):
    emailotp = db.query(models.EmailOTP).join(models.User).filter(models.User.email == otp_check.email).order_by(models.EmailOTP.id.desc()).first()
    if emailotp:
        if emailotp.otp == otp_check.otp:
            emailotp.otp_check = True
            db.commit()
            return JSONResponse(content={'status':status.HTTP_200_OK, 'error':False, 'message': 'otp check please set new password'}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'otp is expire or not valid this mail'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'please enter valid email or otp'}, status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/setnewpassword')
def setnewpassword(setnew_password: schemas.UserSetPassword, db: Session = Depends(database.get_db)):
    print(setnew_password.email)
    user_obj = db.query(models.User).filter(models.User.email == setnew_password.email).first()
    if user_obj:
        emailotp_obj = db.query(models.EmailOTP).filter(models.EmailOTP.user_id == user_obj.id).order_by(models.EmailOTP.id.desc()).first()
        if emailotp_obj:
            if emailotp_obj.otp_check == True:
                hashed_password = utils.hash(setnew_password.password)
                user_obj.password = hashed_password
                delete_otp = db.query(models.EmailOTP).filter(models.EmailOTP.user_id == user_obj.id)
                delete_otp.delete(synchronize_session=False)
                db.commit()
                return JSONResponse(content={'status':status.HTTP_200_OK, 'error':False, 'message': 'Successfully set new password'}, status_code=status.HTTP_200_OK)
            return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'please check validate otp to this mail'}, status_code=status.HTTP_400_BAD_REQUEST)
        return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'please check validate otp to this mail'}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"Status": status.HTTP_400_BAD_REQUEST, 'error':True, 'error_message': 'please enter valid email'}, status_code=status.HTTP_400_BAD_REQUEST)