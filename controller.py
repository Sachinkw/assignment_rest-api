from msilib.schema import File
import profile
from model import User
import os
from flask import jsonify, make_response
from datetime import datetime


def post_user(data):
    '''
    Get the data from the request body and store it in the user model
    '''
    try:
        #create an instance of User model and then save it to database
        new_user = User(**data)
        new_user.save_user()
        response = make_response(jsonify({
            "message" : "User successfully registered",
            "data" : {
                "user_id" : new_user.id,
                "name" : new_user.name,
                "email" : new_user.email,
                "mob_num" : new_user.mobile_number
            }
        }
        ),201)
        return response
    except Exception as e:
        print(e)
        response = make_response(jsonify({
            "message" : "User registration Failed",
            "error" : str(e)
        })
        ,401)
        return response


def get_data(email_id):
    '''
    Get the email_id and return the entire user data
    '''
    try:
        user_data = User.fetch_user_by_email(email_id)

        # Check if the user_data exist and user is in active state
        if user_data and user_data.active:
            user_dict = user_data.to_json()
            response = make_response(jsonify({
                "message":"data Fetched Successfully",
                "data":user_dict
            } ), 202)
            return response

        else:
            return make_response(jsonify({"message":"User doesn't exist"}), 401)

    except Exception as e:
        print(e)
        return make_response(jsonify({
            "message":"Failed to fetch the data"
        }),402)



def update_data(data):
    user = User.fetch_user_by_email(data["email"])
    if user:
        temp = User.update_details(data)
        if temp:
            return make_response(jsonify({"message":"Details updated successfull"}), 201)
        else:
            return make_response(jsonify({"message":"Failed to update the data"}), 401)
    else:
        return make_response(jsonify({"message":"User doesn't exist"}), 402)



def delete_data(args):
    '''
    Take the user id as query parameter in the request and update the active column as 0 in the db
    '''
    u_id = args["user_id"]
    user = User.fetch_user_by_id(u_id)
    # Check if user exist in active state or not
    if user.active:
        res = User.delete_user(args["user_id"])

        if res:
            return make_response(jsonify({"message":"User deleted successfully"}), 201)
        else:
            return make_response(jsonify({"message":"Failed to delete the user"}), 401)

    else:
        return make_response(jsonify({"message":"User doesn't exist"}), 402)



def upload_profile_pic(data, args):
    user = User.fetch_user_by_id(args["user_id"])
    if user and user.active:
        try:
        # create a unique path for pic to store in file system
            prof_pic_url = "/static/images/profiles/" + str(user.id) + str(datetime.now()) + ".png"
            # get the current working directory
            curr_dir = os.path.abspath(os.getcwd())
            complete_pic_url = os.path.join(curr_dir, prof_pic_url)

            pic = data["photo"]
            pic.save(os.path.join(complete_pic_url))

            photo_data = {"profile_pic_url" : complete_pic_url}
            User.update_details(photo_data)

            return make_response(jsonify({"message":"Profile photo updated successfully"}), 201)
        
        except Exception as e:
            # print(e)
            return make_response(jsonify({"message":f"Profile photo updated Failed with error {e}"}), 201)

    else:
        return make_response(jsonify({"message":"User is not in active state"}), 401)
        


