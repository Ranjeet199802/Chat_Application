import datetime

from flask import Flask, request, jsonify, json
from sqlalchemy.exc import IntegrityError

from models import db, Users, Room, app, room_member


@app.route('/create_room', methods=['POST'])
def add_users():
    try:
        if request.method == 'POST':
            name = request.json['name']
            email = request.json['email']
            phone_no = request.json['phone_no']
            city = request.json['city']
            r_name = request.json['r_name']
            r_description = request.json['r_description']
            found = Users.query.filter_by(email=email).first()
            if found:
                user_id = found.id
            else:
                new_user = Users(name=name, email=email, phone_no=phone_no, city=city)
                db.session.add(new_user)
                db.session.commit()
                user_id = new_user.id

            exists = Room.query.filter_by(r_name=r_name).first()
            if exists:
                return jsonify(
                    {
                        "STATUS": 406,
                        "MESSAGE": "ROOM NAME ALREADY TAKEN, PLEASE CHANGE ROOM NAME"
                    }
                )
            else:
                room = Room(r_name=r_name, created_by=user_id, date_time=str(datetime.datetime.now()),
                            r_description=r_description)
                db.session.add(room)
                db.session.commit()
                return jsonify({'message': 'successfully created user', 'Room_id': room.id, 'Status_code': 200})

    except Exception as e:
        return 'found error,somthing went wrong'


@app.route('/get_room', methods=['GET'])
def getroom():
    if request.method == 'GET':

        try:
            data = request.args.get('r_id')

            if data:
                exists = Room.query.filter_by(id=data).first()
                if exists:
                    return jsonify(
                        {
                            'Room_id': exists.id,
                            'Room_name': exists.r_name,
                            'Date': exists.date_time,
                            'Created_by': exists.created_by,
                            'r_Discription': exists.r_description
                        }
                    )
                else:
                    return jsonify(
                        {
                            'MESSAGE': "NO ROOM AVAILABLE WITH THIS ID"
                        }
                    )

            else:

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

        except Exception as e:
            return 'Something went wrong'


@app.route('/create_user', methods=['POST'])
def createuser():
    if request.method == 'POST':
        aid = request.json['Aid']
        rid = request.json['Rid']
        name = request.json['name']
        email = request.json['email']
        phone_no = request.json['phone_no']
        city = request.json['city']

        exist = Room.query.filter_by(id=rid).first()

        if exist:

            admin = exist.created_by

            if admin == aid:

                check = Users.query.filter_by(email=email).first()

                if check:

                    userid = check.id

                else:

                    add = Users(name=name, email=email, phone_no=phone_no, city=city)
                    db.session.add(add)
                    db.session.commit()
                    userid = add.id

                new = room_member(uid=userid, Rid=rid)
                db.session.add(new)
                db.session.commit()

                return jsonify(
                    {
                        "Message": "user added",
                        "user_id": new.id,
                        "room_ id": rid
                    }
                )

            else:
                return jsonify(
                    {
                        "message": "unauthorised access"
                    }
                )
        else:
            return jsonify(
                {
                    "message": "no room available with this id"
                }
            )


if __name__ == '__main__':
    app.run(debug=True)
