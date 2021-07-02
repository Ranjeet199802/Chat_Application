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


@app.route('/add_members', methods=['POST'])
def add_members():
    try:
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
                            "room_ id": rid,
                            "usertable_id": new.uid
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

    except Exception as e:
        return jsonify(
            {
                "Message": "something went wrong"
            }
        )


@app.route('/update', methods=['PUT'])
def update():
    try:
        if request.method == 'PUT':

            roomid = request.json['roomid']
            created_by = request.json['created_by']

            name = request.json['room_name']
            discription = request.json['discription']
            removeid = request.json['remove_id']

            match = Room.query.filter_by(id=roomid).first()

            if match:
                if match.created_by == created_by:
                    if name == "" and discription == "" and removeid == "":
                        return jsonify(
                            {

                                "message": "please input data"
                            }
                        )

                    elif name and discription and removeid:
                        match.r_name = name
                        match.r_description = discription
                        db.session.commit()

                        req_data = room_member.query.filter_by(Rid=roomid, uid=removeid).first()
                        if req_data:
                            Users.query.filter_by(id=removeid).delete()
                            db.session.delete(req_data)
                            db.session.commit()
                        else:
                            return "data not found in room to delet user"


                    elif name and discription == "" and removeid == "":
                        match.r_name = name
                        db.session.commit()

                    elif name == "" and discription and removeid == "":
                        match.r_description = discription
                        db.session.commit()

                    elif name == "" and discription == "" and removeid:
                        req_data = room_member.query.filter_by(Rid=roomid, uid=removeid).first()
                        if req_data:
                            Users.query.filter_by(id=removeid).delete()
                            db.session.delete(req_data)
                            db.session.commit()
                        else:
                            return "data not found in room to delet user"

                    elif name and discription and removeid == "":
                        match.r_name = name
                        match.r_description = discription
                        db.session.commit()

                    elif name and discription == "" and removeid:
                        match.r_name = name
                        db.session.commit()
                        req_data = room_member.query.filter_by(Rid=roomid, uid=removeid).first()
                        if req_data:
                            Users.query.filter_by(id=removeid).delete()
                            db.session.delete(req_data)
                            db.session.commit()
                        else:
                            return "data not found in room to delet user"

                    elif name == "" and discription and removeid:
                        match.r_description = discription
                        db.session.commit()
                        req_data = room_member.query.filter_by(Rid=roomid, uid=removeid).first()
                        if req_data:
                            Users.query.filter_by(id=removeid).delete()
                            db.session.delete(req_data)
                            db.session.commit()
                        else:
                            return "data not found in room to delet user"

                    return jsonify(
                        {
                            "MESSAGE": "DATA IS SUCCEFULLY UPDATED"
                        }
                    )
                else:
                    return " admin not match to the Room id"

            else:
                return "no room found with this id"

    except Exception as e:
        return "something went wrong"


if __name__ == '__main__':
    app.run(debug=True)
