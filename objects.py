from bs4 import BeautifulSoup
import re


# 1 = single -> txt
# 2 = mutiple -> txt
# 3 = single -> att
# 4 = mutiple -> att
# 5 = single -> atts
# 6 = mutiple + atts

combs = [
    ['updated', 1], # single + txt
    ['published', 1], # single + txt
    ['title', 1], # single + txt
    ['summary', 1], # single + txt
    ['name', 2], # mutiple + txt
    ['arxiv:affiliation', 2], # mutiple + txt
    # ['arxiv:doi', 1], # single + txt
    ['link', 6, ['title', 'href']], # mutiple + atts
    ['arxiv:comment', 1], # single + txt
    # ['arxiv:journal_ref', 1], # single + txt
    ['arxiv:primary_category', 3, ['term']], # single + att
    ['category', 4, ['term']], # single + att
]
date_tags = ['updated','published']


class Entry:
    def __init__(self, souped:BeautifulSoup) -> None:
        self.souped = souped
        self.info = dict()

    def _clean_tag_name(self):
        return {key.replace('arxiv:', ''): value for key, value in self.info.items()}
    
    def _find(self, tag_name:str, type:int=0, atts:list=[]):
        if type == 0: return None
        # print(tag_name)
        f = self.souped.find(tag_name, {att:True for att in atts})
        if f==None: return
        if type==3:
            f = f[atts[0]]
            return f.strip()
        elif type==5:
            f = {f[atts[1]]: f[atts[1]].strip()}
            return f
        
        return f.text.strip()
    
    def _find_all(self, tag_name:str, type:int=0, atts:list=[]):
        n = list()
        f = self.souped.find_all(tag_name, {attr:True for attr in atts})
        if f==[] or f==None: return
        for s in f:
            if type==2:
                n.append(s.text.strip())
            elif type==4:
                n.append(s[atts[0]].strip())
            elif type==6:
                n.append({s[atts[0]]: s[atts[1]].strip()})

        return n
    
    def _clean_date(self):
        for tag in date_tags:
            self.info[tag] = self.info[tag].split('T')[0].split('-')
        return
    
    def scrape(self):
        for comb in combs:
            n, t, a= comb if len(comb) == 3 else comb + [[]]
            if t%2 == 1:
                self.info[n] = self._find(n, t, a)
            elif t%2 == 0:
                self.info[n] = self._find_all(n, t, a)
                    


        self._clean_date()

    def get_info(self):
        return self._clean_tag_name()