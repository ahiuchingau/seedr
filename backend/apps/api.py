from django.db import connection
from django.utils import timezone
from ninja import NinjaAPI

api = NinjaAPI(title="Seedr", version="0.1.0", docs_url="/docs", csrf=False)


@api.get("health", tags=["health"])
def health(request) -> dict[str, str]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return {"status": "ok", "timestamp": timezone.now().isoformat()}
