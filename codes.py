# 获取电影天堂的电影信息
# 全局变量一般用大写

from lxml import etree
# 进行信息的提取
import requests

DOMAIN = 'https://www.dytt8.net'
HEAD = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Referer': 'https://www.dytt8.net/html/gndy/dyzz/list_23_3.html',
    'Host': 'www.dytt8.net'
}
# 全局变量一般大写命名

# 使用map函数
# 注意解码的写法
movie_in_links = []
# 存放每部电影的 url
all_movie_info = []
# 存放每部电影的信息


def url_list():
    # 只爬取前10页就可以了
    urlist = []
    for i in range(1, 11):
        url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(i)
        urlist.append(url)
    # 创建每一个列表页的链接
    return urlist


def get_moviepage_links(url):
    global movie_in_links
    # 需要进行全局变量的声明
    resp = requests.get(url, headers=HEAD)
    resp.encoding = 'utf-8'
    resplx = etree.HTML(resp.text)
    links = resplx.xpath('//table[@class="tbspan"]//a/@href')
    # 查找每部电影网页的 url
    linklist = list(map(lambda x: DOMAIN + x, links))
    # 用map函数对每个 url 进行拼接
    # 需要进行列表话
    movie_in_links += linklist
    # 列表的相加就是合并而已
    return movie_in_links


def get_each_movie(movie_url):
    # 获取每一部电影的信息
    res = requests.get(movie_url)
    res.encoding = 'utf-8'
    reslx = etree.HTML(res.content)
    movie_info = reslx.xpath('//div[@id="Zoom"]//text()')
    # 把信息部分进行提取
    movie_name_index = None
    movie_actor_index = None
    movie_score_index = None
    # 对索引先声明，防止后续报错
    try:
        # try except 结构，过滤报错
        for item in movie_info:
            if '◎译\u3000\u3000名\u3000'in item:
                # \u3000 的意思是 全角的空白符
                movie_name_index = movie_info.index(item)
            if '◎主\u3000\u3000演\u3000' in item:
                movie_actor_index = movie_info.index(item)
            if '豆瓣评分\u3000' in item:
                movie_score_index = movie_info.index(item)

        movie_dloadurl = reslx.xpath('//div[@id="Zoom"]//a/@href')
        # 提取电影的下载链接
        dic = {
            'movie_name': movie_info[movie_name_index].split('\u3000')[-1].split('/')[0],
            'movie_actor': movie_info[movie_actor_index].split('\u3000')[-1],
            # 此处有问题
            # 通过 try 进行过滤
            'movie_score': movie_info[movie_score_index].split('\u3000')[-1],
            'movie_dloadurl': movie_dloadurl
        }
        all_movie_info.append(dic)
        print('已获取电影信息：--> %s' % movie_info[movie_name_index].split('\u3000')[-1].split('/')[0])
    except TypeError:
        print('---------电影获取错误---------')
    return all_movie_info


# for i in get_each_movie('https://www.dytt8.net/html/gndy/dyzz/20181107/57755.html'):
#     if '◎译\u3000\u3000名\u3000' in i:
#         print(i.split('\u3000')[-1].split('/')[0])

# print(get_each_movie('https://www.dytt8.net/html/gndy/dyzz/20181107/57755.html'))
def main():
    urllist = url_list()
    for each in urllist[:2]:
        get_moviepage_links(each)
    print('\n共解析了 %d 页\n' % len(urllist[:2]))
    for each_movie in movie_in_links:
        # 只取其前4页以作示范
        get_each_movie(each_movie)
    # for n in all_movie_info:
    #     print(n)
    return all_movie_info


if __name__ == '__main__':
    get_movies = main()
    with open(r'get_movies.csv', 'w') as getmovie:
            for i in all_movie_info:
                try:
                    getmovie.write('{0},{1},{2},{3}\n'.format('电影', i['movie_name'], '下载地址', i['movie_dloadurl'][0]))
                    print('***已写入一部电影信息***')
                    # 此处，因为获取的下载地址是一个含有两个元素的列表，所以取其第一个磁力链接。
                except IndexError:
                    print('文件写入出现错误')
