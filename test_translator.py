import pytest
from translator import parse_config
import toml

# 1. Тест на корректное преобразование простого словаря
def test_simple_dict():
    input_data = """
    {
      key1: 123,
      key2: 'value'
    }
    """
    expected_output = {
        "key1": 123,
        "key2": "value"
    }
    assert parse_config(input_data) == expected_output

# 2. Тест на вложенные словари
def test_nested_dict():
    input_data = """
    {
      outer: {
        inner1: 42,
        inner2: 'text'
      }
    }
    """
    expected_output = {
        "outer": {
            "inner1": 42,
            "inner2": "text"
        }
    }
    assert parse_config(input_data) == expected_output

# 3. Тест на константы
def test_constants():
    input_data = """
    var host = 'localhost';
    var port = 8080;

    {
      server: {
        address: |host|,
        port: |port|
      }
    }
    """
    expected_output = {
        "server": {
            "address": "localhost",
            "port": 8080
        }
    }
    assert parse_config(input_data) == expected_output

# 4. Тест на некорректное объявление констант
def test_invalid_constant():
    input_data = """
    var = 'localhost';
    """
    with pytest.raises(SyntaxError, match="Некорректное объявление константы"):
        parse_config(input_data)

# 5. Тест на неизвестную константу
def test_unknown_constant():
    input_data = """
    {
      address: |unknown_const|
    }
    """
    with pytest.raises(SyntaxError, match="Неизвестная константа: unknown_const"):
        parse_config(input_data)

# 6. Тест на некорректный ключ словаря
def test_invalid_key():
    input_data = """
    {
      key-1: 123
    }
    """
    with pytest.raises(SyntaxError, match="Некорректное имя ключа: key-1"):
        parse_config(input_data)

# 7. Тест на пустой словарь
def test_empty_dict():
    input_data = """
    {
    }
    """
    expected_output = {}
    assert parse_config(input_data) == expected_output

# 8. Тест на смешанные типы значений
def test_mixed_types():
    input_data = """
    {
      str_key: 'value',
      int_key: 123,
      nested: { inner_key: 'inner_value' }
    }
    """
    expected_output = {
        "str_key": "value",
        "int_key": 123,
        "nested": {
            "inner_key": "inner_value"
        }
    }
    assert parse_config(input_data) == expected_output
