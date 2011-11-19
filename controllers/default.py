#!/usr/bin/python
# -*- coding: utf-8 -*-

# from gluon.tools import Auth
# auth = Auth(DAL(None))

if session.auth and session.auth.user:
    time_expire = 0
else:
    time_expire = 300


#@auth.requires_login()
#@cache(request.env.path_info, time_expire=time_expire, cache_model=cache.ram)
def index():
    redirect(URL('home', 'index'))


def user():
    from movuca import Access, DataBase
    db = DataBase()
    access = Access(db)
    return dict(form=access(), auth=access)


def download():
    flnm = request.args(0)
    if request.env.web2py_runtime_gae:
        tbl, fld = flnm.split('.')[:2]
        from config import Config
        config = Config()
        config._db.define_table(tbl, Field(fld, "upload"), migrate=False)
        return response.download(request, config._db)
    else:
        import os
        response.stream(os.path.join(request.folder, 'uploads', flnm))


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
