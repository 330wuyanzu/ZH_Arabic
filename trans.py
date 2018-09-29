#encode: utf-8
#coding: utf-8

'''
Only tested on Python 3.7
Only suport UTF-8
'''

class Trans(object):
    def __init__(self, ch):
        self.ch = ch
        self.num = {"零":'0', "一":'1', "二":'2', "两":'2', "三":'3', "四":'4', "五":'5', "六":'6', "七":'7', "八":'8', "九":'9'}
        self.unit = {"个":0,"十":1,"百":2,"千":3,"万":4,"亿":8}#个0
        self.placeholder = ''
        self.value = ''
    
    def _placeholder(self):
        what = self.ch
        count_y = what.count('亿')
        count_w = what.count('万')
        count_q = what.count('千')
        count_b = what.count('百')
        count_s = what.count('十')
        if count_y != 0: # 至少亿级
            self.placeholder = 'qbsw'+'qbsyqbsw'*count_y+'qbsg' #亿亿级 qbsw qbsyqbsw qbsyqbsw qbsg 亿级 qbsw qbsyqbsw qbsg
        elif count_w != 0: # 没有达到亿级，那只能是万级
            self.placeholder = 'qbswqbsg'# 万级 qbsw qbsg 万级
        elif count_q != 0: # 没有达到万级，那就只有千级
            self.placeholder = 'qbsg'
        elif count_b != 0: # 没有达到千级，那就只有百级
            self.placeholder ='bsg'
        elif count_s != 0: # 十级
            self.placeholder = 'sg'
        else:
            self.placeholder = 'g'
                
    def _qbswqbsyqbswqbsg(self, qbswqbsyqbswqbsg):
        # [一]亿[]
        # [一]亿[两千三百四十五万六千七百八十九]
        # [一]亿[零三百四十万五千六百七十八]
        group = qbswqbsyqbswqbsg.split('亿')
        arabic = []
        for qbswqbsg in group:
            if qbswqbsg == '':
                temp = '00000000'
            else:
                temp = self._qbswqbsg(qbswqbsg)
            arabic.append(temp)
        return ''.join(arabic)
    
    def _qbswqbsg(self, qbswqbsg):
        # x，xx，xxx，xxxx，x xxxx，xx xxxx，xxx xxxx，xxxx xxxx
        # [一]，[两千三百四十五]万[六千七百八十九]
        # [零三百四十]万[五千六百七十八]
        if '万' in qbswqbsg:
            [qbsw, qbsg] = qbswqbsg.split('万')
            qbsw = self._qbsg(qbsw)
            if qbsg == '':
                qbsg = '0000'
            else:
                qbsg = self._qbsg(qbsg)
        else:
            qbsw = '0000'
            qbsg = self._qbsg(qbswqbsg)
        return qbsw+qbsg

    def _qbsg(self, qbsg):
        if '千' in qbsg:
            [q, bsg] = qbsg.split('千')
            q = self._g(q)
            if bsg == '':
                bsg = '000'
            else:
                bsg = self._bsg(bsg)
        else:
            q = '0'
            bsg = self._bsg(qbsg)
        return q+bsg

    def _bsg(self, bsg):
        if '百' in bsg:
            [b, sg] = bsg.split('百')
            b = self._g(b)
            if sg == '':
                sg = '00'
            else:
                sg = self._sg(sg)
        else:
            b = '0'
            sg = self._sg(bsg)
        return b+sg

    def _sg(self, sg):
        if '十' in sg:
            [s,g] = sg.split('十')
            if s =='':
                s = '1'
            else:
                s = self._g(s)
            if g=='':
                g = '0'
            else:
                g = self.num[g]
        else:
            s = '0'
            g = self._g(sg)
        return s+g

    def _g(self, g):
        if g.startswith('零'):
            g = g[-1]
        return self.num[g]

    def Arabic(self):
        self._placeholder()
        if self.placeholder == 'g':
            self.value = self._g(self.ch)
        elif self.placeholder == 'sg':
            self.value = self._sg(self.ch)
        elif self.placeholder == 'bsg':
            self.value = self._bsg(self.ch)
        elif self.placeholder == 'qbsg':
            self.value = self._qbsg(self.ch)
        elif self.placeholder == 'qbswqbsg':
            self.value = self._qbswqbsg(self.ch)
        else:
            self.value = self._qbswqbsyqbswqbsg(self.ch)
        return self.value.lstrip('0')


def TEST(test):
    trans = Trans(test)
    print(f'{test} - {trans.Arabic()}')


if __name__ == '__main__':
    test = "十亿两千三百四十五万六千七百八十九亿零一百二十三万四千五百六十七"#1 2345 6789 0123 4567
    TEST("一")
    TEST("十")
    TEST("十一")
    TEST("二十")
    TEST("二十一")
    TEST("一百")
    TEST("一百零二")
    TEST("一百一十")
    TEST("一百一十一")
    TEST("一千")
    TEST("一千两百三十四")
    TEST("一千两百三十")
    TEST("一千两百零三")
    TEST("一千零二十")
    TEST("一千零二十三")
    TEST("一千零二")
    TEST("一万两千三百四十五")
    TEST("一万零三百四十五")
    TEST("一万零四十五")
    TEST("一万零四十")
    TEST("一万零四")
    TEST("十亿")
    TEST("一亿零一")
    TEST(test)