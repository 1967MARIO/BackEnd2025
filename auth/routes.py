from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from ..extensions import db, limiter
from ..models import User
from ..schemas import RegisterSchema, LoginSchema, UserSchema


bp = Blueprint('auth', __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


@bp.post('/register')
@limiter.limit('10 per hour')
def register():
    data = request.get_json() or {}
    errors = register_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(error='Email already registered'), 409

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201


@bp.post('/login')
@limiter.limit('5 per minute')
def login():
    data = request.get_json() or {}
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify(error='Invalid credentials'), 401

    claims = {'role': user.role}
    access = create_access_token(identity=user.id, additional_claims=claims)
    refresh = create_refresh_token(identity=user.id, additional_claims=claims)
    return jsonify(access_token=access, refresh_token=refresh)


@bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    claims = {'role': user.role if user else 'user'}
    access = create_access_token(identity=user_id, additional_claims=claims)
    return jsonify(access_token=access)


@bp.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)