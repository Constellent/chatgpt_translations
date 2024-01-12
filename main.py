'''
    Apifox Translations
    使用了此API接口制作的自动翻译脚本：https://rvvnzeghdn.apifox.cn/
    非自制，对此脚本进行的修改，十分感谢！：https://apifox.com/apiskills/python-gpt3-5/
'''

import os, requests, json

#==========================================================

# 数据
data = {
    "apiurl": "http://ai.tentech.top",
    "payload": {},
    "headers": {
        'Authorization': 'Bearer sk-7eLfqi1P7HpkQswwrRqULae0Ocbjru8plvZGtiM',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }
}

# 配置文件
config = {
    # Debug
    "Debug": False,
    # 翻译的时候是否下一行
    "AutoLineFeed": True,
    # 原文语种
    "source": "auto",
    # 目标翻译
    # chinese = zh
    "target": "zh",
    # 源文件
    "source_file": "hello.md",
    # 目标文件
    "target_file": "hello-zh.md"
}

#==========================================================

# 当前脚本所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))
print("当前脚本所在的目录路径：" + script_dir)

def get_markdown_file(source_file): 
    source_path = os.path.join(script_dir, source_file)
    print("源文件路径：" + source_path)
    
    # 读取源文件内容
    with open(source_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content

zh_text = get_markdown_file(config['source_file'])

# 调用翻译API将内容从英文翻译成中文
def get_completion(prompt):
    url = f"{data['apiurl']}/v1/text/translations?text={prompt}&source={config['source']}&target={config['target']}"
    response = requests.request("GET", url, headers = data["headers"], data = data["payload"])
    json_data = json.loads(response.text)
    return json_data["data"]

# 分割翻译的文本
segments = [line.strip() for line in zh_text.splitlines()]
translated_segments = []

print("分割完成，开始翻译")
# 逐段进行翻译
for i, segment in enumerate(segments):

    # Debug内容
    # 检测字典索引数和原文内容，用于检查是否有导致脚本错误的内容
    if (config["Debug"]):
        print(f"index: {i} | text: {segment}")

    # 当原文为空时，就直接换行跳过
    if (segment == "" or segment == None):
        translated_segments.append("\n")
        continue

    # 翻译
    response = get_completion(segment)
    translated_segments.append(segment)
    translated_segments.append(response)

    # 当翻译完后立刻换行
    if (config["AutoLineFeed"]):
        translated_segments.append("\n")
    
    # Debug内容
    # 在控制台实时显示翻译进度
    if (config["Debug"]):
        print(f"[Tran] 正在翻译第 {i + 1} 段，共 {len(segments)} 段. 剩余段数: {len(segments) - (i + 1)}.")

# 组合翻译后的文本
translated_content = "\n".join(translated_segments)

# 获取目录路径
target_dir = os.path.join(script_dir, os.path.dirname(config['target_file']))
print("获取目录路径: " + target_dir)

# 创建目标目录（如果不存在）
os.makedirs(target_dir, exist_ok=True)

target_path = os.path.join(script_dir, config['target_file'])
print("写入目标路径：" + target_path)

# 将翻译结果写入目标文件
with open(target_path, 'w', encoding='utf-8') as file:
    file.write(translated_content)

print('翻译完成！')
