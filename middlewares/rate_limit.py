

import time
import logging
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import Request
from fastapi.responses import JSONResponse
from utils.error_codes import ErrorCode, HttpStatusCode

logger = logging.getLogger(__name__)


class RateLimitConfig:
    """Configuration for rate limiting by endpoint pattern."""
    
    LIMITS = {
        "/auth/register": (3, 300),
        "/auth/login": (5, 300),
        "/auth/otp/send": (3, 600),
        "/auth/otp/verify": (5, 300),
        "/auth/password/reset": (3, 1800),
        "/auth/password/verify": (5, 600),
        "/api/resume/upload": (10, 300),
        "/api/resume/delete": (10, 300),
        "/api/jobmatching/analyse": (5, 60),
        "/api/interviewservice/question-gen": (5, 60),
        "/api/interview/start": (10, 300),
        "/api/interview/submit-answer": (50, 300),
        "/api/chat": (30, 60),
    }
    
    DEFAULT_LIMIT = (100, 300)
    
    @staticmethod
    def get_limit(path: str) -> Tuple[int, int]:
        """
        Get rate limit for a path, checking for exact match and prefix matches.
        
        Args:
            path: Request path
        
        Returns:
            Tuple of (max_requests, time_window_seconds)
        """
        if path in RateLimitConfig.LIMITS:
            return RateLimitConfig.LIMITS[path]
        
        for pattern, limit in RateLimitConfig.LIMITS.items():
            if path.startswith(pattern):
                return limit
        
        return RateLimitConfig.DEFAULT_LIMIT


class SlidingWindowRateLimiter:
    """
    Implements sliding window rate limiting algorithm.
    
    Tracks request timestamps for each client (by IP or user ID) and
    enforces limits based on a sliding time window.
    """
    
    def __init__(self):
        self.requests: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    
    def is_allowed(self, identifier: str, path: str) -> Tuple[bool, int, int]:
        """
        Check if request is allowed under rate limit.
        
        Uses sliding window approach:
        - Tracks all request timestamps in the time window
        - Removes timestamps outside the window
        - Checks if new request exceeds limit
        
        Args:
            identifier: Unique identifier (IP address or user ID)
            path: Request path
        
        Returns:
            Tuple of (is_allowed, requests_made, requests_limit)
        """
        now = time.time()
        max_requests, window_seconds = RateLimitConfig.get_limit(path)
        
        request_times = self.requests[identifier][path]
        
        cutoff_time = now - window_seconds
        valid_requests = [ts for ts in request_times if ts > cutoff_time]
        
        if len(valid_requests) >= max_requests:
            self.requests[identifier][path] = valid_requests
            return False, len(valid_requests), max_requests
        
        valid_requests.append(now)
        self.requests[identifier][path] = valid_requests
        
        return True, len(valid_requests), max_requests
    
    def cleanup(self, older_than_seconds: int = 3600) -> int:
        """
        Remove old request tracking data to prevent memory growth.
        
        Args:
            older_than_seconds: Remove data older than this (default: 1 hour)
        
        Returns:
            Number of identifiers cleaned up
        """
        now = time.time()
        cutoff_time = now - older_than_seconds
        cleaned = 0
        
        for identifier in list(self.requests.keys()):
            paths = self.requests[identifier]
            for path in list(paths.keys()):
                paths[path] = [ts for ts in paths[path] if ts > cutoff_time]
                
                if not paths[path]:
                    del paths[path]
            
            if not paths:
                del self.requests[identifier]
                cleaned += 1
        
        return cleaned


_rate_limiter = SlidingWindowRateLimiter()


class RateLimitMiddleware:
    """
    FastAPI middleware for rate limiting requests.
    
    - Extracts client IP from request
    - Checks rate limits using sliding window algorithm
    - Returns 429 (Too Many Requests) if limit exceeded
    - Includes X-RateLimit headers in response
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        if not request.url.path.startswith("/api") and not request.url.path.startswith("/auth"):
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        is_allowed, requests_made, limit = _rate_limiter.is_allowed(client_ip, request.url.path)
        
        if not is_allowed:
            logger.warning(
                f"Rate limit exceeded",
                extra={
                    "client_ip": client_ip,
                    "path": request.url.path,
                    "requests_made": requests_made,
                    "limit": limit
                }
            )
            
            return JSONResponse(
                status_code=HttpStatusCode.TOO_MANY_REQUESTS,
                content={
                    "success": False,
                    "message": "Too many requests. Please try again later.",
                    "error_code": ErrorCode.RATE_LIMIT_EXCEEDED,
                    "data": None
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                }
            )
        
        response = await call_next(request)
        
        remaining = limit - requests_made
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        if requests_made % 1000 == 0:
            cleaned = _rate_limiter.cleanup()
            if cleaned > 0:
                logger.debug(f"Rate limiter cleanup: removed {cleaned} identifiers")
        
        return response
