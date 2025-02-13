from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api.v1.auth.auth_routes import auth_router
from rate_limiter.rate_limiter import RateLimiterMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from routes.api.v1.users.user_routes import user_data_router

# Initialize FastAPI app
app = FastAPI(title="MK Solutions", docs_url="/")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
app.include_router(user_data_router, prefix="/api/v1", tags=["User"])

# Add the RateLimiterMiddleware
# Add rate limiter middleware
rate_limiter_middleware = RateLimiterMiddleware(capacity=100, refill_rate=1.0)
app.add_middleware(BaseHTTPMiddleware,dispatch=rate_limiter_middleware)
