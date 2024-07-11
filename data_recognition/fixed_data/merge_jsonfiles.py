import os
import json

def merge_json_files(output_filename='FinalResult.json'):
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('fixed_data')]
    merged_data = []

    for file_name in json_files:
        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    image_info = {
                        "image_number": data.get("image_number"),
                        "image_url": data.get("image_url"),
                        "messages": []
                    }
                    # Remove keys that are not questions
                    keys_to_remove = ["image_number", "image_url"]
                    for key in keys_to_remove:
                        if key in data:
                            del data[key]

                    # Add remaining data as messages
                    for question, answer_data in data.items():
                        if isinstance(answer_data, list):
                            for qa in answer_data:
                                image_info["messages"].append(qa)
                        else:
                            image_info["messages"].append(answer_data)

                    merged_data.append(image_info)
                elif isinstance(data, list):
                    merged_data.extend(data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file_name}")

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    merge_json_files()