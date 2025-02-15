#!/usr/bin/env python3
import sys
import json
import requests
import os
from PIL import ImageGrab
import io
import tempfile
import hashlib
import time

API_BASE = "https://sm.ms/api/v2"
API_TOKEN = os.getenv('SM_TOKEN')  # 从Alfred workflow配置获取API token
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'sm_ms_icons')

# 支持的图片文件后缀
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp','.webp')

def download_image(url, filename):
    """下载图片到临时目录"""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
    return file_path

def show_notification(message, title):
    """显示系统通知"""
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

def get_image_list():
    """获取已上传的图片列表"""
    headers = {'Authorization': API_TOKEN}
    response = requests.get(f"{API_BASE}/upload_history", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            items = []
            for image in data['data']:
                # 使用URL的MD5作为本地文件名
                filename = hashlib.md5(image['url'].encode()).hexdigest() + '.png'
                # 下载图片到本地临时目录
                icon_path = download_image(image['url'], filename)
                items.append({
                    'title': image['filename'],
                    'subtitle': image['url'],
                    'arg': image['url'],
                    'icon': {'path': icon_path},
                    'quicklookurl': image['url'],
                    'mods': {
                        'cmd': {
                            'valid': True,
                            'arg': image['hash'],
                            'subtitle': '按Enter执行删除操作'
                        }
                    }
                })
            return {'items': items}
    return {'items': [{'title': '获取图片列表失败', 'subtitle': '请检查API token是否正确'}]}

def delete_image(hash):
    """删除指定的图片"""
    headers = {'Authorization': API_TOKEN}
    response = requests.get(f"{API_BASE}/delete/{hash}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            show_notification("图片已从SM.MS删除", "删除成功")
            return
    show_notification("请检查网络连接和API token", "删除失败")

def upload_clipboard_image():
    """上传剪贴板中的图片"""
    try:
        # 从剪贴板获取内容
        from AppKit import NSPasteboard, NSFilenamesPboardType
        pasteboard = NSPasteboard.generalPasteboard()
        
        # 首先检查是否是文件路径
        if pasteboard.types().containsObject_(NSFilenamesPboardType):
            file_paths = pasteboard.propertyListForType_(NSFilenamesPboardType)
            if file_paths and len(file_paths) > 0:
                # 筛选图片文件
                image_files = [f for f in file_paths if f.lower().endswith(IMAGE_EXTENSIONS)]
                if image_files:
                    items = []
                    for file_path in image_files:
                        with open(file_path, 'rb') as f:
                            img_byte_arr = f.read()
                            result = upload_image_bytes(img_byte_arr, os.path.basename(file_path))
                            if 'items' in result:
                                items.append(result['items'][0])
                    return {'items': items}
                return {'items': [{'title': '没有图片文件', 'subtitle': '请确保复制的文件包含图片'}]}
        
        # 如果不是图片文件，尝试获取剪贴板中的图片内容
        image = ImageGrab.grabclipboard()
        if image is None:
            return {'items': [{'title': '剪贴板中没有图片', 'subtitle': '请复制图片或图片文件'}]}
        
        # 将图片转换为字节流
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        # 使用时间戳生成唯一的文件名
        timestamp = int(time.time())
        return upload_image_bytes(img_byte_arr, f'clipboard_{timestamp}.png')
    except Exception as e:
        return {'items': [{'title': '上传出错', 'subtitle': str(e)}]}

def upload_image_bytes(img_bytes, filename):
    """上传图片字节流"""
    try:
        # 上传图片
        headers = {'Authorization': API_TOKEN}
        files = {'smfile': (filename, img_bytes, 'image/png')}
        response = requests.post(f"{API_BASE}/upload", headers=headers, files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                url = data['data']['url']
                # 使用URL的MD5作为本地文件名
                icon_filename = hashlib.md5(url.encode()).hexdigest() + '.png'
                # 下载图片到本地临时目录作为图标
                icon_path = download_image(url, icon_filename)
                show_notification("图片已上传到SM.MS", "上传成功")
                # 复制URL到剪贴板
                os.system(f'echo "{url}" | pbcopy')
                # 返回结果
                return {'items': [{
                    'title': '上传成功',
                    'subtitle': url,
                    'arg': url,
                    'icon': {'path': icon_path}
                }]}
            # 如果上传失败但API返回了错误信息
            error_message = data.get('message', '请检查网络连接和API token')
            return {'items': [{'title': '上传失败', 'subtitle': error_message}]}
        return {'items': [{'title': '上传失败', 'subtitle': '请检查网络连接和API token'}]}
    except Exception as e:
        return {'items': [{'title': '上传出错', 'subtitle': str(e)}]}


def main():
    if len(sys.argv) < 2:
        return
    
    command = sys.argv[1]
    if command == 'list':
        print(json.dumps(get_image_list()))
    elif command == 'upload':
        print(json.dumps(upload_clipboard_image()))
    elif command == 'delete' and len(sys.argv) > 2:
        print(json.dumps(delete_image(sys.argv[2])))

if __name__ == '__main__':
    main()