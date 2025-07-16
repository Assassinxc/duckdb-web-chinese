import os
import requests
import json
import time

# --- 配置常量 ---

# Ollama API 的地址和端口 (与 ServBay 配置一致)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# 您在 ServBay 中下载并希望用于翻译的模型名称 (确保与 Ollama 中存在的模型名称完全一致)
# 例如: "llama3:8b", "mistral:7b", "deepseek-llm:7b-chat" 等
MODEL_NAME = "qwen3:8b"  # <--- 修改为您选择的模型名称!

# 源 Markdown 文件所在的目录
SOURCE_DIR = "stable"

# 存放翻译后文件的目录 (脚本会自动创建)
TARGET_DIR = "translated_qwen3_8b_stable"

# 您希望将文档翻译成的目标语言
TARGET_LANGUAGE = "Simplified Chinese" # 例如: "French", "German", "Japanese", "Spanish", "中文 (简体)"

# 可选：在请求之间添加延迟（秒），以避免过载或让系统有时间响应
REQUEST_DELAY = 1 # 1秒延迟，根据需要调整

# --- Ollama API 调用函数 ---

def translate_text_ollama(text_to_translate, model_name, target_language):
    """
    使用 Ollama API 翻译给定的文本。
    Args:
        text_to_translate (str): 需要翻译的原始文本。
        model_name (str): 要使用的 Ollama 模型名称。
        target_language (str): 目标翻译语言。
    Returns:
        str: 翻译后的文本，如果出错则返回 None。
    """
    # 构建清晰的翻译指令 prompt
    prompt = f"""Translate the following Markdown text into {target_language}.
Preserve the original Markdown formatting (like headings, lists, bold text, code blocks, etc.).
Only output the translated text, without any introductory phrases like "Here is the translation:".
Original Text:
---
{text_to_translate}
---
Translated Text ({target_language}):"""

    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model_name,
        "prompt": prompt,
        "think": False,
        "stream": False,
        "options":{
          "num_ctx": 40960,
            "num_predict": -1
        },

        # 设置为 False 以获取完整响应，而不是流式输出
        # 可选参数，根据需要调整，例如 temperature 控制创造性 (较低值更保守)
        # "options": {
        #     "temperature": 0.3
        # }
    }

    try:
        print(f"  Sending request to Ollama (model: {model_name})...")
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data, timeout=600) # 增加超时时间到300秒
        response.raise_for_status() # 检查 HTTP 错误 (例如 404, 500)

        response_data = response.json()

        # 从响应中提取翻译后的文本
        # Ollama 的 /api/generate 响应结构通常在 'response' 字段中包含完整输出
        if 'response' in response_data:
            translated_text = response_data['response'].strip()
            print(f"  Translation received (length: {len(translated_text)} chars).")
            return translated_text
        else:
            print(f"  Error: 'response' key not found in Ollama output: {response_data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"  Error calling Ollama API: {e}")
        return None
    except json.JSONDecodeError:
        print(f"  Error decoding JSON response from Ollama: {response.text}")
        return None
    except Exception as e:
        print(f"  An unexpected error occurred during translation: {e}")
        return None

# --- 主处理逻辑 ---

def process_directory(source_base, target_base):
    """
    递归遍历源目录，翻译 .md 文件并保存到目标目录。
    """
    print(f"\nProcessing directory: {source_base}")
    for item in os.listdir(source_base):
        source_path = os.path.join(source_base, item)
        target_path = os.path.join(target_base, item)

        if os.path.isdir(source_path):
            # 如果是子目录，递归处理
            print(f"- Found subdirectory: {item}")
            process_directory(source_path, target_path)
        elif os.path.isfile(source_path) and item.lower().endswith(".md"):
            # 如果是 Markdown 文件，进行翻译
            print(f"- Found Markdown file: {item}")

            # 确保目标文件的父目录存在
            target_file_dir = os.path.dirname(target_path)
            if not os.path.exists(target_file_dir):
                print(f"  Creating target directory: {target_file_dir}")
                os.makedirs(target_file_dir)

            # 检查目标文件是否已存在，如果存在则跳过（可选）
            # if os.path.exists(target_path):
            #     print(f"  Skipping, target file already exists: {target_path}")
            #     continue

            try:
                # 读取源文件内容
                print(f"  Reading source file: {source_path}")
                with open(source_path, 'r', encoding='utf-8') as f_in:
                    original_content = f_in.read()

                if not original_content.strip():
                    print("  Skipping empty file.")
                    continue

                # 调用 Ollama 进行翻译
                translated_content = translate_text_ollama(original_content, MODEL_NAME, TARGET_LANGUAGE)

                if translated_content:
                    # 写入翻译后的内容到目标文件
                    print(f"  Writing translated file: {target_path}")
                    with open(target_path, 'w', encoding='utf-8') as f_out:
                        f_out.write(translated_content)
                    print("  Translation complete for this file.")
                else:
                    print(f"  Failed to translate file: {source_path}. Skipping.")

                # 在两次API请求之间添加延迟
                if REQUEST_DELAY > 0:
                    print(f"  Waiting for {REQUEST_DELAY} second(s)...")
                    time.sleep(REQUEST_DELAY)


            except Exception as e:
                print(f"  Error processing file {source_path}: {e}")
        else:
            print(f"- Skipping non-Markdown file or other item: {item}")

# --- 脚本入口 ---

if __name__ == "__main__":
    print("Starting Markdown Bulk Translation Process...")
    print(f"Source Directory: {SOURCE_DIR}")
    print(f"Target Directory: {TARGET_DIR}")
    print(f"Target Language: {TARGET_LANGUAGE}")
    print(f"Using Ollama Model: {MODEL_NAME} at {OLLAMA_API_URL}")
    print("-" * 30)

    # 检查源目录是否存在
    if not os.path.isdir(SOURCE_DIR):
        print(f"Error: Source directory '{SOURCE_DIR}' not found.")
        print("Please create the 'docs' directory and place your Markdown files inside.")
        exit(1)

    # 检查/创建目标目录
    if not os.path.exists(TARGET_DIR):
        print(f"Creating target directory: {TARGET_DIR}")
        os.makedirs(TARGET_DIR)

    # 开始处理
    try:
        process_directory(SOURCE_DIR, TARGET_DIR)
        print("\n" + "=" * 30)
        print("Batch translation process finished!")
        print(f"Translated files are saved in the '{TARGET_DIR}' directory.")
    except Exception as e:
        print(f"\nAn error occurred during the process: {e}")