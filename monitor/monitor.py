"""
库存监控工具 - Inventory Monitor
支持监控任意网页的库存状态变化
"""

import json
import time
import os
import sys
import winsound
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from plyer import notification

# ===== 配置文件路径 =====
CONFIG_FILE = Path(__file__).parent / "config.json"
LOG_FILE = Path(__file__).parent / "monitor.log"

# ===== 默认配置 =====
DEFAULT_CONFIG = {
    "interval": 30,  # 检查间隔（秒）
    "items": [
        {
            "name": "示例商品",
            "url": "https://example.com/product/123",
            "in_stock_keywords": ["有货", "加入购物车", "立即购买", "In Stock"],
            "out_of_stock_keywords": ["缺货", "售罄", "暂时缺货", "Out of Stock", "无货"],
            "enabled": True
        }
    ]
}


def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"[!] 已创建默认配置文件: {CONFIG_FILE}")
        print("[!] 请编辑配置文件后重新运行")
        sys.exit(0)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def log(message):
    """写入日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    try:
        print(line)
    except UnicodeEncodeError:
        # Windows 控制台兼容：去掉 emoji
        safe_line = line.encode("gbk", errors="replace").decode("gbk")
        print(safe_line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def notify(title, message):
    """发送桌面通知 + 播放提示音"""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
    except Exception:
        pass
    # Windows 提示音
    try:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass


def check_stock(item):
    """检查单个商品的库存状态"""
    url = item["url"]
    name = item["name"]
    in_keywords = item.get("in_stock_keywords", [])
    out_keywords = item.get("out_of_stock_keywords", [])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = resp.apparent_encoding
        text = resp.text.lower()

        # 检查关键词
        found_in = [kw for kw in in_keywords if kw.lower() in text]
        found_out = [kw for kw in out_keywords if kw.lower() in text]

        if found_in and not found_out:
            return "in_stock", found_in
        elif found_out and not found_in:
            return "out_of_stock", found_out
        elif found_in and found_out:
            return "mixed", found_in + found_out
        else:
            return "unknown", []

    except requests.RequestException as e:
        return "error", str(e)


def main():
    """主函数"""
    config = load_config()
    interval = config.get("interval", 30)
    items = config.get("items", [])

    if not items:
        print("[!] 没有配置监控项目，请编辑 config.json")
        sys.exit(0)

    enabled_items = [item for item in items if item.get("enabled", True)]
    if not enabled_items:
        print("[!] 没有启用的监控项目")
        sys.exit(0)

    log(f"=== 库存监控启动 ===")
    log(f"监控 {len(enabled_items)} 个项目，间隔 {interval} 秒")
    log(f"按 Ctrl+C 停止\n")

    # 记录上一次状态
    last_status = {}

    try:
        while True:
            for item in enabled_items:
                name = item["name"]
                url = item["url"]

                status, detail = check_stock(item)
                prev_status = last_status.get(name)

                if status == "in_stock":
                    log(f"✅ [{name}] 有货！关键词: {detail}")
                    if prev_status != "in_stock":
                        notify("库存到货！", f"{name} 现在有货了！")
                elif status == "out_of_stock":
                    log(f"❌ [{name}] 缺货")
                elif status == "mixed":
                    log(f"⚠️ [{name}] 状态混合: {detail}")
                elif status == "error":
                    log(f"🔴 [{name}] 请求失败: {detail}")
                else:
                    log(f"❓ [{name}] 未匹配到关键词")

                last_status[name] = status

            log(f"--- 等待 {interval} 秒 ---\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        log("=== 监控已停止 ===")


if __name__ == "__main__":
    main()
