#File nay duoc tao o video 2.Chapter 11
# Ly do phai tao JsonRenderer vi serializers o users ko tra ve json
# JsonRenderer tra ve json theo format json, co status_code va object_label
# object_label co the la users, profiles v.v...
# Dang tra ve se la:
# object_label trong json nay la profiles
"""
    "status_code": 200,
    "profiles": {
        "count": 4,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "96d60bab-54db-48c2-953b-cdb1db59910e",
                "slug": "member4",
                "first_name": "Member",
                "last_name": "Four",
                "username": "member4",
                "full_name": "Member Four",
                "gender": "",
                "occupation": "tenant",
                "avatar": "http://res.cloudinary.com/bangdigi/image/upload/v1732099449/i98n78nk37ebfx79qkpv.jpg",
                "bio": "",
                "phone_number": "",
                "country_of_origin": "Vietnam",
                "city_of_origin": "",
                "report_count": 0,
                "reputation": 100,
                "date_joined": "2024-11-19T11:33:12.611485Z"
            },
            ...
        ]
    }

"""
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