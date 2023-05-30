from flask import Blueprint, render_template,request,session
from flask_paginate import get_page_parameter, Pagination
from models import Food,Fencifanwei,Fencibiao
import jieba
from sqlalchemy import desc

#分页用的这个函数返回两个参数记得用两个变量装（foods和pagination）a是判断是否有筛选操作重置页数
def fenye(foods,a):
    foods = list(foods)
    if a==0:
        page = request.args.get(get_page_parameter(), type=int, default=1)
    else:
        page=1
    # 每页显示多少条
    per_page = 10
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
    # 获取当前页数据
    start = (page - 1) * per_page
    end = start + per_page
    return foods[start:end],pagination



bp=Blueprint("search",__name__,url_prefix="/search")

@bp.route("/",methods=['POST', 'GET'])
def search():
    content = request.form.get('content')
    type = request.form.get('text')
    paixu = request.form.get('paixu')
    jingque=request.form.get('jingque')
    print(jingque)
    if jingque:
        session['searchtype']=jingque
    g=0
    if type:
        session['type2']=type
        g=1
    if paixu:
        session['paixu']=paixu
        g=1
    #没有输入检索词的情况分两种一种是在翻页一种是未在检索并且筛选操作都是在未输入检索词下进行的所以只需在未输入检索词情况下定义
    if content is None:
        #判读是否处于精确检索状态
        searchtype = session.get('searchtype')
        print('pdjqq',searchtype)
        if searchtype:
            a = Fencifanwei.query.filter(Fencifanwei.word.like(session['search'])).all()
            totallist = {}
            for t in a:
                p = t.began
                o = t.down
                # 建范围列表
                mylist = []
                for q in range(p, o + 1):
                    mylist.append(q)

                b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                for k in b:
                    if k.fnum in totallist:
                        totallist[k.fnum] += 1
                    else:
                        totallist[k.fnum] = 1

             # 越多交集排前面
            d = list(totallist.items())
            d.sort(key=lambda x: x[1], reverse=True)
            mylist = []
            for k in d:
                mylist.append(k[0])
            if mylist == []:
                content = session.get('search')
                a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                for k in a:
                    mylist.append(k.fnum)
            type = session.get('type2')
            paixu = session.get('paixu')
            # 如果有在分类筛选
            if type:
                print('有分')
                # 如果有在排序筛序
                if paixu:
                    print('有排')
                    if paixu == '升序':
                        print('sx')
                        foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist), Food.type2 == type).all()
                        foods, pagination = fenye(foods, g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z ,food=foods, pagination=pagination, type=type)
                    else:
                        print('jx')
                        foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist),
                                                                              Food.type2 == type).all()
                        foods, pagination = fenye(foods, g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination, type=type)
                # 如果没有排序筛选
                else:
                    print('没排')
                    foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist), Food.type2 == type).all()
                    foods, pagination = fenye(foods, g)
                    z = 0
                    if foods == []:
                        z = 1
                    return render_template("search1.html",z=z, food=foods, pagination=pagination, type=type)
            # 如果没有在分类筛选
            else:
                print('没分')
                # 如果有在排序筛选
                if paixu:
                    print('有排')
                    if paixu == '升序':
                        print('sx')
                        foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist)).all()
                        foods, pagination = fenye(foods, g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination)
                    else:
                        print('jiang')
                        foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist)).all()
                        foods, pagination = fenye(foods, g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination)
                # 如果没在排序筛选
                else:
                    print('没排')
                    foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
                    foods, pagination = fenye(foods, g)
                    z = 0
                    if foods == []:
                        z = 1
                    return render_template("search1.html",z=z, food=foods, pagination=pagination)
        #没处于精确搜索状态
        else:
            print('没精确')
            # session['search'] = '蛋白棒'                 #测试用的
            # session.permanent = True
            # 实现在检索页翻页
            content=session.get('search')
            d = ("/".join(jieba.lcut(session['search'], cut_all=True)))
            word = d.split("/")
            print(word)
            totallist = {}
            # 取每个切词并集
            for i in word:
                a = Fencifanwei.query.filter(Fencifanwei.word.like(i)).all()

                for t in a:
                    p = t.began
                    o = t.down
                    # 建范围列表
                    mylist = []
                    for q in range(p, o + 1):
                        mylist.append(q)

                    b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                    for k in b:
                        if k.fnum in totallist:
                            totallist[k.fnum] += 1
                        else:
                            totallist[k.fnum] = 1

            # 越多交集排前面
            d = list(totallist.items())
            d.sort(key=lambda x: x[1], reverse=True)
            mylist = []
            a = Food.query.filter(Food.fname.like('{content}%'.format(content=content))).all()
            for i in a:
                mylist.append(i.fnum)
            for k in d:
                if k[0] not in mylist:
                    mylist.append(k[0])
            if mylist == []:
                content = session.get('search')
                a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                for k in a:
                    mylist.append(k.fnum)
            print(mylist)
            foods1 = Food.query.filter(Food.fnum.in_(mylist)).order_by(Food.fnum).all()
            foods = []
            for i in mylist:
                for t, k in enumerate(foods1):
                    if i == k.fnum:
                        foods.append(foods1[t])

            a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
            for k in a:
                if k not in foods:
                    foods.append(k)
            for i in foods:
                if i.fnum not in mylist:
                    mylist.append(i.fnum)
            type=session.get('type2')
            paixu=session.get('paixu')
            #如果有在分类筛选
            if type:
                print('有分')
                #如果有在排序筛序
                if paixu:
                    print('有排')
                    if paixu=='升序':
                        print('sx')
                        foods=Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist),Food.type2 == type).all()
                        foods,pagination=fenye(foods,g)
                        z = 0
                        if foods == []:
                            z = 1

                        return render_template("search1.html",z=z, food=foods, pagination=pagination,type=type)
                    else:
                        print('jx')
                        foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist), Food.type2 == type).all()
                        foods,pagination = fenye(foods,g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination, type=type)
                # 如果没有排序筛选
                else:
                    print('没排')
                    foods1 = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist), Food.type2 == type).all()
                    foods = []
                    for i in mylist:
                        for t, k in enumerate(foods1):
                            if i == k.fnum:
                                foods.append(foods1[t])
                    foods,pagination = fenye(foods,g)
                    z = 0
                    if foods == []:
                        z = 1
                    return render_template("search1.html",z=z, food=foods, pagination=pagination, type=type)
            #如果没有在分类筛选
            else:
                print('没分')
                # 如果有在排序筛选
                if paixu:
                    print('有排')
                    if paixu == '升序':
                        print('sx')
                        foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist)).all()
                        foods,pagination = fenye(foods,g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination)
                    else:
                        print('jiang')
                        foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist)).all()
                        foods,pagination = fenye(foods,g)
                        z = 0
                        if foods == []:
                            z = 1
                        return render_template("search1.html",z=z, food=foods, pagination=pagination)
                #如果没在排序筛选
                else:
                    print('没排')
                    foods1 = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
                    foods = []
                    for i in mylist:
                        for t, k in enumerate(foods1):
                            if i == k.fnum:
                                foods.append(foods1[t])
                    foods,pagination = fenye(foods,g)
                    z = 0
                    if foods == []:
                        z = 1
                    return render_template("search1.html",z=z, food=foods, pagination=pagination)




    #正常的检索实现
    else:
        session['search'] = content
        session.permanent = True
        #判断检索状态
        if jingque:
            a = Fencifanwei.query.filter(Fencifanwei.word.like(content)).all()
            totallist = {}
            for t in a:
                p = t.began
                o = t.down
                # 建范围列表
                mylist = []
                for q in range(p, o + 1):
                    mylist.append(q)

                b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                for k in b:
                    if k.fnum in totallist:
                        totallist[k.fnum] += 1
                    else:
                        totallist[k.fnum] = 1

                # 越多交集排前面
            d = list(totallist.items())
            d.sort(key=lambda x: x[1], reverse=True)
            mylist = []
            for k in d:
                mylist.append(k[0])
            if mylist == []:
                content = session.get('search')
                a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                for k in a:
                    mylist.append(k.fnum)
            foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
            page = 1
            # 每页显示多少条
            per_page = 10
            # 分页处理
            pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
            # 获取当前页数据
            start = (page - 1) * per_page
            end = start + per_page
            foods = foods[start:end]
            type = session.get('type2')
            paixu = session.get('paixu')
            if type:
                session.pop('type2')
            if paixu:
                session.pop('paixu')
            z = 0
            if foods == []:
                z = 1
            return render_template("search1.html",z=z, food=foods, pagination=pagination)
        else:
            searchtype=session.get('searchtype')
            if searchtype:
                session.pop('searchtype')
            print(searchtype)
            d = ("/".join(jieba.lcut(content, cut_all=True)))
            word= d.split("/")
            print(word)
            totallist={}
            #取每个切词并集
            for i in word:
                a=Fencifanwei.query.filter(Fencifanwei.word.like( i )).all()

                for t in a:
                    p=t.began
                    o=t.down
                    #建范围列表
                    mylist=[]
                    for q in range(p,o+1):
                        mylist.append(q)

                    b=Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                    for k in b:
                        if k.fnum in totallist:
                            totallist[k.fnum]+=1
                        else:
                            totallist[k.fnum]=1

            #越多交集排前面
            d=list(totallist.items())
            d.sort(key=lambda x:x[1],reverse=True)
            mylist=[]
            a=Food.query.filter(Food.fname.like('{content}%'.format(content=content))).all()
            for i in a:
                mylist.append(i.fnum)
            for k in d:
                if k[0] not in mylist:
                    mylist.append(k[0])
            if mylist == []:
                content = session.get('search')
                a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                for k in a:
                    mylist.append(k.fnum)
            print(mylist)
            foods1 = Food.query.filter(Food.fnum.in_(mylist)).order_by(Food.fnum).all()
            foods=[]
            for i in mylist:
                for t,k in enumerate(foods1):
                    if i== k.fnum:
                        foods.append(foods1[t])
            print(foods)
            a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
            for k in a:
                if k not in foods:
                    foods.append(k)
            page = 1
            # 每页显示多少条
            per_page = 10
            # 分页处理
            pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
            # 获取当前页数据
            start = (page - 1) * per_page
            end = start + per_page
            foods = foods[start:end]
            type = session.get('type2')
            paixu = session.get('paixu')
            if type:
                session.pop('type2')
            if paixu:
                session.pop('paixu')
            print(foods)
            z=0
            if foods==[]:
                z=1
                print(z)
            return render_template("search1.html", z=z,food=foods, pagination=pagination)


#实现添加记录
@bp.route("/search2",methods=['POST', 'GET'])
def search1():
    content = request.form.get('content')
    type = request.form.get('text')
    paixu = request.form.get('paixu')
    jingque = request.form.get('jingque')
    zt=request.form.get('food_ct')
    if jingque:
        session['searchtype'] = jingque
    g=0
    if type:
        session['type2']=type
        g=1
    if paixu:
        session['paixu']=paixu
        g=1

    #刚从记录页面跳转
    if zt:
        foods=Food.query.filter(Food.type2=='主食')
        session['type2'] = '主食'
        type='主食'
        session.permanent = True
        foods=list(foods)
        #获取当前页码
        page = 1
        #每页显示多少条
        per_page=10
        #分页处理
        pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
        #获取当前页数据
        start = (page - 1) * per_page
        end = start + per_page
        foods= foods[start:end]
        search=session.get('search')
        if search:
            session.pop('search')
        return render_template("search2.html",food=foods,pagination=pagination,type=type)

    # 如果不是刚从记录页面进来
    else:
        # 没有输入检索词的情况分两种一种是在翻页一种是未在检索并且筛选操作都是在未输入检索词下进行的所以只需在未输入检索词情况下定义
        if content is None:
            # session['search'] = '蛋白棒'                 #测试用的
            # session.permanent = True
            # 实现在检索页翻页

            search = session.get('search')
            # 如果有在搜索
            if search:
                # 判断检索状态
                searchtype = session.get('searchtype')
                print(searchtype)
                if searchtype:
                    a = Fencifanwei.query.filter(Fencifanwei.word.like(session['search'])).all()
                    totallist = {}
                    for t in a:
                        p = t.began
                        o = t.down
                        # 建范围列表
                        mylist = []
                        for q in range(p, o + 1):
                            mylist.append(q)

                        b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                        for k in b:
                            if k.fnum in totallist:
                                totallist[k.fnum] += 1
                            else:
                                totallist[k.fnum] = 1

                    # 越多交集排前面
                    d = list(totallist.items())
                    d.sort(key=lambda x: x[1], reverse=True)
                    mylist = []
                    for k in d:
                        mylist.append(k[0])
                    if mylist == []:
                        content = session.get('search')
                        a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                        for k in a:
                            mylist.append(k.fnum)
                    type = session.get('type2')
                    paixu = session.get('paixu')
                    # 如果有在分类筛选
                    if type:
                        print('有分')
                        # 如果有在排序筛序
                        if paixu:
                            print('有排')
                            if paixu == '升序':
                                print('sx')
                                foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist),
                                                                                Food.type2 == type).all()
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                            else:
                                print('jx')
                                foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist),
                                                                                      Food.type2 == type).all()
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                        # 如果没有排序筛选
                        else:
                            print('没排')
                            foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist),
                                                                          Food.type2 == type).all()
                            foods, pagination = fenye(foods, g)
                            z = 0
                            if foods == []:
                                z = 1
                                print(z)
                            return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                    # 如果没有在分类筛选
                    else:
                        print('没分')
                        # 如果有在排序筛选
                        if paixu:
                            print('有排')
                            if paixu == '升序':
                                print('sx')
                                foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist)).all()
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination)
                            else:
                                print('jiang')
                                foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist)).all()
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination)
                        # 如果没在排序筛选
                        else:
                            print('没排')
                            foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
                            foods, pagination = fenye(foods, g)
                            z = 0
                            if foods == []:
                                z = 1
                                print(z)
                            return render_template("search2.html",z=z, food=foods, pagination=pagination)
                # 没在精确检索状态的检索
                else:
                    content=session.get('search')
                    d = ("/".join(jieba.lcut(session['search'], cut_all=True)))
                    word = d.split("/")
                    print(word)
                    totallist = {}
                    # 取每个切词并集
                    for i in word:
                        a = Fencifanwei.query.filter(Fencifanwei.word.like(i)).all()

                        for t in a:
                            p = t.began
                            o = t.down
                            # 建范围列表
                            mylist = []
                            for q in range(p, o + 1):
                                mylist.append(q)

                            b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                            for k in b:
                                if k.fnum in totallist:
                                    totallist[k.fnum] += 1
                                else:
                                    totallist[k.fnum] = 1

                        # 越多交集排前面
                        d = list(totallist.items())
                        d.sort(key=lambda x: x[1], reverse=True)
                        mylist = []
                        a = Food.query.filter(Food.fname.like('{content}%'.format(content=content))).all()
                        for i in a:
                            mylist.append(i.fnum)
                        for k in d:
                            if k[0] not in mylist:
                                mylist.append(k[0])
                        if mylist == []:
                            content = session.get('search')
                            a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                            for k in a:
                                mylist.append(k.fnum)
                        print(mylist)
                        foods1 = Food.query.filter(Food.fnum.in_(mylist)).order_by(Food.fnum).all()
                        foods = []
                        for i in mylist:
                            for t, k in enumerate(foods1):
                                if i == k.fnum:
                                    foods.append(foods1[t])

                        a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                        for k in a:
                            if k not in foods:
                                foods.append(k)
                        for i in foods:
                            if i.fnum not in mylist:
                                mylist.append(i.fnum)
                        type = session.get('type2')
                        paixu = session.get('paixu')
                        # 如果有在分类筛选
                        if type:
                            print('有分')
                            # 如果有在排序筛序
                            if paixu:
                                print('有排')
                                if paixu == '升序':
                                    print('sx')
                                    foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist),
                                                                                    Food.type2 == type).all()
                                    foods, pagination = fenye(foods, g)
                                    z = 0
                                    if foods == []:
                                        z = 1
                                        print(z)
                                    return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                                else:
                                    print('jx')
                                    foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist),
                                                                                          Food.type2 == type).all()
                                    foods, pagination = fenye(foods, g)
                                    z = 0
                                    if foods == []:
                                        z = 1
                                        print(z)
                                    return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                            # 如果没有排序筛选
                            else:
                                print('没排')
                                foods1 = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist),
                                                                              Food.type2 == type).all()
                                foods = []
                                for i in mylist:
                                    for t, k in enumerate(foods1):
                                        if i == k.fnum:
                                            foods.append(foods1[t])
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination, type=type)
                        # 如果没有在分类筛选
                        else:
                            print('没分')
                            # 如果有在排序筛选
                            if paixu:
                                print('有排')
                                if paixu == '升序':
                                    print('sx')
                                    foods = Food.query.order_by(Food.energy).filter(Food.fnum.in_(mylist)).all()
                                    foods, pagination = fenye(foods, g)
                                    z = 0
                                    if foods == []:
                                        z = 1
                                        print(z)
                                    return render_template("search2.html",z=z, food=foods, pagination=pagination)
                                else:
                                    print('jiang')
                                    foods = Food.query.order_by(desc(Food.energy)).filter(Food.fnum.in_(mylist)).all()
                                    foods, pagination = fenye(foods, g)
                                    z = 0
                                    if foods == []:
                                        z = 1
                                        print(z)
                                    return render_template("search2.html",z=z, food=foods, pagination=pagination)
                            # 如果没在排序筛选
                            else:
                                print('没排')
                                foods1 = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
                                foods = []
                                for i in mylist:
                                    for t, k in enumerate(foods1):
                                        if i == k.fnum:
                                            foods.append(foods1[t])
                                foods, pagination = fenye(foods, g)
                                z = 0
                                if foods == []:
                                    z = 1
                                    print(z)
                                return render_template("search2.html",z=z, food=foods, pagination=pagination)
            # 如果没在搜索
            else:
                type = request.form.get('text')
                paixu = request.form.get('paixu')
                g = 0
                if type:
                    session['type2'] = type
                    g = 1
                if paixu:
                    session['paixu'] = paixu
                    g = 1
                # 如果现在点击分类
                if type:
                    print('1')
                    if type:
                        session['type2'] = type
                        session.permanent = True
                    foods = Food.query.filter(Food.type2 == type)

                    foods, pagination = fenye(foods, g)
                    return render_template("search2.html", food=foods, pagination=pagination, type=type)
                # 如果没有点击分类
                else:

                    print('2')
                    type = session.get('type2')
                    if type:
                        type = type
                        g = 0
                    else:
                        type = '主食'
                        g = 1
                    # 如果现在有点击排序
                    if paixu != None:
                        g = 1
                        print('px')
                        if paixu == '升序':
                            session['paixu'] = paixu
                            session.permanent = True
                            foods = Food.query.filter(Food.type2 == type).order_by(Food.energy)
                        else:
                            session['paixu'] = paixu
                            session.permanent = True
                            foods = Food.query.filter(Food.type2 == type).order_by(desc(Food.energy))
                    # 如果没有点击排序但之前有
                    else:
                        paixu = session.get('paixu')

                        if paixu == '升序':
                            foods = Food.query.filter(Food.type2 == type).order_by(Food.energy)
                            g = 0
                        elif paixu == '降序':
                            foods = Food.query.filter(Food.type2 == type).order_by(desc(Food.energy))
                            g = 0
                        else:
                            foods = Food.query.filter(Food.type2 == type)
                            g = 0

                    foods, pagination = fenye(foods, g)
                    return render_template("search2.html", food=foods, pagination=pagination, type=type)

        # 正常的检索实现
        else:
            session['search'] = content
            session.permanent = True
            if jingque:
                a = Fencifanwei.query.filter(Fencifanwei.word.like(content)).all()
                totallist = {}
                for t in a:
                    p = t.began
                    o = t.down
                    # 建范围列表
                    mylist = []
                    for q in range(p, o + 1):
                        mylist.append(q)

                    b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                    for k in b:
                        if k.fnum in totallist:
                            totallist[k.fnum] += 1
                        else:
                            totallist[k.fnum] = 1

                    # 越多交集排前面
                d = list(totallist.items())
                d.sort(key=lambda x: x[1], reverse=True)
                mylist = []
                for k in d:
                    mylist.append(k[0])
                if mylist == []:
                    content = session.get('search')
                    a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                    for k in a:
                        mylist.append(k.fnum)
                foods = Food.query.order_by(Food.fnum).filter(Food.fnum.in_(mylist)).all()
                page = 1
                # 每页显示多少条
                per_page = 10
                # 分页处理
                pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
                # 获取当前页数据
                start = (page - 1) * per_page
                end = start + per_page
                foods = foods[start:end]
                type = session.get('type2')
                paixu = session.get('paixu')
                if type:
                    session.pop('type2')
                if paixu:
                    session.pop('paixu')
                return render_template("search2.html", food=foods, pagination=pagination)
            else:
                d = ("/".join(jieba.lcut(content, cut_all=True)))
                word = d.split("/")
                print(word)
                totallist = {}
                # 取每个切词并集
                for i in word:
                    a = Fencifanwei.query.filter(Fencifanwei.word.like(i)).all()

                    for t in a:
                        p = t.began
                        o = t.down
                        # 建范围列表
                        mylist = []
                        for q in range(p, o + 1):
                            mylist.append(q)

                        b = Fencibiao.query.order_by(Fencibiao.wnum).filter(Fencibiao.wnum.in_(mylist)).all()

                        for k in b:
                            if k.fnum in totallist:
                                totallist[k.fnum] += 1
                            else:
                                totallist[k.fnum] = 1

                # 越多交集排前面
                d = list(totallist.items())
                d.sort(key=lambda x: x[1], reverse=True)
                mylist = []
                a = Food.query.filter(Food.fname.like('{content}%'.format(content=content))).all()
                for i in a:
                    mylist.append(i.fnum)
                for k in d:
                    if k[0] not in mylist:
                        mylist.append(k[0])
                if mylist == []:
                    content = session.get('search')
                    a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                    for k in a:
                        mylist.append(k.fnum)
                print(mylist)
                foods1 = Food.query.filter(Food.fnum.in_(mylist)).order_by(Food.fnum).all()
                foods = []
                for i in mylist:
                    for t, k in enumerate(foods1):
                        if i == k.fnum:
                            foods.append(foods1[t])

                a = Food.query.filter(Food.fname.like('%{content}%'.format(content=content))).all()
                for k in a:
                    if k not in foods:
                        foods.append(k.fnum)
                page = 1
                # 每页显示多少条
                per_page = 10
                # 分页处理
                pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
                # 获取当前页数据
                start = (page - 1) * per_page
                end = start + per_page
                foods = foods[start:end]
                type = session.get('type2')
                paixu = session.get('paixu')
                if type:
                    session.pop('type2')
                if paixu:
                    session.pop('paixu')
                return render_template("search2.html", food=foods, pagination=pagination)


