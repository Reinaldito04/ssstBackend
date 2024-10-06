from fastapi import APIRouter, HTTPException, Depends
from db.db import get_db
from models.Users import UserLogin, UserResponse
import sqlite3

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_user(db: sqlite3.Connection, name: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE UserName = ?", (name,))
    user_row = cursor.fetchone()
    
    if user_row:
        return {
            "ID": user_row[0],
            "UserName": user_row[1],
            "Password": user_row[2],
            "TypeUser": user_row[3],
        }
    return None

@router.post('/login', response_model=UserResponse)
def login(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    db_user = get_user(db, user.name)

    if not db_user or db_user["Password"] != user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return UserResponse(
        id=db_user["ID"], 
        name=db_user["UserName"], 
        typeUser=db_user["TypeUser"]
    )
