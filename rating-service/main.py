from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
import httpx

from database import SessionLocal, engine, Base
from models import Rating
from schemas import RatingCreate, RatingUpdate, RatingResponse

# Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(title="Rating Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
RECIPE_SERVICE_URL = os.getenv("RECIPE_SERVICE_URL", "http://recipe-service:8002")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_user_token(token: str):
    print(f"🔐 [DEBUG] Starting token verification...")
    print(f"🔐 [DEBUG] USER_SERVICE_URL: {USER_SERVICE_URL}")
    print(f"🔐 [DEBUG] Token received (first 20 chars): {token[:20]}...")
    
    async with httpx.AsyncClient() as client:
        try:
            # First test if user service is reachable
            print(f"🔐 [DEBUG] Testing connection to user service...")
            health_response = await client.get(f"{USER_SERVICE_URL}/", timeout=5.0)
            print(f"🔐 [DEBUG] User service health check status: {health_response.status_code}")
            
            # Now verify the token
            print(f"🔐 [DEBUG] Verifying token with /users/me endpoint...")
            response = await client.get(
                f"{USER_SERVICE_URL}/users/me", 
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            
            print(f"🔐 [DEBUG] Token verification response status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ [DEBUG] Token valid for user ID: {user_data.get('id')}, Username: {user_data.get('username')}")
                return user_data
            else:
                print(f"❌ [DEBUG] Token invalid - Status: {response.status_code}")
                print(f"❌ [DEBUG] Response text: {response.text}")
                return None
                
        except httpx.ConnectError as e:
            print(f"🚨 [DEBUG] Connection error to user service: {e}")
            return None
        except httpx.TimeoutException as e:
            print(f"🚨 [DEBUG] Timeout connecting to user service: {e}")
            return None
        except Exception as e:
            print(f"🚨 [DEBUG] Unexpected error: {e}")
            return None

async def verify_recipe_exists(recipe_id: int):
    print(f"🍳 [DEBUG] Verifying recipe exists: {recipe_id}")
    print(f"🍳 [DEBUG] RECIPE_SERVICE_URL: {RECIPE_SERVICE_URL}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{RECIPE_SERVICE_URL}/recipes/{recipe_id}", timeout=5.0)
            print(f"🍳 [DEBUG] Recipe verification status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"🚨 [DEBUG] Error verifying recipe: {e}")
            return False

@app.post("/ratings", response_model=RatingResponse)
async def create_rating(
    rating: RatingCreate, 
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    print(f"⭐ [DEBUG] Starting rating creation...")
    print(f"⭐ [DEBUG] Rating data: {rating.dict()}")
    
    # Extract token from Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        print(f"🚨 [DEBUG] Missing or invalid Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required"
        )
    
    token = authorization.replace("Bearer ", "")
    print(f"⭐ [DEBUG] Token extracted from header")
    
    # Verify user token
    user_data = await verify_user_token(token)
    
    if not user_data:
        print(f"🚨 [DEBUG] Token verification failed")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    print(f"✅ [DEBUG] User authenticated: {user_data['id']}")
    
    # Verify recipe exists
    if not await verify_recipe_exists(rating.recipe_id):
        print(f"🚨 [DEBUG] Recipe not found: {rating.recipe_id}")
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    print(f"✅ [DEBUG] Recipe verified: {rating.recipe_id}")
    
    # Check if user already rated this recipe
    existing_rating = db.query(Rating).filter(
        Rating.user_id == user_data["id"],
        Rating.recipe_id == rating.recipe_id
    ).first()
    
    if existing_rating:
        print(f"🚨 [DEBUG] User already rated this recipe")
        raise HTTPException(status_code=400, detail="You have already rated this recipe")
    
    # Create new rating
    print(f"⭐ [DEBUG] Creating new rating...")
    db_rating = Rating(**rating.dict(), user_id=user_data["id"])
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    print(f"✅ [DEBUG] Rating created successfully: {db_rating.id}")
    return db_rating

@app.get("/recipes/{recipe_id}/ratings", response_model=List[RatingResponse])
def get_recipe_ratings(recipe_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print(f"📊 [DEBUG] Getting ratings for recipe: {recipe_id}")
    ratings = db.query(Rating).filter(Rating.recipe_id == recipe_id).offset(skip).limit(limit).all()
    print(f"📊 [DEBUG] Found {len(ratings)} ratings")
    return ratings

@app.put("/ratings/{rating_id}", response_model=RatingResponse)
async def update_rating(
    rating_id: int, 
    rating: RatingUpdate, 
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    print(f"✏️ [DEBUG] Updating rating: {rating_id}")
    
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
    
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    if db_rating.user_id != user_data["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this rating")
    
    for key, value in rating.dict(exclude_unset=True).items():
        setattr(db_rating, key, value)
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.delete("/ratings/{rating_id}")
async def delete_rating(
    rating_id: int, 
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    print(f"🗑️ [DEBUG] Deleting rating: {rating_id}")
    
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
    
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    if db_rating.user_id != user_data["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this rating")
    
    db.delete(db_rating)
    db.commit()
    return {"message": "Rating deleted successfully"}

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "rating-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8003)))









# from fastapi import FastAPI, Depends, HTTPException, status, Header
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List
# import os
# from dotenv import load_dotenv
# import httpx

# from database import SessionLocal, engine, Base
# from models import Rating
# from schemas import RatingCreate, RatingUpdate, RatingResponse

# # Base.metadata.create_all(bind=engine)

# load_dotenv()

# app = FastAPI(title="Rating Service", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Your frontend URLs
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
# RECIPE_SERVICE_URL = os.getenv("RECIPE_SERVICE_URL", "http://recipe-service:8002")

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

# async def verify_recipe_exists(recipe_id: int):
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(f"{RECIPE_SERVICE_URL}/recipes/{recipe_id}")
#             return response.status_code == 200
#         except:
#             return False

# @app.post("/ratings", response_model=RatingResponse)
# # async def create_rating(rating: RatingCreate, token: str, db: Session = Depends(get_db)):
# #     user_data = await verify_user_token(token)
# async def create_rating(
#     rating: RatingCreate, 
#     authorization: str = Header(None),
#     db: Session = Depends(get_db)
# ):
#     # Extract token from Authorization header
#     if not authorization or not authorization.startswith("Bearer "):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authorization header with Bearer token required"
#         )
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     if not await verify_recipe_exists(rating.recipe_id):
#         raise HTTPException(status_code=404, detail="Recipe not found")
    
#     existing_rating = db.query(Rating).filter(
#         Rating.user_id == user_data["id"],
#         Rating.recipe_id == rating.recipe_id
#     ).first()
    
#     if existing_rating:
#         raise HTTPException(status_code=400, detail="You have already rated this recipe")
    
#     db_rating = Rating(**rating.dict(), user_id=user_data["id"])
#     db.add(db_rating)
#     db.commit()
#     db.refresh(db_rating)
#     return db_rating

# @app.get("/recipes/{recipe_id}/ratings", response_model=List[RatingResponse])
# def get_recipe_ratings(recipe_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     ratings = db.query(Rating).filter(Rating.recipe_id == recipe_id).offset(skip).limit(limit).all()
#     return ratings

# @app.put("/ratings/{rating_id}", response_model=RatingResponse)
# async def update_rating(rating_id: int, rating: RatingUpdate, token: str, db: Session = Depends(get_db)):
#     user_data = await verify_user_token(token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
#     if db_rating is None:
#         raise HTTPException(status_code=404, detail="Rating not found")
    
#     if db_rating.user_id != user_data["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to update this rating")
    
#     for key, value in rating.dict(exclude_unset=True).items():
#         setattr(db_rating, key, value)
    
#     db.commit()
#     db.refresh(db_rating)
#     return db_rating

# @app.delete("/ratings/{rating_id}")
# async def delete_rating(rating_id: int, token: str, db: Session = Depends(get_db)):
#     user_data = await verify_user_token(token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
#     if db_rating is None:
#         raise HTTPException(status_code=404, detail="Rating not found")
    
#     if db_rating.user_id != user_data["id"]:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this rating")
    
#     db.delete(db_rating)
#     db.commit()
#     return {"message": "Rating deleted successfully"}

# @app.get("/")
# def health_check():
#     return {"status": "healthy", "service": "rating-service"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8003)))