from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_response import StreamResponse


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if getattr(self.request, 'admin', None) is None:
            raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()
