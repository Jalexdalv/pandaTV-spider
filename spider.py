import re
from urllib  import request
import win_unicode_console

class Sprider():
    url = 'https://www.panda.tv/all'
    root_pattern = '<div class="video-info">([\w\W]*?)</div>'
    name_pattern = '</i>([\w\W]*?)</span>'
    number_pattern = '<span class="video-number">([\w\W]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Sprider.url)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls
    
    def __analysls(self,htmls):
        root_html = re.findall(Sprider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Sprider.name_pattern, html)
            number = re.findall(Sprider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l, anchors)

    def __sort(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchor):
        r = re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self,anchors):
        i = 0
        for anchor in anchors:
            print(anchor['name']+'-----'+anchor['number'])
            i+=1
        print(i)

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysls(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

win_unicode_console.enable()
spider = Sprider()
spider.go()
