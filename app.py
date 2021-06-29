import datetime

from flask import Flask, request, jsonify, json
from sqlalchemy.exc import IntegrityError

from models import db, Users, Room, app


@app.route('/user', methods=['POST', 'GET'])
def add_users():
    try:
        if request.method == 'POST':
            name = request.json['name']
            email = request.json['email']
            phone_no = request.json['phone_no']
            city = request.json['city']
            found = Users.query.filter_by(email=email).first()
            found1 = Users.query.filter_by(phone_no=phone_no).first()
            if found or found1:
                return jsonify(
                    {
                        "status": 400,
                        "MESSAGE": "USER ALREADY EXISTS"
                    }
                )
            else:

                new_user = Users(name=name, email=email, phone_no=phone_no, city=city)
                db.session.add(new_user)
                db.session.commit()

            r_name = request.json['r_name']
            room = Room(r_name=r_name)
            room.created_by = new_user.id
            room.date_time = str(datetime.datetime.now())
            exists = Room.query.filter_by(r_name=r_name).first()
            if exists:
                return jsonify(
                    {
                        "STATUS": 406,
                        "MESSAGE": "ROOM NAME ALREADY TAKEN, PLEASE CHANGE ROOM NAME"
                    }
                )
            else:
                db.session.add(room)
                db.session.commit()
                return jsonify({'message': 'successfully created user', 'Room_id': room.id, 'Status_code': 200})

    except Exception as e:
        return 'found error,somthing went wrong'

    if request.method == 'GET':

        try:
            data = request.args.get('r_id')
            if not data:
                r_list = []
                table = Room.query.all()
                for rinfo in table:
                    r_list.append(
                        {
                            'Room_id': rinfo.id,
                            'Room_name': rinfo.r_name,
                            'Date': rinfo.date_time,
                            'Created_by': rinfo.created_by,
                            'R_disciption': rinfo.r_description

                        }
                    )
                return jsonify(r_list)

            exists = Room.query.filter_by(id=data).first()
            if exists:
                return jsonify(
                    {
                        'Room_id': exists.id,
                        'Room_na': exists.r_name
                    }
                )
            if not exists:
                return "no room exits with this id"

        except Exception as e:
            return 'Something went wrong'


if __name__ == '__main__':
    app.run(debug=True)
