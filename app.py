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
            check = Users.query.filter_by(email=email).first()
            if check:
                return "Email already taken, please try another one"
            else:
                phone_no = request.json['phone_no']
                found = Users.query.filter_by(phone_no=phone_no).first()
                if found:
                    return "Phone_no already exixts"
                else:
                    city = request.json['city']

            new_user = Users(name=name, email=email, phone_no=phone_no, city=city)
            db.session.add(new_user)
            db.session.commit()

            room = Room(r_name='groupc')
            exists = Room.query.filter_by(r_name=room.r_name).first()
            if exists:
                return "Room with same name alredy exists, please change room name"
            else:
                room.created_by = new_user.id
                room.date_time = str(datetime.datetime.now())

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
