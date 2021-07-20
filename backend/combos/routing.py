from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from . import consumers

# from combos.consumers import UploadConsumer


websocket_urlpatterns = [
    # path('combos/', consumers.ComboConsumer),
]

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter([
#             path('taxi/', consumers.ComboConsumer),
#         ])
#     )
# })