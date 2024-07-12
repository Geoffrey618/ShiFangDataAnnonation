import os
import json
from http import HTTPStatus
import dashscope
from natsort import natsorted

# 设置API相关信息
API_KEY = "YOUR_API_KEY"

# 定义问题模板
questions_templates = {
    "food_identification": [
        "这是什么食物？", "这个食物是什么？", "你能告诉我这是哪种食物吗？", "这是什么东西？",
        "这个食物叫什么名字？", "这种食物是什么？", "这个食物是什么东西？", "你知道这是什么食物吗？",
        "这个食物是什么东西？", "你知道这个食物叫什么名字？"
    ],
    "quantity_inquiry": [
        "这里有几个这种食物？", "这个食物有多少份？", "你知道这里有多少这种食物吗？", "数量是多少？",
        "这种食物的数量是多少？", "这种食物有多少？", "你知道这是多少食物吗？", "这个食物有多少个？",
        "你知道这种食物有多少吗？", "有多少食物？"
    ],
    "weight_inquiry": [
        "它们的重量大约是多少？", "这种食物大概有多重？", "你知道它们的重量吗？", "重量是多少？",
        "这种食物的重量是多少？", "这种食物有多重？", "你知道这种食物的重量吗？", "这种食物重多少？",
        "它们的重量是多少？", "这种食物大概有多少？"
    ],
    "nutritional_value": [
        "这种食物有什么营养价值？", "能告诉我一些关于这种食物的营养信息吗？", "这种食物对健康有什么好处？",
        "这种食物包含哪些营养成分？", "它有什么营养价值？", "能说说这种食物的营养价值吗？",
        "这种食物的营养成分是什么？", "能说说这种食物对身体的好处吗？", "这种食物有哪些营养成分？",
        "你知道这种食物的营养成分吗？"
    ],
    "recipe_recommendations": [
        "你能推荐一些这种食物的做法吗？", "有没有关于这种食物的烹饪建议？", "你知道怎么样把这种食物做得好吃吗？",
        "能告诉我一些关于这种食物的烹饪方法吗？", "你有没有这种食物的烹饪技巧？", "能不能说说这种食物的制作方法？",
        "你知道这种食物的制作技巧吗？", "能不能告诉我怎样烹饪这种食物？", "有什么建议关于这种食物的烹饪？",
        "能不能说说怎样把这种食物变得美味？"
    ]
}

# 定义请求函数
def send_request(image_path, text):
    # 检查文件是否存在并可读
    if not os.path.isfile(image_path) or not os.access(image_path, os.R_OK):
        print(f"Error: Cannot access file - {image_path}")
        return None

    # 创建正确的文件路径格式
    local_file_path = f"file://{os.path.abspath(image_path)}"
    messages = [
        {
            "role": "user",
            "content": [
                {"image": local_file_path},
                {"text": text}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(
        model='qwen-vl-plus',
        api_key=API_KEY,  # 如果没有设置环境变量，请在此处填写 API Key
        messages=messages
    )

    if response.status_code == HTTPStatus.OK:
        return response.output
    else:
        print(f"Error: {response.code}, {response.message}")
        return None

# 定义循环调用函数
def process_images():
    image_dir = "./images"
    response_dir = "./origin_data"
    os.makedirs(response_dir, exist_ok=True)
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
    sorted_image_files = natsorted(image_files)  # 自然排序

    for idx, image_file in enumerate(sorted_image_files):
        image_path = os.path.join(image_dir, image_file)
        responses = []
        for key in questions_templates:
            question = questions_templates[key][idx % len(questions_templates[key])]
            response = send_request(image_path, question)
            if response:
                responses.append({"question": question, "response": response})
        if responses:
            with open(os.path.join(response_dir, f"response{idx + 1}.json"), 'w', encoding='utf-8') as f:
                json.dump(responses, f, ensure_ascii=False, indent=4)
            print(f"Processed {image_file}")
        else:
            print(f"Skipped {image_file} due to accessibility issues")

# 执行处理
if __name__ == "__main__":
    process_images()