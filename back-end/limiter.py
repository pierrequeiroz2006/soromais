from slowapi import Limiter
from slowapi.util import get_remote_address

# Single shared rate-limiter instance. Registered on app.state.limiter in main.py
# so the exception handler and storage are consistent across all routes.
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
