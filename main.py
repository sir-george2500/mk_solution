from fastapi import FastAPI
from starlette.responses import JSONResponse

from rate_limiter.rate_limiter import RateLimiterMiddleware

# Initialize FastAPI app
app = FastAPI(title="MK Solutions", docs_url="/")

# Add the RateLimiterMiddleware
app.add_middleware(RateLimiterMiddleware)
