from django.db import models, connection
from collections import namedtuple


# Create your models here.
class Data(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    display = models.BooleanField()
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data'


class Source(models.Model):
    name = models.TextField()
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'source'


def fund_datas(**kwargs):
    idk = kwargs.get('id')
    if idk:
        result = Data.objects.raw('select * from data where id = %s', [idk])
    else:
        result = Data.objects.raw('select * from data')
    return result


def update_text(**kwargs):
    category = kwargs.get('category')
    tag = kwargs.get('tag')
    display = kwargs.get('display')
    id = kwargs.get('id')
    print(category, tag, display, id)
    cursor = connection.cursor()
    cursor.execute("update data\
                            set\
                                category = '%s',\
                                tag = '%s',\
                                display = '%s'\
                            where id = '%s'" % (category, tag, display, id))
    num = cursor.rowcount
    return num

    # with connection.cursor() as cursor:

    # cursor.execute("select * from data where id = %s", [id])
    # result = nametuplefetchall(cursor)
    # result = [
    #     {
    #         'id': r.id,
    #         'title': r.title,
    #         'time': r.time,
    #         'link': r.link,
    #         'author': r.author,
    #         'text': r.text,
    #         'images': r.images,
    #         'category': r.category,
    #         'tag': r.tag,
    #         'display': r.display
    #     }
    #     for r in result
    # ]
    #
    # return result


def nametuplefetchall(cursor):
    desc = cursor.description
    print(desc)
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def dbget_info_min():
    with connection.cursor() as cursor:
        cursor.execute("select id,title,author, category,tag,display, source\
                        from data")
        result = nametuplefetchall(cursor)
        result = [
            {'id': r.id,
             'title': r.title,
             'author': r.author,
             'category': r.category,
             'tag': r.tag,
             'display': r.display,
             'source': r.source
             }
            for r in result
        ]
        cursor.close()

        return result


def verify_account(**kwargs):
    account = kwargs.get('account')
    password = kwargs.get('password')
    cursor = connection.cursor()
    cursor.execute("select exists(\
                       select account, password\
                       from members\
                       where account = '%s'\
                         and password = '%s')" % (account, password)
                   )
    result = cursor.fetchone()[0]
    if result:
        member_hash = hash(account)
        cursor.execute("update members\
                        set hash = %s\
                        where account = %s", [member_hash, account])
        print(member_hash)
        return member_hash
    return result


def check_hash(account, hashnum):
    cursor = connection.cursor()
    print(hashnum)
    print('asd')
    cursor.execute("select hash\
                    from members\
                    where account = '%s'" % (account))
    re = cursor.fetchone()
    print(re[0])

    if re[0] == hashnum:
        return True
    return False


def delete_byid(id):
    cursor = connection.cursor()
    cursor.execute("delete from data\
                        where id = '%s'" % (id))
    result = cursor.rowcount
    cursor.close()
    return result


def getfulltext(**kwargs):
    id = kwargs.get('id')
    cursor = connection.cursor()
    if id:
        cursor.execute("select id, title, time, author, text, images, source\
                        from data\
                        where display = 't' and id = '%s'" % (id))
    else:
        cursor.execute("select id, title, time, author, text, images, source\
                                from data\
                                where display = 't'")
    result = nametuplefetchall(cursor)
    result = [
        {'id': r.id,
         'title': r.title,
         'time': r.time,
         'author': r.author,
         'text': r.text,
         'images': r.images,
         'source': r.source
         }
        for r in result
    ]
    cursor.close()
    return result


# 　廢棄用
def get_text_by_source_server(source):
    cursor = connection.cursor()
    cursor.execute("select id, title, source, category, tag, display\
                    from data\
                    where source = '%s'" % (source))
    result = cursor.fetchall()
    cursor.close()
    return result


# 廢棄用
def get_text_by_source_client(source):
    cursor = connection.cursor()
    cursor.execute("select id, title, category, time, text, images\
                    from data\
                    where source = '%s'" % (source))
    result = cursor.fetchall()
    cursor.close()
    return result


def return_source():
    cursor = connection.cursor()
    cursor.execute("select source\
                    from data\
                    group by source")
    result = cursor.fetchall()
    cursor.close()
    print(result)
    print(type(result[0]))
    print(result[0])
    return result


def get_info_in_page_server(**kwargs):
    page = kwargs.get('page')
    source = kwargs.get('source')

    cursor = connection.cursor()
    sql = "select id, title, source, category, tag, display\
                    from data\n"
    if source:
        sql += "where source = '%s'\n" % (source)
    sql += "limit 20 offset " + str((page - 1) * 20)
    cursor.execute(sql)
    result = cursor.fetchall()

    sql = "select count(id) from data"
    if source:
        sql += " where source = '%s'" % (source)
    cursor.execute(sql)
    num = cursor.fetchone()
    print(num)
    # result.append(num)

    return result, num


def get_info_in_page_client(**kwargs):
    page = kwargs.get('page')
    source = kwargs.get('source')

    cursor = connection.cursor()
    sql = "select id, title, time,text, images\
                    from data\n\
                    where display = 't'"

    if source:
        sql += " and source = '%s'" % (source)
    sql += "\nlimit 12 offset " + str((page - 1) * 12)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()

    sql = "select count(id) from data"
    if source:
        sql += " where display = 't' and source = '%s'" % (source)
    cursor.execute(sql)
    num = cursor.fetchone()
    print(num)
    cursor.close()

    return result, num


def search_data(title):
    cursor = connection.cursor()
    cursor.execute("select id, title, source, category, tag, display\
                    from data\
                    where (select title ~ '%s')" % (title))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_source():
    cursor = connection.cursor()
    cursor.execute("select *\
                    from source\
                    order by id")
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return result


def insert_source(**kwargs):
    name = kwargs.get('name')
    url = kwargs.get('url')
    id = kwargs.get('id')
    cursor = connection.cursor()

    if id:
        sql = "insert into source (id, name, url)\
                            values ('%s', '%s', '%s');" % (id, name, url)
    else:
        sql = "insert into source (name, url)\
                            values ('%s', '%s');" % (name, url)
    cursor.execute(sql)
    result = cursor.rowcount
    cursor.close()
    return result


def delete_source(id):
    cursor = connection.cursor()
    cursor.execute("delete from source\
                    where id = '%s'" % (id))
    result = cursor.rowcount
    cursor.close()
    return result
