from fastapi import Request, HTTPException
from rate_limiter.algorithms.token_token import TokenBucket

class RateLimiterMiddleware:
    """
    Middleware for rate limiting requests using the Token Bucket algorithm.

    Args:
        capacity (int): The maximum number of tokens the bucket can hold.
        refill_rate (float): The rate at which tokens are refilled (tokens per second).

    Attributes:
        bucket (TokenBucket): An instance of the TokenBucket class representing the token bucket.

    Raises:
        HTTPException: If the rate limit is exceeded (HTTP status code 429).

    Usage Example:
        ```python
        from fastapi import FastAPI
        from your_module import RateLimiterMiddleware

        app = FastAPI()
        app.add_middleware(RateLimiterMiddleware(capacity=100, refill_rate=1.0))
        ```
    """

    def __init__(self, capacity: int, refill_rate: float):
        self.bucket = TokenBucket(capacity, refill_rate)

    async def __call__(self, request: Request, call_next):
        """
        Middleware method that gets called for each incoming request.

        Args:
            request (Request): The incoming request object.
            call_next (function): The function to call to proceed with handling the request.

        Returns:
            Response: The response generated by the corresponding path operation.

        Raises:
            HTTPException: If the rate limit is exceeded (HTTP status code 429).
        """
        self.bucket.get_tokens()
        if not self.bucket.consume(1):
            raise HTTPException(status_code=429, detail="Too Many Requests")
        return await call_next(request)

