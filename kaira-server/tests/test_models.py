# tests/test_models.py
import pytest
from pydantic import ValidationError
from app.models import Item

def test_item_valid():
    """올바른 데이터 검증"""
    item = Item(name="책", price=15000, quantity=3)
    assert item.name == "책"
    assert item.price == 15000
    assert item.quantity == 3

def test_item_invalid_price():
    """잘못된 가격 검증"""
    with pytest.raises(ValidationError) as exc_info:
        Item(name="책", price=-1000)
  
    errors = exc_info.value.errors()
    assert any(err['loc'] == ('price',) for err in errors)

def test_item_empty_name():
    """빈 이름 검증"""
    with pytest.raises(ValidationError) as exc_info:
        Item(name="   ", price=1000)
  
    assert "이름은 공백일 수 없습니다" in str(exc_info.value)

@pytest.mark.parametrize("name,price,should_pass", [
    ("책", 1000, True),
    ("", 1000, False),
    ("책", 0, False),
    ("책", -100, False),
    ("A" * 51, 1000, False),  # 너무 긴 이름
])
def test_item_validation(name, price, should_pass):
    """매개변수화 검증 테스트"""
    if should_pass:
        item = Item(name=name, price=price)
        assert item.name == name.strip()
    else:
        with pytest.raises(ValidationError):
            Item(name=name, price=price)

