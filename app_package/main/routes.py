from flask import Blueprint
from flask import render_template, jsonify, send_file, send_from_directory, \
    request, current_app
import os
import logging
from logging.handlers import RotatingFileHandler
from tr01_models import sess, Users, Rincons, RinconsPosts, UsersToRincons, \
    RinconsPostsComments, RinconsPostsLikes, RinconsPostsCommentsLikes
from app_package.main.utils import get_post_dict, extract_urls_info


main = Blueprint('main', __name__)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

logger_main = logging.getLogger(__name__)
logger_main.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('WEB_ROOT'),'logs','main_routes.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_main.addHandler(file_handler)
logger_main.addHandler(stream_handler)


@main.route("/", methods=["GET","POST"])
def home():
    logger_main.info(f"-- in home page route --")

    return render_template('home.html')


@main.route("/json01", methods=["GET","POST"])
def json01():
    logger_main.info(f"-- in json01--")
    rincon = sess.query(Rincons).filter_by(id= 4).first()
    print(Rincons.metadata.tables)
    print(rincon)
    return jsonify({"item1":"Something cool!", "item2":"somethign necessary"})



@main.route("/image01", methods=["GET","POST"])
def image01():
    logger_main.info(f"-- in image01--")

    # return jsonify({"item1":"Something cool!", "item2":"somethign necessary"})
    # return send_file(filename, mimetype='image/gif')
    dir = "/Users/nick/Documents/_databases/personalWebsite/dossier"
    return send_from_directory(dir, "NickAndMolly2022.jpg")




@main.route("/rincon_posts/<rincon_name>", methods=["GET","POST"])
def rincon_posts(rincon_name):
    logger_main.info(f"-- in rincon_posts --")
    # print("requeste.args", request.args)
    # data_dict = request.get_json()

    # print("request,get_sjons: ", data_dict)
    # rincon_id = request.args.get('rincon_id')
    # rincon_id = data_dict.get('rincon_id')
    rincon_id = 4

    print("SQL_URI: ", current_app.config.get("SQL_URI"))
    print(dir(current_app.config))
    print("---------------------------")
    print(current_app.config.items())

    print("rincond_id: ", rincon_id)
    print(Rincons)
    # rincon = sess.get(Rincons, int(rincon_id))
    rincon = sess.query(Rincons).filter_by(id= 4).first()

    print(rincon)

    rincon_posts = []
    for i in rincon.posts:
        temp_dict = {}

        temp_dict['post_id'] = i.id
        temp_dict['date_for_sorting'] = i.time_stamp_utc
        temp_dict['username'] = sess.get(Users,i.user_id).username

        #search for http in i.text


        # temp_dict['text'] = i.text
        temp_dict['text'] = extract_urls_info(i.text)
        # print(temp_dict['text'])



        print("-- what is image ---")
        print(i.image_file_name)
        temp_dict['image_exists'] = False if i.image_file_name == None else True
        temp_dict['image_name_and_path'] = f"rincon_files/{rincon_id}_{rincon.name_no_spaces}/{i.image_file_name}"
        temp_dict['date'] = i.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        # temp_dict['delete_post_permission'] = False if i.user_id != current_user.id else True
        temp_dict['delete_post_permission'] = False

        comments_list = []
        for comment in i.comments:
            temp_sub_dict = {}
            temp_sub_dict['date'] = comment.time_stamp_utc.strftime("%m/%d/%y %H:%M")
            # temp_sub_dict['username'] = sess.get(Users,comment.user_id).username
            temp_sub_dict['username'] = "Batman"
            temp_sub_dict['text'] = comment.text
            # temp_sub_dict['delete_comment_permission'] = False if comment.user_id != current_user.id else True
            temp_sub_dict['delete_comment_permission'] = False
            temp_sub_dict['comment_id'] = comment.id
            comments_list.append(temp_sub_dict)
        temp_dict['comments'] = comments_list
        rincon_posts.append(temp_dict)

    rincon_posts = sorted(rincon_posts, key=lambda d: d['date_for_sorting'], reverse=True)

    return jsonify(rincon_posts)


@main.route("/rincon_posts_payload/<rincon_name>", methods=["GET","POST"])
def rincon_posts_payload(rincon_name):
    logger_main.info(f"-- in rincon_posts --")
    # print("requeste.args", request.args)
    data_headers = request.headers
    print(data_headers)

    print(dir(request))
    print()
    print(request.content_type)
    print(request.view_args)
    print("reqeust.charset: ", request.charset)
    print("reqeust.args: ", request.args)


    try:
        # data_dict = request.get_json()
        # request.accept_charsets("utf-8")
        data_dict = request.json
        print(data_dict)
    except Exception as e:
        print(e)

    # print("request,get_sjons: ", data_dict)
    # rincon_id = request.args.get('rincon_id')
    rincon_id = data_dict.get('rincon_id')
    # rincon_id = 4

    print("SQL_URI: ", current_app.config.get("SQL_URI"))
    print(dir(current_app.config))
    print("---------------------------")
    print(current_app.config.items())

    print("rincond_id: ", rincon_id)
    print(Rincons)
    rincon = sess.get(Rincons, int(rincon_id))
    # rincon = sess.query(Rincons).filter_by(id= 4).first()

    print(rincon)

    rincon_posts = []
    for i in rincon.posts:
        temp_dict = {}

        temp_dict['post_id'] = i.id
        temp_dict['date_for_sorting'] = i.time_stamp_utc
        temp_dict['username'] = sess.get(Users,i.user_id).username

        #search for http in i.text


        # temp_dict['text'] = i.text
        temp_dict['text'] = extract_urls_info(i.text)
        # print(temp_dict['text'])



        print("-- what is image ---")
        print(i.image_file_name)
        temp_dict['image_exists'] = False if i.image_file_name == None else True
        temp_dict['image_name_and_path'] = f"rincon_files/{rincon_id}_{rincon.name_no_spaces}/{i.image_file_name}"
        temp_dict['date'] = i.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        # temp_dict['delete_post_permission'] = False if i.user_id != current_user.id else True
        temp_dict['delete_post_permission'] = False

        comments_list = []
        for comment in i.comments:
            temp_sub_dict = {}
            temp_sub_dict['date'] = comment.time_stamp_utc.strftime("%m/%d/%y %H:%M")
            # temp_sub_dict['username'] = sess.get(Users,comment.user_id).username
            temp_sub_dict['username'] = "Batman"
            temp_sub_dict['text'] = comment.text
            # temp_sub_dict['delete_comment_permission'] = False if comment.user_id != current_user.id else True
            temp_sub_dict['delete_comment_permission'] = False
            temp_sub_dict['comment_id'] = comment.id
            comments_list.append(temp_sub_dict)
        temp_dict['comments'] = comments_list
        rincon_posts.append(temp_dict)

    rincon_posts = sorted(rincon_posts, key=lambda d: d['date_for_sorting'], reverse=True)

    return jsonify(rincon_posts)






@main.route("/rincon_posts_payload02/<rincon_name>", methods=["GET","POST"])
def rincon_posts_payload02(rincon_name):
    logger_main.info(f"-- in rincon_posts --")
    data_headers = request.headers


    try:
        data_dict = request.json
        # print(data_dict)
    except Exception as e:
        print(e)

    rincon_id = data_dict.get('rincon_id')


    rincon = sess.get(Rincons, int(rincon_id))
    # rincon = sess.query(Rincons).filter_by(id= 4).first()

    # print(rincon)

    rincon_posts = []
    for i in rincon.posts:
        temp_dict = {}

        temp_dict['post_id'] = i.id
        temp_dict['date_for_sorting'] = i.time_stamp_utc
        print("date_for_sorting: ", i.time_stamp_utc)
        temp_dict['username'] = sess.get(Users,i.user_id).username
        


        temp_dict['text'] = extract_urls_info(i.text)

        # print(i.image_file_name)
        temp_dict['image_exists'] = False if i.image_file_name == None else True
        temp_dict['image_name_and_path'] = f"rincon_files/{rincon_id}_{rincon.name_no_spaces}/{i.image_file_name}"
        # temp_dict['date'] = i.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        # temp_dict['delete_post_permission'] = False if i.user_id != current_user.id else True
        temp_dict['delete_post_permission'] = False

        # comments_list = []
        # for comment in i.comments:
        #     temp_sub_dict = {}
        #     temp_sub_dict['date'] = comment.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        #     # temp_sub_dict['username'] = sess.get(Users,comment.user_id).username
        #     temp_sub_dict['username'] = "Batman"
        #     temp_sub_dict['text'] = comment.text
        #     # temp_sub_dict['delete_comment_permission'] = False if comment.user_id != current_user.id else True
        #     temp_sub_dict['delete_comment_permission'] = False
        #     temp_sub_dict['comment_id'] = comment.id
        #     comments_list.append(temp_sub_dict)
        # temp_dict['comments'] = comments_list
        rincon_posts.append(temp_dict)

    rincon_posts = sorted(rincon_posts, key=lambda d: d['date_for_sorting'], reverse=True)

    print("Sending this:::")
    print(rincon_posts)

    return jsonify(rincon_posts)





@main.route("/rincon_posts_payload03/", methods=["GET","POST"])
def rincon_posts_payload03():
    logger_main.info(f"-- in rincon_posts --")
    data_headers = request.headers

    try:
        data_dict = request.json
        # print(data_dict)
    except Exception as e:
        print(e)

    rincon_id = data_dict.get('rincon_id')
    rincon = sess.get(Rincons, int(rincon_id))


    rincon_posts = []
    for i in rincon.posts:
        temp_dict = {}
        temp_dict['post_id'] = i.id
        temp_dict['date'] = i.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        temp_dict['username'] = sess.get(Users,i.user_id).username
        temp_dict['text'] = extract_urls_info(i.text)['text']
        temp_dict['date_for_sorting'] = i.time_stamp_utc
        rincon_posts.append(temp_dict)

    rincon_posts = sorted(rincon_posts, key=lambda d: d['date_for_sorting'], reverse=True)

    print("Sending this:::")
    print(rincon_posts)

    return jsonify(rincon_posts)



@main.route("/rincon_posts_payload04/", methods=["GET","POST"])
def rincon_posts_payload04():
    logger_main.info(f"-- in rincon_posts --")
    data_headers = request.headers

    try:
        data_dict = request.json
        # print(data_dict)
    except Exception as e:
        print(e)

    rincon_id = data_dict.get('rincon_id')
    rincon = sess.get(Rincons, int(rincon_id))


    rincon_posts = []
    for i in rincon.posts:
        temp_dict = {}
        temp_dict['post_id'] = i.id
        temp_dict['date'] = i.time_stamp_utc.strftime("%m/%d/%y %H:%M")
        temp_dict['username'] = sess.get(Users,i.user_id).username
        temp_dict['post_text'] = extract_urls_info(i.text)['text']
        temp_dict['date_for_sorting'] = i.time_stamp_utc
        rincon_posts.append(temp_dict)

    rincon_posts = sorted(rincon_posts, key=lambda d: d['date_for_sorting'], reverse=True)

    print("Sending this:::")
    print(rincon_posts)

    return jsonify(rincon_posts)