import article_parser

article_parser.parse(
    url='',  # The URL of the article.
    html='',  # The HTML of the article.
    threshold=0.9,  # The ratio of text to the entire document, default 0.9.
    output='html',  # Result output format, support ``markdown`` and ``html``, default ``html``.
),

title, content = article_parser.parse(url="http://www.chinadaily.com.cn/a/202009/22/WS5f6962b2a31024ad0ba7afcb.html",
                                      output='markdown', timeout=5)

print(title, content)
