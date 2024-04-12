from channels.db import database_sync_to_async
from accounts.models import User
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(slug):
    try:
        return User.objects.get(slug=slug)
    except User.DoesNotExist:
        return AnonymousUser()

class QueryAuthMiddleware:

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        query_slug = scope.get("query_string").decode("utf-8")
        slug = query_slug.split("=")
        
        scope['user'] = await get_user(slug[1])

        return await self.app(scope, receive, send)
