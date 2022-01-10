"""Pagination token client."""
import logging
from base64 import urlsafe_b64decode, urlsafe_b64encode

logger = logging.getLogger(__name__)


class PaginationTokenClient:
    """Pagination token operations."""

    def to_token(self, keyset: str) -> str:  # type:ignore
        """Transform a keyset to a token."""
        # for now just encode the keyset and return it
        return urlsafe_b64encode(
            keyset.encode(encoding="utf-8", errors="strict")
        ).decode("utf-8")

    def from_token(self, token_id: str) -> str:
        """Transform a token to a keyset."""
        return urlsafe_b64decode(token_id).decode("utf-8")