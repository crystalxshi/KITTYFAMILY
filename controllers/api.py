# Here go your api methods.
# Here go your api methods.
import json
import traceback


@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_content=request.vars.post_content,
    )
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))

@auth.requires_signature()
def edit_post():
 db(db.post.id == request.vars.post_id).update(
     post_content = request.vars.post_content,
 )

@auth.requires_signature()
def delete_post():
 db(db.post.id == request.vars.post_id).delete()


def get_post_list():
    results = []
    if auth.user is None:
        # Not logged in.
        rows = db().select(db.post.ALL, orderby=~db.post.id)
        thumbs = db().select(db.thumb.ALL)
        for row in rows:
            row.like_num = 0
            row.unlike_num = 0
            for thumb in thumbs:
                if thumb.post_id == row.id:
                    if thumb.thumb_state == 'u':
                        row.like_num = row.like_num + 1
        for row in rows:
            results.append(dict(
                id=row.id,
                post_content=row.post_content,
                post_author=row.post_author,
                like_num=row.like_num,
                thumb=None,
            ))
    else:
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                           left=[
                               db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                           ],
                           orderby=~db.post.post_time)
        thumbs = db().select(db.thumb.ALL)
        for row in rows:
            row.post.like_num = 0
            row.post.unlike_num = 0
            for thumb in thumbs:
                if thumb.post_id == row.post.id:
                    if thumb.thumb_state == 'u':
                        row.post.like_num = row.post.like_num + 1
        for row in rows:
            results.append(dict(
                id=row.post.id,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                like_num=row.post.like_num,
                thumb=None if row.thumb.id is None else row.thumb.thumb_state,
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))

def set_like():
    if auth.user is None:
        return response.json(dict(code=-1,msg="need login"))
    sql='insert or replace into thumb (user_email,post_id,thumb_state) values ("'+auth.user.email+'",'+request.vars.post_id+',"'+request.vars.thumb_state+'")'
    db.executesql(sql)
    return response.json(dict(code=0))
def user():
    return response.json(auth.user)

def get_logged_in_user():
   user = None if auth.user == None else auth.user.email
   return response.json(dict(user = user))
