from django.contrib.auth.models import Group
from django.db import connection
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from fetchdata import dictfetchall
from permission.schemas import UpdatePermissionSchema, DeletePermissionSchema, AddPermissionSchema


class PermissionView(APIView):
    """
    权限管理数据表格
    """
    def get(self, request):
        cursor = connection.cursor()
        sql = """
            select g_id, name, p_names, group_concat(auth_user.username) as u_names
            from (select auth_group.id as g_id, auth_group.name, group_concat(auth_permission.name) as p_names
                from auth_group left join auth_group_permissions 
                on auth_group.id = auth_group_permissions.group_id
                left join auth_permission on auth_group_permissions.permission_id = auth_permission.id
                group by auth_group.id) as gp 
                left join auth_user_groups on gp.g_id = auth_user_groups.group_id
                left join auth_user on auth_user_groups.user_id = auth_user.id
                group by group_id;
        """

        cursor.execute(sql)
        res_dict = dictfetchall(cursor)
        cursor.close()
        return Response(res_dict)


class UpdatePermissionView(APIView):
    """
    修改角色的权限，或者修改角色下的用户
    """
    schema = UpdatePermissionSchema

    def post(self, request):
        cursor = connection.cursor()
        id = request.data.get("id")
        names = request.data.get("names")
        tag = int(request.data.get("tag"))
        # 根据标志选取操作的表名
        if tag == 1:
            select_table = "auth_permission"
            update_table = "auth_group_permissions"
        elif tag == 2:
            select_table = "auth_user"
            update_table = "auth_user_groups"
        else:
            return Response(data={"code": 400, "message": "修改失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 将名称变成id
        names = names.split(",")
        for i in range(len(names)):
            sql = """
                select id
                from {}
                where name='{}';
            """.format(select_table, names[i])
            cursor.execute(sql)
            res = cursor.fetchone()
            names[i] = res[0]

        try:
            with transaction.atomic():

                # 删除当前角色下的所有权限或者用户
                delete_sql = """
                    delete
                    from {}
                    where group_id = '{}';
                """.format(update_table, id)
                cursor.execute(delete_sql)

                # 赋予角色权限或者用户
                for name in names:
                    insert_sql = """
                        insert into {} (group_id, permission_id)
                        values ('{}', '{}')
                    """.format(update_table, id, name)
                    cursor.execute(insert_sql)
        except:
            cursor.close()
            return Response(data={"code": 400, "message": "修改失败"}, status=status.HTTP_400_BAD_REQUEST)
        cursor.close()
        return Response(data={"code": 200, "message": "修改成功"}, status=status.HTTP_200_OK)


class DeletePermissionView(APIView):
    """
    撤权及撤销用户
    """
    schema = DeletePermissionSchema

    def post(self, request):
        try:
            id = request.data.get("id")
            cursor = connection.cursor()
            # 在角色权限表中撤销当前角色下的所有权限
            sql = """
                delete
                from auth_group_permissions
                where group_id = '{}';
            """.format(id)
            cursor.execute(sql)
            # 在角色用户表中删除当前角色下的所有用户
            sql = """
                delete
                from auth_user_groups
                where group_id = '{}';
            """.format(id)
            cursor.execute(sql)
        except:
            cursor.close()
            return Response(data={"code": 400, "message": "操作失败"}, status=status.HTTP_400_BAD_REQUEST)
        cursor.close()
        return Response(data={"code": 200, "message": "操作成功"}, status=status.HTTP_200_OK)


class AddPermissionView(APIView):
    """
    创建角色
    """
    schema = AddPermissionSchema

    def post(self, request):
        cursor = connection.cursor()
        role_name = request.data.get("role_name")
        permission_names = request.data.get("permission_names")
        user_names = request.data.get("user_names")

        # 将权限名称变成权限id
        permission_names = permission_names.split(",")
        if permission_names:
            for i in range(len(permission_names)):
                sql = """
                    select id
                    from auth_permission
                    where name='{}';
                """.format(permission_names[i])
                cursor.execute(sql)
                res = cursor.fetchone()
                permission_names[i] = res[0]

        # 将用户名称变成用户id
        user_names = user_names.split(",")
        if user_names:
            for i in range(len(user_names)):
                sql = """
                        select id
                        from auth_user
                        where username='{}';
                    """.format(user_names[i])
                cursor.execute(sql)
                res = cursor.fetchone()
                user_names[i] = res[0]

        try:
            # 创建角色
            sql = """
                insert into auth_group (name)
                values ('{}');
            """.format(role_name)
            cursor.execute(sql)
            # 角色id
            group_id = Group.objects.last().id
            if permission_names:
                for i in range(len(permission_names)):
                    # 给角色赋予权限
                    sql = """
                        insert into auth_group_permissions (group_id, permission_id)
                        values ('{}', '{}');
                    """.format(group_id, permission_names[i])
                    cursor.execute(sql)

            if user_names:
                for i in range(len(user_names)):
                    # 给角色增加用户
                    sql = """
                        insert into auth_user_groups (group_id, user_id)
                        values ('{}', '{}');
                    """.format(group_id, user_names[i])
                    cursor.execute(sql)
        except Exception as e:
            print(e)
            cursor.close()
            return Response(data={"code": 400, "message": "创建角色失败！"})
        cursor.close()
        return Response(data={"code": 200, "message": "创建角色成功！"})
