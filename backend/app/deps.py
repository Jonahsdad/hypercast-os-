from collections.abc import Iterator
from contextlib import contextmanager

from .domain.repository import InMemoryForecastRepository
from .domain.service import ForecastService

# In a real system this would be a session-based or request-scoped dependency.
# For now we use a single in-memory repo instance.


_repo = InMemoryForecastRepository()
_service = ForecastService(repository=_repo)


def get_forecast_service() -> ForecastService:
    return _service


@contextmanager
def service_context() -> Iterator[ForecastService]:
    # Placeholder for future DB/session lifecycle control
    yield _service
