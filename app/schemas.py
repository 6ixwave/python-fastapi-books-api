from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class HealthRead(BaseModel):
    status: str = "ok"
    database: str = "connected"


class CategoryBase(BaseModel):
    title: str = Field(min_length=2, max_length=100, examples=["Backend"])

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        return " ".join(value.split())


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str = Field(
        min_length=2, max_length=200, examples=["Designing Maintainable APIs"]
    )
    description: str = Field(
        min_length=5,
        max_length=5000,
        examples=["Practical patterns for reliable web services"],
    )
    price: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2, examples=[Decimal("1490.00")]
    )
    url: HttpUrl = Field(examples=["https://example.com/book"])
    category_id: int = Field(gt=0, examples=[1])


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
