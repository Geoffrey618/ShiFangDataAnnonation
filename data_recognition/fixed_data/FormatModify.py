import json

# 输入的JSON文件路径
input_file_path = 'UnModifiedFinalResult.json'
# 输出的JSON文件路径
output_file_with_origin_path = 'ModifiedFinalResult_with_origin.json'
# 输出的JSON文件路径（没有 origin data）
output_file_without_origin_path = 'ModifiedFinalResult_without_origin.json'

def transform_data(input_data):
    transformed_data = []

    for item in input_data:
        transformed_item = {
            "image_info": {
                "image_url": f"../{item['image_info']['image_url']}"
            },
            "messages": []
        }

        for message in item["messages"]:
            transformed_item["messages"].append({
                "role": "user",
                "content": message["question"]
            })
            transformed_item["messages"].append({
                "role": "assistant",
                "content": message["answer"],
                "fixed_content": message["fixed_answer"]
            })

        transformed_data.append(transformed_item)

    return transformed_data

def transform_data_without_origin(input_data):
    transformed_data = []

    for item in input_data:
        transformed_item = {
            "image_info": {
                "image_url": f"../{item['image_info']['image_url']}"
            },
            "messages": []
        }

        for message in item["messages"]:
            transformed_item["messages"].append({
                "role": "user",
                "content": message["question"]
            })
            transformed_item["messages"].append({
                "role": "assistant",
                "content": message["fixed_answer"]
            })

        transformed_data.append(transformed_item)

    return transformed_data

def main():
    # 读取输入的JSON文件
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)

    # 转换数据
    transformed_data_with_origin = transform_data(input_data)
    transformed_data_without_origin = transform_data_without_origin(input_data)

    # 写入输出的JSON文件（包含原始内容）
    with open(output_file_with_origin_path, 'w', encoding='utf-8') as output_file_with_origin:
        json.dump(transformed_data_with_origin, output_file_with_origin, ensure_ascii=False, indent=4)

    # 写入输出的JSON文件（不包含原始内容）
    with open(output_file_without_origin_path, 'w', encoding='utf-8') as output_file_without_origin:
        json.dump(transformed_data_without_origin, output_file_without_origin, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()