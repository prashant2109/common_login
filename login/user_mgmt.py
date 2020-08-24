import common.dbcrypt_intf as dbcrypt
import db.get_conn as get_conn
conn_obj    = get_conn.DB()
class User():
    def login(self, ijson, login_db):
        user_id, user_pass  = ijson['istr'].split(':$:')
        conn, cur   = conn_obj.MySQLdb_connection(login_db)
        enc_user_pass   = dbcrypt.encryptIVfix(user_pass)
        sel_sql         = "select * from login_master where user_id = '%s' and user_passwd = '%s'"%(user_id, enc_user_pass)
        cur.execute(sel_sql)
        user_ar         = cur.fetchone()
        tdict = {}
        if user_ar:
            user_id,user_passwd,user_name,user_role,login_status,unique_key,user_time = user_ar
            tdict = {'user_id':user_id,'user_passwd':user_pass,'user_name':user_name,'user_role':user_role,'login_status':login_status,'unique_key':unique_key,'user_time':user_time}
            return tdict
        else:
            return {}
