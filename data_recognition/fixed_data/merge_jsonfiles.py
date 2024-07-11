import os
import json

def merge_json_files(output_filename='FinalResult.json'):
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('fixed_data')]
    merged_data = []

    for file_name in json_files:
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    item_dict = {"image_info": {}, "messages": []}
                    for item in data:
                        if "image_number" in item and "image_url" in item:
                            item_dict["image_info"]["image_number"] = item["image_number"]
                            item_dict["image_info"]["image_url"] = item["image_url"]
                        else:
                            item_dict["messages"].append(item)
                    merged_data.append(item_dict)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file_name}")

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

    print("json文件已合并完成")

if __name__ == '__main__':
    merge_json_files()