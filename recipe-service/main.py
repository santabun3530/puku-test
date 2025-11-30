from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
import httpx
from jose import JWTError, jwt  # ADD THIS IMPORT

from database import SessionLocal, engine, Base
from models import Recipe
from schemas import RecipeCreate, RecipeUpdate, RecipeResponse

# Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(title="Recipe Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")

# ADD THESE LINES - Use same SECRET_KEY as user service
SECRET_KEY = os.getenv("SECRET_KEY", "de6b19b222")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_user_token(token: str):
    print(f"🔐 [Recipe Service] Verifying token...")
    
    # Try local JWT validation first (same as rating service fix)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id = payload.get("user_id")
        
        if username and user_id:
            print(f"✅ [Recipe Service] Local JWT valid for user: {username}")
            return {"id": user_id, "username": username}
        return None
    except JWTError as e:
        print(f"❌ [Recipe Service] Local JWT validation failed: {e}")
        # Fallback to user service API
        return await verify_user_token_fallback(token)

async def verify_user_token_fallback(token: str):
    """Fallback to user service API validation"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{USER_SERVICE_URL}/users/me", 
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

@app.post("/recipes", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate, 
    authorization: str = Header(None),  # CHANGE: Use header instead of token parameter
    db: Session = Depends(get_db)
):
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required"
        )
    
    token = authorization.replace("Bearer ", "")
    user_data = await verify_user_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = Recipe(**recipe.dict(), user_id=user_data["id"])
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.get("/recipes", response_model=List[RecipeResponse])
def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.put("/recipes/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: int, 
    recipe: RecipeUpdate, 
    authorization: str = Header(None),  # CHANGE: Use header
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required"
        )
    
    token = authorization.replace("Bearer ", "")
    user_data = await verify_user_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if db_recipe.user_id != user_data["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this recipe")
    
    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/recipes/{recipe_id}")
async def delete_recipe(
    recipe_id: int, 
    authorization: str = Header(None),  # CHANGE: Use header
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required"
        )
    
    token = authorization.replace("Bearer ", "")
    user_data = await verify_user_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if db_recipe.user_id != user_data["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this recipe")
    
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "recipe-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8002)))



# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List
# import os
# from dotenv import load_dotenv
# import httpx

# from database import SessionLocal, engine, Base
# from models import Recipe
# from schemas import RecipeCreate, RecipeUpdate, RecipeResponse

# # Base.metadata.create_all(bind=engine)

# load_dotenv()

# app = FastAPI(title="Recipe Service", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Your frontend URLs
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# async def verify_user_token(token: str):
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(f"{USER_SERVICE_URL}/users/me", 
#                                       headers={"Authorization": f"Bearer {token}"})
#             if response.status_code == 200:
#                 return response.json()
#             return None
#         except:
#             return None

# @app.post("/recipes", response_model=RecipeResponse)
# async def create_recipe(recipe: RecipeCreate, token: str, db: Session = Depends(get_db)):
#     user_data = await verify_user_token(token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     db_recipe = Recipe(**recipe.dict(), user_id=user_data["id"])
#     db.add(db_recipe)
#     db.commit()
#     db.refresh(db_recipe)
#     return db_recipe

# @app.get("/recipes", response_model=List[RecipeResponse])
# def get_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     recipes = db.query(Recipe).offset(skip).limit(limit).all()
#     return recipes

# @app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
# def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
#     recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
#     if recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
#     return recipe

# @app.put("/recipes/{recipe_id}", response_model=RecipeResponse)
# async def update_recipe(recipe_id: int, recipe: RecipeUpdate, token: str, db: Session = Depends(get_db)):
#     user_data = await verify_user_token(token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
#     if db_recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
    
#     if db_recipe.user_id != user_data["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to update this recipe")
    
#     for key, value in recipe.dict(exclude_unset=True).items():
#         setattr(db_recipe, key, value)
    
#     db.commit()
#     db.refresh(db_recipe)
#     return db_recipe

# @app.delete("/recipes/{recipe_id}")
# async def delete_recipe(recipe_id: int, token: str, db: Session = Depends(get_db)):
#     user_data = await verify_user_token(token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
#     if db_recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
    
#     if db_recipe.user_id != user_data["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this recipe")
    
#     db.delete(db_recipe)
#     db.commit()
#     return {"message": "Recipe deleted successfully"}

# @app.get("/")
# def health_check():
#     return {"status": "healthy", "service": "recipe-service"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8002)))