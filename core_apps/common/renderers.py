#File nay duoc tao o video 2.Chapter 11
# Ly do phai tao JsonRenderer vi serializers o users ko tra ve json
# JsonRenderer tra ve json theo format json, co status_code va object_label
# object_label co the la users, profile v.v...
import json
from typing import Any, Optional, Union
from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer

class GenericJsonRenderer(JSONRenderer):
    charset = "utf-8"
    object_label = _("object")
    media_type = "application/json"
    format = "json"

    def render(self, data: Any, accepted_media_type: Optional[str] = None, renderer_context: Optional[dict] = None) -> Union[str, bytes]:
        if renderer_context is None:
            renderer_context = {}
        view = renderer_context.get("view")
        if hasattr(view, "object_label"):
            object_label = view.object_label
        else:
            object_label = self.object_label
        
        response = renderer_context.get("response")
        if not response:
            raise ValueError(
                _("Response not found in rendered context")
            )
        status_code = response.status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(GenericJsonRenderer, self).render(data)

        return json.dumps({
            "status_code": status_code,
            object_label: data
        }).encode(self.charset)