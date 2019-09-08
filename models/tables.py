# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

# logger.info("The user record is: %r" % auth.user)

import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_current_time():
    return datetime.datetime.utcnow()

db.define_table('post',
                Field('post_author', default=get_user_email()),
                Field('post_title'),
                Field('post_content', 'text'),
                Field('post_time', 'datetime', update=get_current_time()),
                )

db.post.post_time.readable = db.post.post_time.writable = False
db.post.post_author.writable = False
db.post.id.readable = False
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)



db.define_table('adoption',
                Field('post_author', default = get_user_email()),
                Field('picture', 'upload', uploadfield='picture_file'),
                Field('picture_file', 'blob'),
                Field('cat_id', 'integer'),
                Field('cat_name'),
                Field('cat_breed'),
                Field('cat_gender'),
                Field('cat_age'),
                Field('rescue_group'),
                Field('phone','text'),
                Field('email', 'text'),
                Field('cat_intro','text'),
                Field('is_available', 'boolean', default=True),
                Field('post_time','datetime', update=get_current_time())
                )
db.adoption.post_author.writable = False
db.adoption.post_author.readable = False
db.adoption.post_time.writable = db.adoption.post_time.readable = False
db.adoption.id.readable = False
db.adoption.cat_gender.requires=IS_IN_SET(('Male', 'Female'))

db.define_table('thumb',
                Field('user_email'), # The user who thumbed, easier to just write the email here.
                Field('post_id', 'reference post'), # The thumbed post
                Field('thumb_state'), # This can be 'u' for up or 'd' for down, or None for... None.
                )
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS  thumb_post on  thumb(`user_email`, `post_id`);')

db.define_table('recommend',
                Field('post_author', default = get_user_email()),
                Field('picture', 'upload', uploadfield='picture_file'),
                Field('picture_file', 'blob'),
                Field('describes','text'),
                Field('post_time','datetime', update=get_current_time())
                )
db.recommend.post_author.writable = False
db.recommend.post_author.readable = False
db.recommend.post_time.writable = db.recommend.post_time.readable = False
db.recommend.id.readable = False

db.define_table('story',
                Field('post_author', default = get_user_email()),
                Field('video', 'upload', uploadfield='video_file'),
                Field('video_file', 'blob'),
                Field('describes','text'),
                Field('post_time','datetime', update=get_current_time())
                )
db.story.post_author.writable = False
db.story.post_author.readable = False
db.story.post_time.writable = db.story.post_time.readable = False
db.story.id.readable = False