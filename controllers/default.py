# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime


def index():
    return dict()

@auth.requires_login()
def experience():
    return dict()

@auth.requires_login()

def adoption():
    adoption = db(db.adoption.is_available).select(db.adoption.ALL)
    logger.info('The session is: %r' % session)
    return dict(adoption=adoption)

@auth.requires_login()
def recommendation():
    recommend = db().select(db.recommend.ALL)
    logger.info('The session is: %r' % session)
    return dict(recommend=recommend)

@auth.requires_login()
def story():
    story = db().select(db.story.ALL)
    logger.info('The session is: %r' % session)
    return dict(story=story)

@auth.requires_login()
def addstory():
    form = SQLFORM(db.story)
    if form.process().accepted:
        redirect(URL('default', 'story'))
    logger.info("My session is: %r" % session)
    return dict(form=form)


@auth.requires_login()
def addrecommend():
    form = SQLFORM(db.recommend)
    if form.process().accepted:
        redirect(URL('default', 'recommendation'))
    # We ask web2py to lay out the form for us.
    logger.info("My session is: %r" % session)
    return dict(form=form)

@auth.requires_login()
def addcatinfo():
    form = SQLFORM(db.adoption)
    if form.process().accepted:
        redirect(URL('default', 'adoption'))
    # We ask web2py to lay out the form for us.
    logger.info("My session is: %r" % session)
    return dict(form=form)

@auth.requires_login()
def editcat():
    if request.args[0] is None:
        redirect(URL('default', 'adoption'))
    else:
        rows = ((db.adoption.post_author == auth.user.email)&
             (db.adoption.id == request.args[0]))
        r = db(rows).select().first()
        if r is None:
            redirect(URL('default', 'adoption'))

        url = URL('download')
        form = SQLFORM(db.adoption, record=r, upload=url)
        if form.process().accepted:
            redirect(URL('default', 'adoption'))
        return dict(form=form)

def ifavailable():
    if request.args[0] is not None:
        rows = ((db.adoption.post_author == auth.user.email) &
             (db.adoption.id == request.args[0]))
        r = db(rows).select().first()
        if r.is_available is True:
            r.update_record(is_available = False)
        else:
            r.update_record(is_available = True)
        redirect(URL('default', 'adoption'))

@auth.requires_login()
def viewcat():
    if request.args[0] is None:
        redirect(URL('default', 'adoption'))
    else:
        rows =(db.adoption.id == request.args(0))
        cat_infor = db(rows).select().first()
        if cat_infor is None:
            redirect(URL('default','adoption'))

        url = URL('download')
        form = SQLFORM(db.adoption, record=cat_infor, upload=url, deletable=False, readonly=True,writable=False)
        #lat1=db(db.catInfor.id == cl).select(db.catInfor.lat)
        #lng1 = db(db.catInfor.id == cl).select(db.catInfor.lng)


        if form.process().accepted:
            redirect(URL('default','adoption'))
        return dict(cat_infor = cat_infor)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


