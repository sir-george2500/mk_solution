from ratelimiter import RateLimiter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
from typing import Dict
import asyncio

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: float = 1.0):
        super().__init__(app)
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.max_calls = calls
        self.period = period

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else None
        
        if not client_host:
            return await call_next(request)
            
        # Get or create a rate limiter for this client
        if client_host not in self.rate_limiters:
            self.rate_limiters[client_host] = RateLimiter(max_calls=self.max_calls, period=self.period)
            
        limiter = self.rate_limiters[client_host]
        
        try:
            # Use the context manager to acquire the rate limit
            async with asyncio.timeout(0.1):  # 100ms timeout for rate limit check
                with limiter:
                    return await call_next(request)
        except (asyncio.TimeoutError, RuntimeError):
            return JSONResponse(
                {"detail": "Rate limit exceeded"}, 
                status_code=429,
                headers={"Retry-After": str(int(self.period))}
            )
