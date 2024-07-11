# ShifangDataAnnotation

> 基于QwenVL的多模态大模型调用和数据标注工具

### 使用方法：

1. 将待处理图片移动至**images**目录下，使用命令`python rename_images.py`对所有待处理的图片进行**编号重命名**操作；
2. 修改**questions_templates**中的问题库，将**API_KEY**替换为个人申请到的API_KEY，通过修改**dashscope请求体**中**model**的值，执行命令`python images_process.py`，调用不同模型进行提问，返回的数据将以**resposneN.json**(N与image编号相同)的形式保存在**origin_data**目录下；

3. 执行命令`python DataAnnotationsTool.py`，进行数据标注。相应图片会在页面左侧显示，对比参考数据进行人工校验，修改”修正答案“框内的值，点击**保存修改**后将对应字段的值写入**fixed_data**目录下对应的**fix_dataN.json**中;
4. 

