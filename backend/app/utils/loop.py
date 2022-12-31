from typing import Optional, Callable, Awaitable
from starlette.concurrency import run_in_threadpool
from traceback import format_exception
from asyncio import ensure_future
import logging, asyncio


def repeat_every(    
    func: Callable,
    args: list,
    *,
    seconds: float,
    wait_first: bool = False,
    logger: Optional[logging.Logger] = None,
    raise_exceptions: bool = False,
    max_repetitions: Optional[int] = None,
) -> None:

    is_coroutine = asyncio.iscoroutinefunction(func)

    repetitions = 0

    async def loop() -> None:
        nonlocal repetitions
        if wait_first:
            await asyncio.sleep(seconds)
        while max_repetitions is None or repetitions < max_repetitions:
            try:
                if is_coroutine:
                    await func(*args)  # type: ignore
                else:
                    await run_in_threadpool(func, *args)
                repetitions += 1
            except Exception as exc:
                if logger is not None:
                    formatted_exception = "".join(format_exception(type(exc), exc, exc.__traceback__))
                    logger.error(formatted_exception)
                if raise_exceptions:
                    raise exc
            await asyncio.sleep(seconds)

    ensure_future(loop())