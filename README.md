# ShifangDataAnnotation

### 使用方法：

将待处理图片移至images文件夹中，启动rename_images.py对所有待处理队列中的图片进行重命名操作；

启动images_process.py，通过修改questions_templates中的内容调整问题库，将API_KEY设置为通过阿里平台所申请到的API_KEY，修改dashscope请求体中model的值，调用不同模型进行提问，返回值以resposneN.json(N与image编号相同)形式保存在origin_data目录下；

启动DataAnnotations.py，进行数据标注。相应图片会在页面左侧显示，修改”修正答案“框内的值，点击保存修改后将对应字段的值写入fixed_data目录下对应的fix_dataN.json中。
