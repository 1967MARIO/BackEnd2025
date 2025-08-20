from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import asc, desc
from ..extensions import db, cache, limiter
from ..models import Item, User
from ..schemas import ItemSchema
from ..utils.security import roles_required


bp = Blueprint('api', __name__)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@bp.get('/items')
@jwt_required()
@limiter.limit('60 per minute')
@cache.cached(timeout=20, query_string=True)
def list_items():
    # Admin ve todo; user ve solo sus items
    claims = get_jwt()
    role = claims.get('role', 'user')
    user_id = get_jwt_identity()

    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 10)), 1), 100)
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = Item.query
    if role != 'admin':
        query = query.filter_by(owner_id=user_id)

    if sort not in {'id', 'name'}:
        sort = 'id'
    ordering = asc(sort) if order == 'asc' else desc(sort)
    query = query.order_by(ordering)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(
        items=items_schema.dump(pagination.items),
        page=page,
        per_page=per_page,
        total=pagination.total
    )


@bp.post('/items')
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    errors = item_schema.validate(data)
    if errors:
        return jsonify(errors=errors), 400
    item = Item(name=data['name'], description=data.get('description', ''), owner_id=user_id)
    db.session.add(item)
    db.session.commit()
    # invalidar cache de listados
    cache.delete_memoized(list_items)
    return item_schema.jsonify(item), 201


@bp.get('/items/<int:item_id>')
@jwt_required()
def get_item(item_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role', 'user')
    item = Item.query.get_or_404(item_id)
    if role != 'admin' and item.owner_id != user_id:
        return jsonify(error='Forbidden'), 403
    return item_schema.jsonify(item)


@bp.put('/items/<int:item_id>')
@jwt_required()
def update_item(item_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role', 'user')
    item = Item.query.get_or_404(item_id)
    if role != 'admin' and item.owner_id != user_id:
        return jsonify(error='Forbidden'), 403

    data = request.get_json() or {}
    errors = item_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors=errors), 400
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    cache.delete_memoized(list_items)
    return item_schema.jsonify(item)


@bp.delete('/items/<int:item_id>')
@jwt_required()
@roles_required('admin', 'user')
def delete_item(item_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role', 'user')
    item = Item.query.get_or_404(item_id)
    if role != 'admin' and item.owner_id != user_id:
        return jsonify(error='Forbidden'), 403
    db.session.delete(item)
    db.session.commit()
    cache.delete_memoized(list_items)
    return '', 204