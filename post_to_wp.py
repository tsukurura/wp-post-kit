import json
import requests
import sys
from pathlib import Path

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def parse_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    title = lines[0].strip().replace("# ", "")
    content = "".join(lines[1:])
    return title, content

def post_to_wordpress(title, content, config):
    url = config["url"]
    user = config["user"]
    app_pass = config["app_password"]

    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "content": content,
        "status": "draft"
    }
    response = requests.post(
        f"{url}/wp-json/wp/v2/posts",
        headers=headers,
        auth=(user, app_pass),
        json=data
    )
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_to_wp.py <markdown_file>")
        sys.exit(1)

    config = load_config()
    title, content = parse_markdown(sys.argv[1])
    post_to_wordpress(title, content, config)