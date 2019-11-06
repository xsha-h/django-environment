def dictfetchall(cursor):
    desc = cursor.description   # 得到列明
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()    # ((1,'zs',5),(),())
    ]
