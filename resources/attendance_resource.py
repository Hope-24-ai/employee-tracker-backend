from flask_restful import Resource
from flask import request
from models import db, AttendanceRecord

class AttendanceListResource(Resource):
    def get(self):
        attendance_records = AttendanceRecord.query.all()
        return [
            {
                "id": a.id,
                "employeeId": a.employeeId,
                "date": a.date,
                "status": a.status
            }
            for a in attendance_records
        ], 200

    def post(self):
        data = request.get_json()
        attendance = AttendanceRecord(
            employeeId=data["employeeId"],
            date=data["date"],
            status=data["status"]
        )
        db.session.add(attendance)
        db.session.commit()
        return {"message": "Attendance record added"}, 201

class AttendanceResource(Resource):
    def get(self, attendance_id):
        attendance = AttendanceRecord.query.get_or_404(attendance_id)
        return {
            "id": attendance.id,
            "employeeId": attendance.employeeId,
            "date": attendance.date,
            "status": attendance.status
        }, 200

    def put(self, attendance_id):
        attendance = AttendanceRecord.query.get_or_404(attendance_id)
        data = request.get_json()
        attendance.date = data.get("date", attendance.date)
        attendance.status = data.get("status", attendance.status)
        db.session.commit()
        return {"message": "Attendance record updated"}, 200

    def delete(self, attendance_id):
        attendance = AttendanceRecord.query.get_or_404(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        return {"message": "Attendance record deleted"}, 200
