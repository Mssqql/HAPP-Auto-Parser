
import urllib.request
import base64
import re
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

        # Поддержка Base64-подписок
        if not any(p in text.lower() for p in PROTOCOLS):
            try:
                decoded = base64.b64decode(
                    text.strip(), validate=True
                )
                text = decoded.decode("utf-8", errors="replace")
            except Exception:
                pass

        return text

    except Exception as error:
        print(f"Ошибка источника: {error}")
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
    output = Path(OUTPUT_FILE)

    if not sources.exists():
        sources.write_text("", encoding="utf-8")

    all_links = []

    for url in sources.read_text(encoding="utf-8").splitlines():
        url = url.strip()

        if not url or url.startswith("#"):
            continue

        print(f"Обработка: {url}")
        content = fetch_source(url)
        all_links.extend(parse_links(content))

    unique_links = list(dict.fromkeys(all_links))

    output.write_text(
        "\n".join(unique_links),
        encoding="utf-8"
    )

    print(f"Готово! Найдено ссылок: {len(unique_links)}")


if __name__ == "__main__":
    main()

