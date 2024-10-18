from fastapi import APIRouter, HTTPException, Depends
from db.db import get_db
from models.Users import UserLogin, UserResponse,UserCreate
import sqlite3

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.delete('/deleteUser/{id}')
def deleteUser(id : int):
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('DELETE FROM Users WHERE ID = ?', (id,))
            connect.commit()

        return {"message": "Usuario eliminado exitosamente"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar usuario: {str(e)}")
    finally:

        connect.close()

@router.put("/updateStatus/{user_id}")
def update_user_status(user_id: int):
    try:
        with get_db() as conn:
            cursor = conn.cursor()

            # Verificar el estado actual del usuario
            cursor.execute("SELECT Status FROM Users WHERE ID = ?", (user_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            current_status = result[0]

            # Determinar el nuevo estado
            new_status = "Inactivo" if current_status == "Activo" else "Activo"

            # Actualizar el estado del usuario en la base de datos
            cursor.execute("UPDATE Users SET Status = ? WHERE ID = ?", (new_status, user_id))
            conn.commit()

            return {"message": f"Estado del usuario actualizado a {new_status}", "new_status": new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el estado del usuario: {str(e)}")

@router.get('/getUsers')
def getUsers():
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT ID, UserName, TypeUser, UID, Code, Status FROM Users')
            result = cursor.fetchall()

            # Convertir los resultados a una lista de diccionarios
            users = [
                {
                    "id": row[0],
                    "name": row[1],
                    "typeUser": row[2],
                    "UID": row[3],
                    "Code": row[4],
                    "Status": row[5]
                }
                for row in result
            ]
            return users
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al visualizar usuarios: {str(e)}")
    finally:
        connect.close()    
    

@router.post('/addUser')
def createUser(user: UserCreate):
    try:
        # Usar 'with' para manejar la base de datos
        with get_db() as connect:
            cursor = connect.cursor()

            # Verificar si el usuario o el UID ya existen
            cursor.execute(
                'SELECT * FROM Users WHERE UserName = ? OR UID = ?',
                (user.name, user.UID)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="El nombre de usuario o el UID ya existen"
                )

            # Si no existe, insertar el nuevo usuario
            cursor.execute(
                'INSERT INTO Users (UserName, Password, TypeUser, UID, Code, Status) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    user.name,
                    user.password,
                    user.typeUser,
                    user.UID,
                    user.Code,
                    user.Status
                )
            )
            connect.commit()

        # Retornar un mensaje de éxito
        return {"message": "Usuario agregado exitosamente"}

    except Exception as e:
        # Manejar cualquier error que ocurra
        raise HTTPException(
            status_code=500,
            detail=f"Error al agregar usuario: {str(e)}"
        )

    finally:
        connect.close()


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
