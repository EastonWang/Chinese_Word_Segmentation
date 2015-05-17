#!/user/bin/python
# -*- coding:utf-8 -*-
# -*- coding: encoding -*-
#coding:gbk
#----------------------------------------------------------
import sqlite3
def add_word(word,freq):   #向词典数据库添加词和词频
    first=word[0]
    r_tempdic(first)
    p=0
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)==False:
             tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
             conn.commit()
        else:
            return False
    else:
        tempdicname.execute(''''create table '''+first+''' (
        word text ,
        freq text
        )''')
        tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
        conn.commit()
    first=word[-1]
    l_tempdic(first)
    p=-1
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)==False:
             tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
             conn.commit()
        else:
            return False
    else:
        tempdicname.execute('''create table '''+first+''' (
        word text ,
        freq text
        )''')
        tempdicname.execute('insert into '+first+' values (?,?)',(word,freq))
        conn.commit()
def del_word(word):  #从词典数据库删词
    first=word[0]
    r_tempdic(first)
    p=0
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)!=False:
             tempdicname.execute('delete from '+first+' where word==?',(word,))
             conn.commit()
        else:
            return False
    else:
        return False
    first=word[-1]
    l_tempdic(first)
    p=-1
    if able_word(first,tempdicname)==True:
        if find_word(word,tempdicname,p)!=False:
             tempdicname.execute('delete from '+first+' where word==?',(word,))
             conn.commit()
        else:
            return False
    else:
        return False
#----------------------------------------------------------
conn1=sqlite3.connect('db\\a-h.db')   #与六个数据库建立连接并定义指针
conn2=sqlite3.connect('db\\i-p.db')
conn3=sqlite3.connect('db\\q-z.db')
conn4=sqlite3.connect('db\\l_a-h.db')
conn5=sqlite3.connect('db\\l_i-p.db')
conn6=sqlite3.connect('db\\l_q-z.db')
curs1=conn1.cursor()
curs2=conn2.cursor()
curs3=conn3.cursor()
curs4=conn4.cursor()
curs5=conn5.cursor()
curs6=conn6.cursor()
def able_word(fir,curs): #判断词典中是否有以某个字开头的词语
    try:
        curs.execute('select * from '+fir)
        return True
    except:
        return False
def find_word(word,curs,p):  #判断是否有某个词语并返回词频
    first=word[p]
    curs.execute('select * from '+first+' where word==?',(word,))
    line=curs.fetchone()
    if line==None:
        return False
    else:
        freq=line[1]
        return freq
#--------------------------------------------------------
import string
notchs=string.ascii_letters+string.digits+' +=' #标记 数字 字母 + = 以分为一个词
tempdicname=sqlite3.Cursor     #当前数据库游标
special=[]     #辅助分词词典
r_freq=0       #正向匹配词频和
l_freq=0       #逆向匹配词频和
#词库判断模块-----------数据库游标切换
a=[ i.encode('gbk') for i in ['祸', '瀑'] ]
def r_tempdic(s):
    global tempdicname
    global conn
    te=s.encode('gbk')
    if a[1]<te:     #声母在q-z
        tempdicname=curs3
        conn=conn3
    elif a[0]<te:   #声母在i-p
        tempdicname=curs2
        conn=conn2
    else:           #声母在a-h
        tempdicname=curs1
        conn=conn1
def l_tempdic(s):
    global tempdicname
    global conn
    te=s.encode('gbk')
    if a[1]<te:
        tempdicname=curs6  #声母在q-z
        conn=conn6
    elif a[0]<te:
        tempdicname=curs5  #声母在i-p
        conn=conn5
    else:                  #声母在a-h
        tempdicname=curs4
        conn=conn3   #-
def right_seg(text):     #正向分词
    global r_freq,tempdicname
    if len(text)>=1:
        if text[0] in notchs:    #如果分词内容第一个字不是中文（字母数字+=）
            try:                 #继续读取下一个字直到是中文为止，并分出前面部分
                if text[1] in notchs:
                    return text[0] + right_seg(text[1:])
                else:
                    return text[0]+'/' +right_seg(text[1:])
            except:
                return text[0] +'/' +right_seg(text[1:])
        else:
            length=5       #设定词语最大长度为5进行最大匹配
            if len(text)<length: #预处理最大长度以减小时间复杂度
                length=len(text)
            r_tempdic(text[0])        #首字游标预处理
            while length>1:
                if not able_word(text[0],tempdicname):      #判断首字是否可构成词
                    return text[0] + '/' + right_seg(text[1:])
                else:
                    tempfreq=find_word(text[:length],tempdicname,0)   #匹配词语
                    if tempfreq!=False:
                        r_freq=r_freq+int(tempfreq)    #计算正向词频
                        return text[:length] + '/' + right_seg(text[length:])
                length=length-1
            return text[0] + '/' + right_seg(text[1:])
    else:
        return text
def left_seg(text):    #逆向分词
    global tempdicname,l_freq
    if len(text)>=1:
        if text[-1] in notchs:     #如果分词内容最后一个字不是中文（字母数字+=）
            try:                   #继续读取上一个字直到是中文为止，并分出后面部分
                if text[-2] in notchs:
                    return left_seg(text[:-1]) + text[-1]
                else:
                    return left_seg(text[:-1]) +'/'+text[-1]
            except:
                return  left_seg(text[:-1])+'/'+text[-1]
        else:
            length=5           #设定词语最大长度为5进行最大匹配
            if len(text)<length:   #预处理最大长度以减小时间复杂度
                length=len(text)
            l_tempdic(text[-1])    #尾字游标预处理
            while length>1:
                if not able_word(text[-1],tempdicname):    #判断尾字是否可构成词
                    return  left_seg(text[:-1]) + '/' + text[-1]
                else:
                    tempfreq=find_word(text[-length:],tempdicname,-1)  #匹配词语
                    if tempfreq!=False:
                        l_freq=l_freq+int(tempfreq)      #计算逆向词频
                        return left_seg(text[:-length]) + '/' + text[-length:]
                length=length-1
            return left_seg(text[:-1]) + '/' + text[-1]
    else:
        return text
def divide(text): #按标点分割句子
    punctuation='，。、：；《》（）？！.~…\"“”()‘’——'
    sentences=[]
    for i in punctuation:
        text=text.replace(i,' ')
    sentences=text.split()
    return sentences
def accurate_seg(sentence):  #精准分词
    r=right_seg(sentence)
    if r[-1]=='/':     #首末/符处理
        r=r[:-1]
    l=left_seg(sentence)
    if l[0]=='/':
        l=l[1:]
    if r==l:
        return r
    else:
        return reprocess(r,l)
def fast_seg(sentence):      #快速分词
    r=left_seg(sentence)
    if r[0]=='/':
        r=r[1:]
    return r
def reprocess(rseg,lseg):   #精准分词词频处理
    r=rseg.count('/')       #对分词个数进行比较取较小者
    l=lseg.count('/')
    if r==l:
        if r_freq>l_freq:
            return rseg
        else:
            return lseg
    elif r<l:
        return rseg
    elif r>l:
        return lseg
def special_divide(text,words):  #辅助分词划分处理
    global special
    special=words.split('|')
    for i in special:
        text=('，'+i+'，').join(text.split(i))   #将辅助词语分隔为句子
    return text

#------界面部分------------
from tkinter import*
from tkinter.filedialog import*
from tkinter.messagebox import*
from tkinter.font import*
class MyTL1:        #词频操作窗口
    def __init__(self,root):
        self.bm=PhotoImage(file='ico.gif')
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('字典操作')
        self.v=IntVar()
        self.v.set(1)
        self.menubar=Menu(self.tl)
        self.fm1=Menu(self.menubar,tearoff=0)
        self.fm1.add_radiobutton(label='添加词语',variable=self.v,value=1,command=self.TJ)
        self.fm1.add_radiobutton(label='删除词语',variable=self.v,value=2,command=self.SC)
        self.menubar.add_cascade(label='操作选项',menu=self.fm1)
        self.menubar.add_command(label='帮助',command=self.open)
        self.tl['menu']=self.menubar
        self.frame=Frame(self.tl)
        self.frame1=Frame(self.frame)
        self.text3=StringVar()
        self.text3.set('添加词：')
        self.label1=Label(self.frame1,textvariable=self.text3)
        self.label1.pack(anchor='nw',ipadx=40)
        self.text1=StringVar()
        self.entry1=Entry(self.frame1,textvariable=self.text1,width=25)
        self.entry1.pack()
        self.frame1.pack(side=LEFT,ipadx=40)
        self.frame2=Frame(self.frame)
        self.label2=Label(self.frame2,text='添加词词频：')
        self.label2.pack(anchor='nw',ipadx=40)
        self.text2=IntVar()
        self.entry2=Entry(self.frame2,textvariable=self.text2,wid=10)
        self.entry2.pack()
        self.frame2.pack(side=LEFT,ipadx=40)
        self.frame.pack(fill=X)
        self.label4=Label(self.tl,image=self.bm)
        self.label4.pack()
        self.frame3=Frame(self.tl)
        self.button1=Button(self.frame3,text='添加',command=self.add,width=12)
        self.button2=Button(self.frame3,text='删除',command=self.dele,width=12)
        self.frame3.pack(side=BOTTOM)
        self.button1.pack()
    def SC(self):       #切换删除模式
        self.text3.set('删除词：')
        self.text1.set('')
        self.text2.set(0)
        self.frame3.forget()
        self.frame2.forget()
        self.frame1.pack(ipadx=40)
        self.frame3.pack(side=BOTTOM)
        self.button1.forget()
        self.button2.pack()
    def TJ(self):       #切换添加模式
        self.text3.set('添加词：')
        self.text1.set('')
        self.frame3.forget()
        self.frame2.pack(ipadx=40)
        self.frame3.pack(side=BOTTOM)
        self.button2.forget()
        self.button1.pack()
    def open(self):     #打开新窗口
        self.tl2=MyTL3(self.tl)
    def add(self):
        if self.text1.get() == '':
            showerror(title='错误',message='添加的词不能为空！')
        else:
            if self.text2.get() == 0:
                showerror(title='错误',message='添加词的词频不能为0！')
            else:
                if add_word(self.text1.get(),str(self.text2.get())) == False:
                    showerror(title='错误',message='添加的词已存在！')
                else:
                    showinfo(title='消息',message='添加成功！')
    def dele(self):
        if self.text1.get() == '':
            showerror(title='错误',message='删除的词不能为空！')
        else:
            if del_word(self.text1.get()) == False:
                showerror(title='错误',message='删除的词不存在！')
            else:
                showinfo(title='消息',message='删除成功！')
class MyTL2:        #帮助窗口-1
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('说明')
        for i in ['文件：点击菜单中的‘文件’可以选择‘打开’来打开一个txt文档，将其导入‘分词原文’。',
        '         也可以选择‘保存’将‘分词结果’的内容以txt文档格式保存。',
        '         点击‘退出’可以退出本软件。',' ','模式：点击菜单中的‘模式’可以选择‘快速分词’与‘精准分词’。','      ‘快速分词’模式速度快，准确率较低。',
        '      ‘精准分词’模式速度较慢，准确率高，默认选择准确率更高的‘双向分词’模式，并且可以使用‘辅助分词功能’来使特定的词语不被分割。',' ',
        '工具：点击菜单中的‘工具’可以选择‘字典操作’来在分词的数据库添加、删除词语。',' ',
        '帮助：点击菜单中的‘帮助’可以获取‘说明’中的软件使用方法，和‘关于’中的软件信息。']:
            self.label=Label(self.tl,text=i)
            self.label.pack(anchor='nw')
        self.bm = PhotoImage(file='ico.gif')
        self.label1=Label(self.tl,image=self.bm)
        self.label1.pack()
class MyTL3:   #帮助窗口-2
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('帮助')
        for i in ['通过选择操作选项可以切换‘添加词语’与‘删除词语’模式。',
        '‘添加词语’：向字典中添加输入的词语与它的词频。添加词必须为字典中不存在的词。',
        '‘删除词语’：在字典中删除输入的词语与它的词频，删除词必须为字典中已存在的词。']:
            self.label=Label(self.tl,text=i)
            self.label.pack()
        self.bm = PhotoImage(file='ico.gif')
        self.label1=Label(self.tl,image=self.bm)
        self.label1.pack()
class MyTL4:
    def __init__(self,root):
        self.root=root
        self.tl=Toplevel(root)
        self.tl.title('关于')
        self.ft1=Font(family = '黑体',size = 35)
        self.bm = PhotoImage(file='ico.gif')
        self.blank1=Label(self.tl,text='                                     ')
        self.blank1.pack()
        self.frame1=Frame(self.tl)
        self.gif=Label(self.frame1,image=self.bm)
        self.gif.pack(side=LEFT)
        self.label1=Label(self.frame1,text='中文分词系统 ',font=self.ft1,fg='#4F4F4F')
        self.label1.pack()
        self.label2=Label(self.frame1,text='Chinese Word Segmentating System')
        self.label2.pack()
        self.frame1.pack()
        self.xhx=Label(self.tl,text='————————————————————————————',fg='#8E8E8E')
        self.xhx.pack()
        self.frame2=Frame(self.tl)
        for i in ['K.O.1 小组','Verson 3.0（内部版本 3.3.7）','Copyright © 2012-2013 K.O.1 小组保留所有权利。'
        ,'中文分词系统 Verson 3.0 分词算法及其用户界面受中国和其他','国家/地区的商标法和其他待颁布或已颁布的知识产权法保护。']:
            self.label=Label(self.frame2,text=i)
            self.label.pack(anchor='nw')
        self.xhx2=Label(self.frame2,text='————————————————————————————',fg='#8E8E8E')
        self.xhx2.pack()
        for i in ['重要更新历史：','————Verson 3.0：','    1.增加辅助词语分词功能，人工干预分词结果更精准'
        ,'    2.分词算法优化，速度更快更流畅','————Verson 2.1：','    1.改进分词算法和查询结构，分词速度优化'
        ,'    2.同步改进数据库结构','    3.分词算法的细微调整，优化了分词速度'
        ,'————Verson 2.0：','    1.语料词典保存在数据库中，启动速度大幅优化'
        ,'    2.分词算法查询系统优化','    3.增加了数据库词典操作功能','————Verson 1.1：',
        '    1.分离双向分词功能为快速分词和精准分词，用户可自行选择','    2.分词算法大幅优化，快速分词更快，精准分词更准']:
            self.label=Label(self.frame2,text=i)
            self.label.pack(anchor='nw')
        self.frame2.pack()


        self.blank2=Label(self.tl,text='                                     ')
        self.blank2.pack()
class MyMenu:   #主菜单
    def __init__(self,root,text1,text2,Addword):
        self.root=root
        self.text1=text1
        self.text2=text2
        self.Addword=Addword
        self.v=IntVar()
        self.v.set(2)
        self.menubar=Menu(root)
        self.fm1=Menu(self.menubar,tearoff=0)
        self.fm1.add_radiobutton(label='快速分词',variable=self.v,value=2,command=self.Bctrl)
        self.fm1.add_radiobutton(label='精准分词',variable=self.v,value=1,command=self.Actrl)
        self.fm2=Menu(self.menubar,tearoff=0)
        self.fm2.add_command(label='打开',command=self.open_file)
        self.fm2.add_command(label='另存为',command=self.save_file)
        self.fm2.add_command(label='退出',command=self.quit)
        self.menubar.add_cascade(label='文件',menu=self.fm2)
        self.menubar.add_cascade(label='模式',menu=self.fm1)
        self.fm3=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='工具',menu=self.fm3)
        self.fm3.add_command(label='字典操作',command=self.open_1)
        self.fm4=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='帮助',menu=self.fm4)
        self.fm4.add_command(label='说明',command=self.open_2)
        self.fm4.add_command(label='关于',command=self.open_3)
        self.root['menu']=self.menubar
    def Actrl(self):    #精准分词模式
        self.Addword.repack()
    def Bctrl(self):    #快速分词模式
        self.Addword.forget()
    def open_1(self):   #打开词频操作窗口
        self.tl=MyTL1(root)
    def open_2(self):   #打开帮助窗口
        self.tl=MyTL2(root)
    def open_3(self):   #打开关于窗口
        self.tl=MyTL4(root)
    def open_file(self):    #导入文件
        self.t=askopenfilename(filetypes=[("文本文档","*.txt")])
        if self.t != '':
           self.file=open(self.t,'r')
           self.content=self.file.read()
           self.text1.insert(self.content)
    def save_file(self):    #保存文件
        if self.text2.get()=='\n':
            showerror(title='错误',message='保存的分词结果不能为空！')
        else:
            self.t=asksaveasfilename(filetypes=[("文本文档","*.txt")],defaultextension='txt')
            if self.t != '':
                self.file=open(self.t,'w')
                self.file.write(self.text2.get())
                self.file.close()
    def quit(self):
        root.destroy()
class Mybottun:  #主界面按钮
    def __init__(self,root,text1,text2,menu,AW):
        self.root=root
        self.text1=text1
        self.text2=text2
        self.menu=menu
        self.frame=Frame(root)
        self.text=StringVar()
        self.text.set('')
        self.AW=AW
        self.bm=PhotoImage(file='ico.gif')
        self.label=Label(self.frame,textvariable=self.text,fg='red',image=self.bm,compound='left',width=200,height=75)
        self.label.pack(side=LEFT)
        self.bottun1=Button(self.frame,text='开始分词',command=self.start,width=12)
        self.bottun1.pack(side=LEFT,padx=15)
        self.bottun2=Button(self.frame,text='清空原文',command=self.clean1,width=12)
        self.bottun2.pack(side=LEFT,padx=15)
        self.bottun3=Button(self.frame,text='清空结果',command=self.clean2,width=12)
        self.bottun3.pack(side=LEFT,padx=15)
        self.frame.pack(side=BOTTOM,ipady=10)
    def start(self):
        global special
        global r_freq
        global l_freq
        if self.text1.get()=='\n':
            showerror(title='错误',message='分词输入内容不能为空！')
        else:
            self.text.set('正在分词，请耐心等待………')
            result=[]
            special={}
            if self.menu.v.get() == 1:
                if self.AW.text1.get() != '':
                    temp=special_divide(self.text1.get(),self.AW.text1.get())
                else:
                    temp=self.text1.get()
                sentences=divide(temp)
                if self.AW.v.get() == 1:
                    for i in sentences:
                        if i in special:
                            result.append(i)
                        else:
                            r_freq=0
                            l_freq=0
                            result.append(accurate_seg(i))
                else:
                    for i in sentences:
                        if i in special:
                            result.append(i)
                        else:
                            r_freq=0
                            l_freq=0
                            r=left_seg(i)
                            if r[0]=='/':
                                r=r[1:]
                            result.append(r)
            if self.menu.v.get() == 2:
                sentences=divide(self.text1.get())
                for i in range(len(sentences)):
                    r_freq=0
                    l_freq=0
                    result.append(fast_seg(sentences[i]))

            self.text2.insert('/'.join(result))
            self.text.set('分词完毕')
    def clean1(self):
        if askquestion(title='提示',message='真的要清空分词原文么？') == 'yes':
            self.text1.clear()
    def clean2(self):
        if askquestion(title='提示',message='真的要清空分词结果么？') == 'yes':
            self.text2.clear()
            self.text.set('')
class MyText:   #文本输入/输出框
    def __init__(self,root,type):
        self.root=root
        self.frame1=Frame(root)
        if type==0:
            self.lb=Label(self.frame1,text='分词原文')
            self.lb.pack()
            self.frame1.pack()
        if type==1:
            self.lb=Label(self.frame1,text='分词结果')
            self.lb.pack()
            self.frame1.pack()
        self.frame=Frame(root)
        self.T=Text(self.frame,width=100,height=12)
        self.sl=Scrollbar(self.frame)
        self.sl.pack(side=RIGHT,fill=Y)
        self.T['yscrollcommand']=self.sl.set
        self.T.pack(side=LEFT)
        self.sl['command'] = self.T.yview
        self.frame.pack()
    def insert(self,r):
        self.T.insert(1.0,r)
    def clear(self):
        self.T.delete(1.0,END)
    def get(self):
        return self.T.get(1.0,END)
        #精准分词
class Addword:
    def __init__(self,root):
        self.root=root
        self.frame=Frame(root)
        self.text3='辅助词语(以|分隔)：'
        self.label1=Label(self.frame,text=self.text3)
        self.label1.pack(side=LEFT)
        self.text1=StringVar()
        self.entry1=Entry(self.frame,textvariable=self.text1,width=50)
        self.entry1.pack(side=LEFT,padx=20)
        self.v=IntVar()
        self.v.set(1)
        self.cb=Checkbutton(self.frame,text='双向分词',variable=self.v)
        self.cb.pack(side=LEFT,padx=20)
    def forget(self):
        self.frame.forget()
    def repack(self):
        self.frame.pack(pady=20)

root=Tk()
root.title('Chinese Word Segmentating System -Beta v3.0- Power by K.O.1')
text1=MyText(root,0)
text2=MyText(root,1)
AW=Addword(root)
menu=MyMenu(root,text1,text2,AW)
bottun=Mybottun(root,text1,text2,menu,AW)
root.mainloop()