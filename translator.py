import argparse
import re
import sys
import toml

def parse_config(content):
    """
    Парсит текст на учебном конфигурационном языке и возвращает словарь.
    """
    constants = {}
    result = {}

    def replace_constants(value):
        # Заменяет константы по имени на их значения
        if value.startswith("|") and value.endswith("|"):
            const_name = value.strip("|")
            if const_name in constants:
                return constants[const_name]
            else:
                raise SyntaxError(f"Неизвестная константа: {const_name}")
        return value

    def parse_value(value):
        # Определяет тип значения: число, строка, словарь или константа
        value = value.strip()
        if value.isdigit():  # Число
            return int(value)
        elif value.startswith("'") and value.endswith("'"):  # Строка
            return value.strip("'")
        elif value.startswith("{") and value.endswith("}"):  # Словарь
            return parse_dict(value)
        else:  # Попытка заменить константу
            return replace_constants(value)

    def parse_dict(content):
        # Парсит словарь
        content = content.strip("{}").strip()
        pairs = [pair.strip() for pair in content.split(",") if pair.strip()]
        result = {}
        for pair in pairs:
            if ":" not in pair:
                raise SyntaxError(f"Некорректная пара: {pair}")
            key, value = pair.split(":", 1)
            key = key.strip()
            if not re.fullmatch(r"[a-z_]+", key):
                raise SyntaxError(f"Некорректное имя ключа: {key}")
            result[key] = parse_value(value)
        return result

    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Игнорируем пустые строки и комментарии
            continue
        if line.startswith("var "):  # Обработка объявления констант
            match = re.match(r"var\s+([a-z]+)\s*=\s*(.+);", line)
            if not match:
                raise SyntaxError(f"Некорректное объявление константы: {line}")
            const_name, const_value = match.groups()
            if not re.fullmatch(r"[a-z]+", const_name):
                raise SyntaxError(f"Некорректное имя константы: {const_name}")
            constants[const_name] = parse_value(const_value)
        else:  # Обработка словарей
            result.update(parse_dict(line))
    return result

def translate_to_toml(input_file):
    """
    Читает файл УКЯ, парсит и выводит результат в формате TOML.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        parsed_config = parse_config(content)
        toml_output = toml.dumps(parsed_config)
        print(toml_output)
    except (SyntaxError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Переводчик УКЯ в TOML.")
    parser.add_argument("input_file", help="Путь к файлу на учебном конфигурационном языке.")
    args = parser.parse_args()

    translate_to_toml(args.input_file)
