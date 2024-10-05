from rest_framework.permissions import IsAuthenticated


def authentication(action: str) -> list:
    if action in ['create', 'destroy', 'update', 'partial_update']:
        return [IsAuthenticated()]
    return []
