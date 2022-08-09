"""TarkovBot's Utility File"""

# Built-in Modules
import asyncio

__all__ = (
    "get_asyncio_event_loop",
)


def get_asyncio_event_loop() -> asyncio.AbstractEventLoop:
    """Gets the running event loop or creates a new one if one is not running."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()
