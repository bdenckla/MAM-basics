import json

file_path = r'in\mam-ws\A1-Genesis.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

first_chapter_key = next(iter(data.keys()))
print(f"First chapter key: '{first_chapter_key}', Type: {type(first_chapter_key)}")

first_chapter_content = data[first_chapter_key]
if isinstance(first_chapter_content, list):
    print(f"Chapter content is a list of length {len(first_chapter_content)}")
    if len(first_chapter_content) > 0:
        first_item = first_chapter_content[0]
        print(f"First item type: {type(first_item)}")
        if isinstance(first_item, dict):
            first_verse_key = next(iter(first_item.keys()))
            print(f"First verse key: '{first_verse_key}', Type: {type(first_verse_key)}")
        else:
            print("First item is not a dictionary.")
elif isinstance(first_chapter_content, dict):
    first_verse_key = next(iter(first_chapter_content.keys()))
    print(f"First verse key: '{first_verse_key}', Type: {type(first_verse_key)}")
