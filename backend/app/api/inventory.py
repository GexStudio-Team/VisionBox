from fastapi import APIRouter

from app.schemas.product import Product

router = APIRouter()

@router.get(
    "/inventory",
    response_model=list[Product],
    tags=["Inventory"],
    summary="Inventory",
    description="Returns the current inventory."
)

def get_inventory():
    return [
        Product(
            id=1,
            name="Coca-Cola 350ml",
            quanty=24,
        ),
        Product(
            id=2,
            name="Arroz Diana 500g",
            quanty=12,
        ),
    ]