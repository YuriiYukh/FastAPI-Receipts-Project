
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.models import Receipt, Product, User

router = APIRouter()

# Ініціалізація JwtAccessBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ProductItem(BaseModel):
    name: str
    price: float
    quantity: int


class ReceiptCreate(BaseModel):
    products: List[ProductItem]
    payment_type: str
    payment_amount: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    Used for checking user auth for the endpoints
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    return username


@router.post("/", summary="Create a new receipt")
async def create_receipt(
    receipt: ReceiptCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''
    Used for creating receipt for an authed users
    '''
    total_price = sum(
        item.price * item.quantity for item in receipt.products)

    if receipt.payment_amount < total_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Insufficient payment amount")

    rest = receipt.payment_amount - total_price

    new_receipt = Receipt(
        user_id=current_user,
        payment_type=receipt.payment_type,
        payment_amount=receipt.payment_amount,
        total=total_price,
        rest=rest
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    for item in receipt.products:
        product = Product(
            receipt_id=new_receipt.id,
            name=item.name,
            price=item.price,
            quantity=item.quantity,
            total=item.price * item.quantity
        )
        db.add(product)
    db.commit()

    response = {
        "id": new_receipt.id,
        "products": [{"name": item.name, "price": item.price, "quantity": item.quantity, "total": item.price * item.quantity} for item in receipt.products],
        "payment": {
            "type": receipt.payment_type,
            "amount": receipt.payment_amount
        },
        "total": total_price,
        "rest": rest,
        "created_at": new_receipt.created_at
    }

    return response


@router.get("/", summary="Get list of receipts")
async def get_receipts(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    '''
    Used for getting the recipes for an authenticated user
    '''
    receipts = db.query(Receipt).filter(Receipt.user_id ==
                                        current_user).offset(skip).limit(limit).all()

    response = [
        {
            "id": receipt.id,
            "total": receipt.total,
            "payment": {
                "type": receipt.payment_type,
                "amount": receipt.payment_amount
            },
            "rest": receipt.rest,
            "created_at": receipt.created_at
        }
        for receipt in receipts
    ]

    return {"receipts": response}


@router.get("/receipt/{receipt_id}/view", summary="View receipt in text format")
async def view_receipt(receipt_id: int, db: Session = Depends(get_db), line_width: int = 40):
    '''
    Formatted view of a recipe
    line_width - allows to configure max symbols quantity in every line
    Can be accessed without the auth, as per task
    '''
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    header = "ФОП Джонсонюк Борис".center(line_width)
    separator = "=" * line_width
    lines = [header, separator]

    products = db.query(Product).filter(Product.receipt_id == receipt.id).all()
    for product in products:
        product_line = f"{product.quantity} x {product.price:.2f}"
        lines.append(product_line)
        lines.append(product.name.ljust(line_width // 2) +
                     f"{product.total:.2f}".rjust(line_width // 2))

        lines.append("-" * line_width)

    total_line = f"СУМА {receipt.total:.2f}".rjust(line_width)
    payment_line = f"{receipt.payment_type.capitalize(
    )} {receipt.payment_amount:.2f}".rjust(line_width)
    rest_line = f"Решта {receipt.rest:.2f}".rjust(line_width)
    date_line = receipt.created_at.strftime(
        "%d.%m.%Y %H:%M").center(line_width)
    thank_you_line = "Дякуємо за покупку!".center(line_width)

    lines.extend([total_line, payment_line, rest_line,
                 separator, date_line, thank_you_line])

    receipt_text = "\n".join(lines)
    return {"receipt_text": receipt_text}
