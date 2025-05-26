import requests
import time
import hashlib
import random
import string
import json


def generate_wbi_sign(params):
    w_rid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    wts = str(int(time.time()))

    sign_str = []
    for k in sorted(params.keys()):
        sign_str.append(f"{k}={params[k]}")
    sign_str.append(f"w_rid={w_rid}")
    sign_str.append(f"wts={wts}")
    sign_str = '&'.join(sign_str)

    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return {
        "w_rid": w_rid,
        "wts": wts,
        "sign": sign
    }


def get_aid_from_bvid(bvid, sessdata):
    url = "https://api.bilibili.com/x/web-interface/view"
    headers = {
        'Cookie': f'SESSDATA={sessdata}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': f'https://www.bilibili.com/video/{bvid}'
    }
    params = {"bvid": bvid}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            return data["data"]["aid"]
        else:
            raise ValueError(f"获取 aid 失败: {data.get('message', '未知错误')}")
    else:
        raise ConnectionError(f"请求失败，状态码: {response.status_code}")


def get_video_info(bvid, sessdata):
    url = "https://api.bilibili.com/x/player/pagelist"
    headers = {
        'Cookie': f'SESSDATA={sessdata}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': f'https://www.bilibili.com/video/{bvid}'
    }
    params = {"bvid": bvid, "jsonp": "jsonp"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            aid = data.get("aid")
            if not aid:
                aid = get_aid_from_bvid(bvid, sessdata)

            video_data = data["data"][0]
            video_data["aid"] = aid
            return video_data
        else:
            raise ValueError(f"API错误: {data.get('message', '未知错误')}")
    else:
        raise ConnectionError(f"请求失败，状态码: {response.status_code}")


def get_subtitle_info(aid, cid, sessdata):
    url = "https://api.bilibili.com/x/player/wbi/v2"
    headers = {
        'Cookie': f'SESSDATA={sessdata}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com/'
    }

    params = {
        "aid": aid,
        "cid": cid
    }

    wbi_params = generate_wbi_sign(params)
    params.update({
        "w_rid": wbi_params["w_rid"],
        "wts": wbi_params["wts"],
        "sign": wbi_params["sign"]
    })

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            subtitles = data["data"]["subtitle"]["subtitles"]
            return [f"https:{sub['subtitle_url']}" for sub in subtitles]
        else:
            raise ValueError(f"API错误: {data.get('message', '未知错误')}")
    else:
        raise ConnectionError(f"请求失败，状态码: {response.status_code}")


def download_subtitle(subtitle_url):
    """
    下载字幕文件并返回其内容（JSON 格式）。
    """
    response = requests.get(subtitle_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ConnectionError(f"下载字幕失败，状态码: {response.status_code}")


def format_time(seconds):
    """
    将秒数转换为标准的时间格式：HH:MM:SS,mmm
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def convert_to_str(subtitle_data):
    """将字幕数据转换为时间戳+字幕的字符串"""
    output = []
    for item in subtitle_data["body"]:
        timestamp = format_time(item["from"])
        content = item["content"]
        output.append(f"{timestamp} {content}")
    return '\n'.join(output)


def get_subtitles(bvid, sessdata):
    """主调用函数：返回结构化数据"""
    try:
        video_info = get_video_info(bvid, sessdata)
        cid = video_info["cid"]
        aid = video_info["aid"]

        subtitle_urls = get_subtitle_info(aid, cid, sessdata)
        if not subtitle_urls:
            return {"status": "success", "subtitles": []}

        all_subtitles = []
        for subtitle_url in subtitle_urls:
            subtitle_data = download_subtitle(subtitle_url)
            str_content = convert_to_str(subtitle_data)
            all_subtitles.append({
                "url": subtitle_url,
                "content": str_content,
                "raw_data": subtitle_data
            })

        return {
            "status": "success",
            "metadata": {"bvid": bvid, "aid": aid, "cid": cid},
            "subtitles": all_subtitles
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"获取字幕失败: {str(e)}"
        }


if __name__ == "__main__":
    # 保留原有命令行测试功能
    bvid = input("请输入视频的BV号: ")
    sessdata = input("请输入你的SESSDATA: ")

    result = get_subtitles(bvid, sessdata)
    print(json.dumps(result, indent=2, ensure_ascii=False))