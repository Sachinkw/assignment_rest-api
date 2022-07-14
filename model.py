from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    country = db.Column(db.String(100))
    active = db.Column(db.Integer, default=1)

    # To add an user instance to db and commit changes
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        f_data = {}
        for att in [x for x in dir(self) if not x.startswith('_') and x != 'metadata']:

            # Follwing dunder returns all the attributes and function metadata
            data = self.__getattribute__(att)
            try:
                # if data variable has data value it will get converted to json, and we will store it in dict
                # else ignore in the except block
                json.dumps(data) 
                f_data[att] = data
            except:
                continue
        # a json-encodable dict
        return f_data

    @classmethod
    def fetch_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def update_details(cls, data):
        try:
            row = cls.query.filter_by(email=data["email"]).update(dict(data))
            db.session.commit()
            return True
        except:
            return False


    @classmethod
    def delete_user(cls, user_id):
        try:
            cls.query.filter_by(id=user_id).update({"active":0})
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

