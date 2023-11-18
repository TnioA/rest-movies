import json
from typing import Any, Dict, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import swagger_ui_default_parameters
from starlette.responses import HTMLResponse

def get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
    swagger_js_standalone_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-standalone-preset.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Optional[str] = None,
    init_oauth: Optional[Dict[str, Any]] = None,
    swagger_ui_parameters: Optional[Dict[str, Any]] = None,
    custom_js_url: Optional[str] = None,
) -> HTMLResponse:
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    """
    
    if custom_js_url:
        html += f"""
        <script src="{custom_js_url}"></script>
        """

    html += f"""
    <script src="{swagger_js_url}"></script>
    <script src="{swagger_js_standalone_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
        'urls.primaryName': 'V1',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIStandalonePreset
    ],
    plugins: [
        SwaggerUIBundle.plugins.DownloadUrl
    ]
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)



# const ui = SwaggerUIBundle({{
#     version: '3.1.6',
#     urls: [
#         {{ url: '/swagger.json', name: 'V1' }},
#         {{ url: '/swagger.json', name: 'V2' }},
#     ],
#     'urls.primaryName': 'V1',
#     dom_id: '#swagger-ui',
#     deepLinking: true,
#     presets: [
#         SwaggerUIBundle.presets.apis,
#         SwaggerUIStandalonePreset
#     ],
#     plugins: [
#         SwaggerUIBundle.plugins.DownloadUrl
#     ],
#     layout: 'StandaloneLayout',
#     supportedSubmitMethods: []
# }})