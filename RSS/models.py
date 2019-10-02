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

    with connection.cursor() as cursor:
        cursor.execute("update data\
                        set\
                            category = %s,\
                            tag = %s,\
                            display = %s\
                        where id = %s", [category, tag, display, id])
        cursor.execute("select * from data where id = %s", [id])
        result = nametuplefetchall(cursor)
        result = [
            {
                'id': r.id,
                'title': r.title,
                'time': r.time,
                'link': r.link,
                'author': r.author,
                'text': r.text,
                'images': r.images,
                'category': r.category,
                'tag': r.tag,
                'display': r.display
            }
            for r in result
        ]

        return result


def nametuplefetchall(cursor):
    desc = cursor.description
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


def getfulltext():
    cursor = connection.cursor()
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
