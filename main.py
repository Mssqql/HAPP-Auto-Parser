
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
    Path(OUTPUT_FILE).write_text("", encoding="utf-8")

    sources = Path(INPUT_FILE)
    all_links = []

    sample = Path("sample.txt")
    if sample.exists():
        test_content = sample.read_text(encoding="utf-8")
        all_links.extend(parse_links(test_content))

    if sources.exists():
        for url in sources.read_text(encoding="utf-8").splitlines():
            url = url.strip()
            if not url or url.startswith("#"):
                continue

            print(f"Обработка: {url}")
            content = fetch_source(url)
            all_links.extend(parse_links(content))

    unique_links = list(dict.fromkeys(all_links))

    Path(OUTPUT_FILE).write_text(
        "\n".join(unique_links),
        encoding="utf-8"
    )

    print(f"Готово! Найдено ссылок: {len(unique_links)}")


if __name__ == "__main__":
    main()


