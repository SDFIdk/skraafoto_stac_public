from typing import Dict

import attr
from stac_fastapi.types.links import BaseHrefBuilder


@attr.s
class ApiTokenHrefBuilder(BaseHrefBuilder):
    """Adds `token` param to all hrefs"""

    token: str = attr.ib()

    def build(self, path: str = None, query: Dict[str, str] = None):
        q = query or {}
        if self.token:
            q["token"] = self.token
        return super().build(path=path, query=q)