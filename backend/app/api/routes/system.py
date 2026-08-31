"""System and service-status endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/")
def root() -> dict[str, str]:
    """Return a minimal service identity response."""
    return {"message": "Cynlith API"}


@router.get("/health")
def health() -> dict[str, str]:
    """Return the service liveness status."""
    return {"status": "ok"}
