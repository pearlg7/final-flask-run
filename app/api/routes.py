from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Run, run_schema, runs_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_run()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/runs', methods = ['POST'])
@token_required
def create_run(current_user_token):
    date = request.json['date']
    distance = request.json['distance']
    pace = request.json['pace']
    heart_rate = request.json['heart_rate']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    run = Run(date, distance, pace, heart_rate, user_token = user_token )

    db.session.add(run)
    db.session.commit()

    response = run_schema.dump(run)
    return jsonify(response)

@api.route('/runs', methods = ['GET'])
@token_required
def get_run(current_user_token):
    a_user = current_user_token.token
    runs = Run.query.filter_by(user_token = a_user).all()
    response = runs_schema.dump(runs)
    return jsonify(response)

@api.route('/runs/<id>', methods = ['GET'])
@token_required
def get_run_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        run = Run.query.get(id)
        response = run_schema.dump(run)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/runs/<id>', methods = ['POST','PUT'])
@token_required
def update_run(current_user_token,id):
    run = Run.query.get(id) 
    run.date = request.json['date']
    run.distance = request.json['distance']
    run.pace = request.json['pace']
    run.heart_rate = request.json['heart_rate']
    run.user_token = current_user_token.token

    db.session.commit()
    response = run_schema.dump(run)
    return jsonify(response)

@api.route('/runs/<id>', methods = ['DELETE'])
@token_required
def delete_run(current_user_token, id):
    run = Run.query.get(id)
    db.session.delete(run)
    db.session.commit()
    response = run_schema.dump(run)
    return jsonify(response)