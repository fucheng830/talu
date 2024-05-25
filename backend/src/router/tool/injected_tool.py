from typing import Optional, Type, Any, Callable, Awaitable
from langchain_core.tools import Tool, AsyncCallbackManagerForToolRun, CallbackManagerForToolRun, \
    BaseModel


class InjectedTool(Tool):
    """
    A tool that allows for dependency injection of external resources like a database session.
    """

    def __init__(self, name: str, func: Optional[Callable], description: str, context: Any, **kwargs: Any):
        super().__init__(name, func, description, **kwargs)
        self.context = context  # Injecting the context into the tool.

    async def _arun(
        self,
        *args: Any,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Use the tool asynchronously, with access to injected dependencies like a database.
        """
        # Ensuring the database session is available in the function's context
        if self.coroutine:
            return await self.coroutine(*args, db=self.db, **kwargs)
        else:
            return await super()._arun(*args, run_manager=run_manager, **kwargs)

    def _run(
        self,
        *args: Any,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Use the tool synchronously, with access to injected dependencies like a database.
        """
        if self.func:
            return self.func(*args, db=self.db, **kwargs)
        else:
            return super()._run(*args, run_manager=run_manager, **kwargs)

    @classmethod
    def from_function(
        cls,
        func: Optional[Callable],
        name: str,
        description: str,
        db: Any,
        return_direct: bool = False,
        args_schema: Optional[Type[BaseModel]] = None,
        coroutine: Optional[Callable[..., Awaitable[Any]]] = None,
        **kwargs: Any,
    ) -> 'InjectedTool':
        """
        Initialize tool from a function with dependency injection.
        """
        return cls(
            name=name,
            func=func,
            coroutine=coroutine,
            description=description,
            db=db,
            return_direct=return_direct,
            args_schema=args_schema,
            **kwargs,
        )
