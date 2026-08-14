import os
import socket
import ipaddress
import logging
from urllib.parse import urlparse

import httpx

logger = logging.getLogger("soromais")

# Hosts the server is allowed to fetch images from. Defaults to Supabase
# Storage (where uploaded animal photos live). Override via ALLOWED_IMAGE_HOSTS
# (comma separated, supports "*.example.com" wildcards).
_DEFAULT_ALLOWED_HOSTS = ["*.supabase.co", "*.supabase.in"]

MAX_IMAGE_BYTES = int(os.getenv("MAX_IMAGE_BYTES", str(5 * 1024 * 1024)))


def _allowed_hosts() -> list[str]:
    raw = os.getenv("ALLOWED_IMAGE_HOSTS")
    if raw:
        return [h.strip().lower() for h in raw.split(",") if h.strip()]
    return list(_DEFAULT_ALLOWED_HOSTS)


def _host_allowed(hostname: str, allowed: list[str]) -> bool:
    hostname = hostname.lower()
    for pattern in allowed:
        if pattern.startswith("*."):
            suffix = pattern[1:]  # ".example.com"
            if hostname == pattern[2:] or hostname.endswith(suffix):
                return True
        elif hostname == pattern:
            return True
    return False


def _is_private(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def safe_fetch(url: str, max_bytes: int = MAX_IMAGE_BYTES, timeout: int = 10) -> bytes | None:
    """Fetch a URL defensively against SSRF.

    - scheme restricted to http/https
    - hostname must be on the allowlist
    - all resolved IPs must be public (no private/loopback/link-local/...)
    - redirects are disabled (prevents DNS-rebinding / internal hop after check)
    - content-type must be an image
    - response body is capped at max_bytes
    """
    allowed = _allowed_hosts()
    try:
        parsed = urlparse(url)
    except ValueError:
        logger.warning("Blocked fetch: malformed URL")
        return None

    if parsed.scheme not in ("http", "https"):
        logger.warning("Blocked fetch: unsupported scheme %r", parsed.scheme)
        return None

    host = parsed.hostname
    if not host:
        logger.warning("Blocked fetch: missing host")
        return None
    if not _host_allowed(host, allowed):
        logger.warning("Blocked fetch: host not allowlisted: %s", host)
        return None

    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port)
    except socket.gaierror as exc:
        logger.warning("Blocked fetch: DNS resolution failed for %s: %s", host, exc)
        return None

    for info in infos:
        ip = info[4][0]
        if _is_private(ip):
            logger.warning("Blocked fetch: resolves to non-public IP %s (%s)", ip, host)
            return None

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=False,
            headers={"User-Agent": "SoroMais/1.0"},
        ) as client:
            with client.stream("GET", url) as resp:
                if resp.status_code != 200:
                    logger.warning("Blocked fetch: unexpected status %s", resp.status_code)
                    return None
                ctype = resp.headers.get("content-type", "")
                if not ctype.startswith("image/"):
                    logger.warning("Blocked fetch: non-image content-type %r", ctype)
                    return None
                data = b""
                for chunk in resp.iter_bytes():
                    data += chunk
                    if len(data) > max_bytes:
                        logger.warning("Blocked fetch: response exceeded %d bytes", max_bytes)
                        return None
                return data
    except Exception as exc:
        logger.warning("Fetch failed: %s", exc)
        return None
