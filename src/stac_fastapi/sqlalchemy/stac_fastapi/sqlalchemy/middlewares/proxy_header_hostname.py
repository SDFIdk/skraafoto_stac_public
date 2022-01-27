"""
This middleware can be used when a known proxy is fronting the application,
and is trusted to be properly setting the `X-Forwarded-Proto` and
`X-Forwarded-For` headers with the connecting client information.

Modifies the `client` and `scheme` information so that they reference
the connecting client, rather that the connecting proxy.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Proxies

Original source: https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py
Altered to accomodate x-forwarded-host instead of x-forwarded-for
Altered: 27-01-2022
"""
from typing import List, Optional, Tuple, Union, cast
import logging

from starlette.types import ASGIApp, Receive, Scope, Send

Headers = List[Tuple[bytes, bytes]]


class ProxyHeadersMiddleware:
    def __init__(self, app, trusted_hosts: Union[List[str], str] = "127.0.0.1") -> None:
        self.app = app
        if isinstance(trusted_hosts, str):
            self.trusted_hosts = {item.strip() for item in trusted_hosts.split(",")}
        else:
            self.trusted_hosts = set(trusted_hosts)
        self.always_trust = "*" in self.trusted_hosts

    def get_trusted_client_host(
        self, x_forwarded_for_hosts: List[str]
    ) -> Optional[str]:
        if self.always_trust:
            return x_forwarded_for_hosts[0]

        for host in reversed(x_forwarded_for_hosts):
            if host not in self.trusted_hosts:
                return host

        return None

    def remap_headers(self, src: Headers, before: bytes, after: bytes) -> Headers:
        remapped = []
        before_value = None
        after_value = None
        for header in src:
            k, v = header
            if k == before:
                before_value = v
                continue
            elif k == after:
                after_value = v
                continue
            remapped.append(header)
        if after_value:
            remapped.append((before, after_value))
        elif before_value:
            remapped.append((before, before_value))
        return remapped

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] in ("http", "websocket"):

            client_addr: Optional[Tuple[str, int]] = scope.get("client")
            client_host = client_addr[0] if client_addr else None

            if self.always_trust or client_host in self.trusted_hosts:
                headers = dict(scope["headers"])
                if b"x-forwarded-proto" in headers:
                    # Determine if the incoming request was http or https based on
                    # the X-Forwarded-Proto header.
                    x_forwarded_proto = headers[b"x-forwarded-proto"].decode("latin1")
                    scope["scheme"] = x_forwarded_proto.strip()  # type: ignore[index]

                if b"x-forwarded-host" in headers:
                    # Determine the client hostname from the last trusted IP in the
                    # X-Forwarded-For header. We've lost the connecting client's port
                    # information by now, so only include the host.
                    x_forwarded_host = headers[b"x-forwarded-host"].decode("latin1")
                    x_forwarded_hosts = [
                        item.strip() for item in x_forwarded_host.split(",")
                    ]
                    host = self.get_trusted_client_host(x_forwarded_hosts)
                    port = 0
                    scope["client"] = (host, port)  # type: ignore[index]
                    scope["headers"] = self.remap_headers(
                        scope["headers"], b"host", b"x-forwarded-host"
                    )
                if b"x-forwarded-prefix" in headers:
                    x_forwarded_prefix = headers[b"x-forwarded-prefix"].decode("latin1")
                    scope["root_path"] = x_forwarded_prefix

        return await self.app(scope, receive, send)