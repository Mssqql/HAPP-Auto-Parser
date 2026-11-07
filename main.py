

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

        text = data.decode("utf-8", errors="replace")

        if not any(p in text.lower() for p in PROTOCOLS):
            try:
                decoded = base64.b64decode(text.strip(), validate=True)
                text = decoded.decode("utf-8", errors="replace")
            except Exception:
                pass

        return text

    except Exception as error:
        print(f"Ошибка загрузки: {error}")
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

    if sources.exists():
        urls = [
            line.strip()
            for line in sources.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        print(f"Источников: {len(urls)}")

        for url in urls:
            print(f"Обработка: {url}")
            content = fetch_source(url)
            links = parse_links(content)
            print(f"Найдено строк: {len(links)}")
            all_links.extend(links)

    unique_links = list(dict.fromkeys(all_links))

    if unique_links:
        output_text = "\n".join(unique_links)
    else:
        output_text = "Источники не добавлены или данные не найдены."

    Path(OUTPUT_FILE).write_text(
        output_text,
        encoding="utf-8"
    )

    print("========== ИТОГ ==========")
    print(f"Всего найдено: {len(unique_links)}")
    print(f"Файл создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

