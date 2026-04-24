import time
import logging
import os
from collections import defaultdict
from typing import Dict, List, Tuple

from fastapi.responses import JSONResponse
from utils.error_codes import ErrorCode, HttpStatusCode

logger = logging.getLogger(__name__)


class RateLimitConfig:
    LIMITS = {
        "/auth/register": (3, 300),
        "/auth/login": (5, 300),
        "/auth/send-otp": (3, 600),
        "/auth/otp/send": (3, 600),
        "/auth/verify-otp": (5, 300),
        "/auth/otp/verify": (5, 300),
        "/auth/password/reset": (3, 1800),
        "/auth/password/verify": (5, 600),
        "/auth/refresh": (10, 300),
        "/auth/logout": (100, 300),

        "/resume/upload": (10, 300),
        "/resume/delete": (10, 300),
        "/api/resume/upload": (10, 300),
        "/api/resume/delete": (10, 300),

        "/api/analyseresume": (5, 60),
        "/api/jobmatching/analyse": (5, 60),
        "/question_gen/generate": (5, 60),
        "/api/interviewservice/question-gen": (5, 60),
        "/api/chat/send-message": (30, 60),
        "/api/chat/create-session": (10, 300),

        "/api/interview/start": (10, 300),
        "/api/interview/submit-answer": (50, 300),

        "/health": (1000, 60),
        "/docs": (100, 60),
        "/redoc": (100, 60),
    }

    DEFAULT_LIMIT = (100, 300)
    ENABLED = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"

    @staticmethod
    def get_limit(path: str) -> Tuple[int, int]:
        if path in RateLimitConfig.LIMITS:
            return RateLimitConfig.LIMITS[path]

        best_match = None
        best_limit = None

        for pattern, limit in RateLimitConfig.LIMITS.items():
            if path.startswith(pattern) and (best_match is None or len(pattern) > len(best_match)):
                best_match = pattern
                best_limit = limit

        return best_limit if best_limit else RateLimitConfig.DEFAULT_LIMIT


class SlidingWindowRateLimiter:
    def __init__(self):
        self.requests: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        self.stats = {
            "total_checks": 0,
            "rate_limit_exceeded": 0,
            "cleanup_runs": 0
        }

    def is_allowed(self, identifier: str, path: str) -> Tuple[bool, int, int]:
        self.stats["total_checks"] += 1
        now = time.time()
        max_requests, window_seconds = RateLimitConfig.get_limit(path)

        request_times = self.requests[identifier][path]

        cutoff_time = now - window_seconds
        valid_requests = [ts for ts in request_times if ts > cutoff_time]

        if len(valid_requests) >= max_requests:
            self.requests[identifier][path] = valid_requests
            self.stats["rate_limit_exceeded"] += 1
            return False, len(valid_requests), max_requests

        valid_requests.append(now)
        self.requests[identifier][path] = valid_requests

        return True, len(valid_requests), max_requests

    def cleanup(self, older_than_seconds: int = 3600) -> int:
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

        self.stats["cleanup_runs"] += 1
        return cleaned


_rate_limiter = SlidingWindowRateLimiter()


class RateLimitMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if not RateLimitConfig.ENABLED:
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")

        if not self._should_rate_limit(path):
            await self.app(scope, receive, send)
            return

        
        client_ip = self._get_client_ip(scope)

        is_allowed, requests_made, limit = _rate_limiter.is_allowed(client_ip, path)

        if not is_allowed:
            await self._send_rate_limit_response(send, limit)
            return

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                remaining = limit - requests_made
                headers = list(message.get("headers", []))
                headers.append((b"x-ratelimit-limit", str(limit).encode()))
                headers.append((b"x-ratelimit-remaining", str(max(0, remaining)).encode()))
                message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_with_headers)

        if _rate_limiter.stats["total_checks"] % 5000 == 0:
            _rate_limiter.cleanup()

    @staticmethod
    def _should_rate_limit(path: str) -> bool:
        return path.startswith(("/api", "/auth", "/question_gen", "/resume"))

    # 🔥 FULLY FIXED FUNCTION
    @staticmethod
    def _get_client_ip(scope) -> str:
        """
        Extract client IP from ASGI scope correctly
        """

        # Direct connection
        client = scope.get("client")
        if client:
            return client[0]  # (ip, port)

        # Headers (convert bytes → dict)
        headers = dict(scope.get("headers", []))

        # X-Forwarded-For
        forwarded_for = headers.get(b"x-forwarded-for")
        if forwarded_for:
            return forwarded_for.decode().split(",")[0].strip()

        return "unknown"

    @staticmethod
    async def _send_rate_limit_response(send, limit: int):
        response = JSONResponse(
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

        await response(scope=None, receive=None, send=send)


