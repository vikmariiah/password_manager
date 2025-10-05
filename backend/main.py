from fastapi import FastAPI, HTTPException
import bcrypt
from .database import get_connection


#creates the app
app = FastAPI()



#user registration
@app.post("\register")
def register(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    #checks if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.clone()
        conn.close()
        raise HTTPException(status_code=400, detail="User with this email already registered")
    
    #hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    #make new user
    cursor.execute(
        "INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id",
        (email, hashed_password.decode("utf-8"))
    )
    user_id = cursor.fetchone()[0]


    #save changes
    conn.commit()
    cursor.close()
    conn.close()


    #return response
    return {"message": "User registered successfully", "user_id": user_id}


