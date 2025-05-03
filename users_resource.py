from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .users import User
from flask import jsonify
from werkzeug.security import generate_password_hash

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    if type(news_id) == int:
        news = session.query(User).get(news_id)
    if not news:
        abort(404, message=f"User {news_id} not found")


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            email=args['email'],
            hashed_password=generate_password_hash(args['hashed_password'])
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})


class UsersResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        user = session.query(User).get(news_id)

        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        users = session.query(User).get(news_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})
