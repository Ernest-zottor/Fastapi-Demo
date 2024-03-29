from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# origins = ['https://www.google.com', 'https://www.youtube.com'] This will only allow google and youtube to communicate to our API
origins = ['*'] # The wildcard allows all.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message': 'Hello, welcome to FastApi Demo by Ernest. Go to /docs for the API'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

