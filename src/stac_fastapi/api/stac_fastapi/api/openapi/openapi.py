from typing import Callable

from fastapi.applications import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse


class VndResponse(JSONResponse):
    media_type = "application/vnd.oai.openapi+json;version=3.0"


def get_openapi_handler(app: FastAPI) -> Callable[[Request], VndResponse]:
    def handler(req: Request):

        # OpenAPI spec must be modified because FastAPI doesn't support
        # encoding style: https://github.com/tiangolo/fastapi/issues/283
        definition = app.openapi().copy()
        # Delete bogus components that are not OGC compliant
        for component in list(definition["components"]["schemas"].keys()):
            if component not in ["HTTPValidationError", "ValidationError"]:
                print("deleting ", component)
                del definition["components"]["schemas"][component]

        # Delete bogus paths that are not OGC compliant
        for component in list(definition["paths"].keys()):
            if component in ["/_mgmt/ping"]:
                print("deleting ", component)
                del definition["paths"][component]

        for path in definition["paths"].values():
            # print(path)
            if "get" in path:
                if "parameters" in path["get"]:
                    for parameter in path["get"]["parameters"]:
                        if "style" not in parameter:
                            parameter["style"] = "form"

        collection_items_bbox_param = list(
            filter(
                lambda parameter: parameter["name"] == "bbox",
                definition["paths"][f"/collections/{{collectionId}}/items"]["get"][
                    "parameters"
                ],
            )
        )[0]
        collection_items_bbox_param["schema"] = {
            "type": "array",
            "minItems": 4,
            "maxItems": 6,
            "items": {
                "type": "number",
            },
        }

        return VndResponse(definition)

    return handler
