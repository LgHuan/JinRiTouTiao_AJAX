# JinRiTouTiao_AJAX
抓取今日头条XHR请求的热榜新闻图片（ajsax,urllib,mongo,json,urlencode）
1、技术难点
（1）xhr请求需要会话保持，否则xhr网页中无需要的内容；（2）不同新闻的xpath节点不一样，采用通用的【//img// href|src】，然后再对图片清洗。
2、技术方案
分析源代码中的xhr网址，请求url并保持会话，使用json.loads转换为html,获取新闻热榜的url列表，请求url并下载图片，清洗图片因为新闻的图片一般是大于logo等图片，所以采用图片大小清洗
