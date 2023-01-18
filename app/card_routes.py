from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from datetime import datetime
from app.board_routes import validate_model


bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# Create a card [POST]
@bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    if not request_body["user_id"]:
        abort(make_response({"message": "No user ID present"}, 400))

    if not request_body["message"]:
        abort(make_response({"message": "No message in card"}, 400))

    date = str(datetime.utcnow())

    new_card = Card.from_dict({'date_created': date, 
                                'likes': 0 ,
                                'message':request_body["message"],
                                'board_id': request_body["board_id"],
                                'author_id':request_body['user_id']})
    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(new_card.to_dict()), 201)

# Get information on a card by ID [GET] 200 will come automatically
@bp.route("/<id>", methods=["GET"])
def read_card(id):
    card = validate_model(Card, id)
    return card.to_dict()
    


# Get information on all cards associated with a board [GET]

# Update information on a card [PATCH]

# Delete card from database / board [DELETE]