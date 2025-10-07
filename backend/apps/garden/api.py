from typing import List
from django.utils import timezone
from ninja import Router

from .models import Garden, GardenPod
from .schemas import GardenSchema, PodSchema as GardenPodSchema

router = Router(tags=["gardens"])


@router.get("/", response=List[GardenSchema])
def get_gardens(request):
    gardens = Garden.objects.all()
    return gardens


@router.post("/", response=GardenSchema)
def create_garden(request, garden: GardenSchema):
    garden = Garden.objects.create(**garden.dict())
    garden.save()
    return garden


@router.get("/{garden_id}", response=GardenSchema)
def get(request, garden_id: int):
    return Garden.objects.get(pk=garden_id)


@router.put("/{garden_id}", response=GardenSchema)
def update_garden(request, garden_id: int, payload: GardenSchema):
    garden = Garden.objects.get(pk=garden_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(garden, attr, value)
    garden.updated_at = timezone.now()
    garden.save()
    return garden


@router.delete("/{garden_id}")
def delete_garden(request, garden_id: int):
    garden = Garden.objects.get(pk=garden_id)
    garden.delete()
    return {"status": "deleted"}


@router.get("/{garden_id}/pods/", response=List[GardenPodSchema])
def get_pods(request, garden_id: int):
    return GardenPod.objects.filter(garden_id=garden_id)


@router.post("/{garden_id}/pods/", response=GardenPodSchema)
def create_pod(request, garden_id: int, pod: GardenPodSchema):
    return GardenPod.objects.create(garden_id=garden_id, **pod.dict())


@router.get("/{garden_id}/pods/{pod_number}", response=GardenPodSchema)
def get_pod(request, garden_id: int, pod_number: int):
    return GardenPod.objects.get(garden_id=garden_id, pod_number=pod_number)
