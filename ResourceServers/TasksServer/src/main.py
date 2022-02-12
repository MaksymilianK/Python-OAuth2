from config import WebConfig
from web.routes import app
from fastapi.middleware.cors import CORSMiddleware

if WebConfig.CORS_ENABLED:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=WebConfig.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
