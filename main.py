

import urllib.request
import base64
from pathlib import Path

INPUT_FILE = "sources.txt"
OUTPUT_FILE = "result.txt"

PROTOCOLS = ("vless://", "vmess://", "trojan://", "ss://")


def fetch_source(url):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "HAPP-Auto-Parser/1.0"}
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read(2_000_000)
            print(f"  Получено данных: {len(data)} байт")

        text = data.decode("utf-8", errors="replace")

        if not any(p in text.lower() for p in PROTOCOLS):
            try:
                decoded = base64.b64decode(text.strip(), validate=True)
                text = decoded.decode("utf-8", errors="replace")
                print("  Данные декодированы из Base64")
            except Exception:
                print("  Base64-декодирование не выполнено")

        return text

    except Exception as error:
        print(f"  Ошибка загрузки: {error}")
        return ""


def parse_links(text):
    links = []

    for line in text.splitlines():
        line = line.strip()

        if line.lower().startswith(PROTOCOLS):
            links.append(line)

    return links


def main():
    sources = Path(INPUT_FILE)
    all_links = []

    if not sources.exists():
        print("ОШИБКА: sources.txt не найден")
    else:
        urls = [
            line.strip()
            for line in sources.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        print(f"Источников для обработки: {len(urls)}")

        for number, url in enumerate(urls, start=1):
            print(f"\nИсточник {number}: {url}")

            content = fetch_source(url)
            links = parse_links(content)

            print(f"  Найдено строк подходящего формата: {len(links)}")
            all_links.extend(links)

    unique_links = list(dict.fromkeys(all_links))

    Path(OUTPUT_FILE).write_text(
        "\n".join(unique_links),
        encoding="utf-8"
    )

    print("\n========== ИТОГ ==========")
    print(f"Всего найдено: {len(all_links)}")
    print(f"Уникальных строк: {len(unique_links)}")
    print(f"Файл создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
