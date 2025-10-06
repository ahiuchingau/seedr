from ninja import Router

from .models import Garden

router = Router()


@router.get("/")
def list_gardens(request):
    return [{"id": g.id, "title": g.title} for g in Garden.objects.all()]


@router.get("/{garden_id}", response=Garden)
def garden_details(request, garden_id: int):
    garden = Garden.objects.get(id=garden_id)
    return garden.dict()
