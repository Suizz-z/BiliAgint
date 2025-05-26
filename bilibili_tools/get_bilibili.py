import asyncio
import json
from typing import List
import datetime

from bilibili_api import search,comment,Credential
from bilibili_api.comment import CommentResourceType,OrderType


async def fetch_comments(oid, page_start, page_end):
    type_ = CommentResourceType.VIDEO
    order =  OrderType.TIME

    credential = Credential(
        sessdata="c8aeb5e6%2C1758110475%2C31b7a%2A32CjA1egWb6AJp52u3GZXVLQr1Zi_2_So2GHiE24JB8Qh6ipM5bkGf1l45VghFNeeVb-YSVkdvMG9JaU5JRFE3cWlPSXU4czJLa2x1T1F1TUtVa29ieEtWYkVjZ1pDU0JfTVdhbWdSLThMamxCQnRMcFRtWXlveEFSZjFjOU1aMGRtUkdCU1YtX2x3IIEC",
        bili_jct="21b9a730e75e84bda30a317b383db508",
        buvid3="1A4A1E30-AFA3-AB67-7F0C-CB3FB293CFED34629infoc",
        dedeuserid="32690965",
        ac_time_value="71a8f07a2f89d438ca260714b181e732"
    )

    comments_list = []

    for page_index in range(page_start,page_end + 1):
        try:
            response = await comment.get_comments(oid, type_, page_index, order, credential=credential)
            if 'replies' not in response or not response['replies']:
                continue

            comments_data = response['replies']
            for context in comments_data:
                message = context['content']['message']
                comments_list.append(message)
        except Exception as e:
            print(f"An error occurred on page {page_index}: {str(e)}")
            continue

    return comments_list


async def process_search_results(results):
    data_to_write = []

    for result in results:
        if result['data']:
            for item in result['data']:
                tages = item.get('tag','').split(',')

                oid = item.get('aid',0),

                # comments = await fetch_comments(oid,1,30)
                comments = ''


                process_data = [
                    item.get('type',''),
                    item.get('author', ''),
                    item.get('typename', ''),
                    item.get('arcurl', ''),
                    item.get('title', '').replace('<em class="keyword">','').replace('</em>',''),
                    item.get('description', ''),
                    item.get('play', 0),
                    item.get('video_review', 0),
                    item.get('favorites', 0),
                    ','.join(tages),
                    item.get('comment',0),
                    comments,
                    datetime.datetime.fromtimestamp(item.get('pubdate',0)).strftime('%Y-%m-%d %H:%M:%S'),
                ]

                headers = ["类型","作者","分类","视频链接","标题","描述","播放量","弹幕数","收藏数","标签","发布曰期","评论"]

                result_text = '\n'.join(f"{header}:{data}" for header,data in zip(headers,process_data))

                data_to_write.append(result_text)

    return json.dumps(data_to_write,ensure_ascii=False)


async def bilibili_detail_pipline(keywords: List,page:int):

    all_results = []

    for keyword in keywords:

        keyword_results = []

        for page in range(1,2):
            result = await search.search(keyword=keyword, page=page)
            # print(f"result:{json.dumps(result,indent=4,ensure_ascii=False)}")
            keyword_results.extend(result.get('result',[]))

            real_data = await process_search_results(keyword_results)
            all_results.append(
                {
                    "keyword": keyword,
                    "real_data": real_data
                }
            )
        print(f"result:{json.dumps(all_results,indent=4,ensure_ascii=False)}")
        return all_results

asyncio.run(bilibili_detail_pipline(keywords=["大模型"],page=1))


