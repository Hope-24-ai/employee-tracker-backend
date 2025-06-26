

from flask_restful import Resource, reqparse
from models import db, AttendanceRecord 
from datetime import date 


attendance_parser = reqparse.RequestParser()
attendance_parser.add_argument('employee_id', type=int, required=True, help='Employee ID is required', location='json')
attendance_parser.add_argument('date', type=str, required=True, help='Date is required (YYYY-MM-DD)', location='json')
attendance_parser.add_argument('status', type=str, required=True, help='Status is required', location='json')
attendance_parser.add_argument('check_in_time', type=str, location='json')
attendance_parser.add_argument('check_out_time', type=str, location='json')


class AttendanceListResource(Resource):
    def get(self):
        """Get all attendance records"""
        attendance_records = AttendanceRecord.query.all()
        return [record.to_dict() for record in attendance_records], 200

    def post(self):
        """Create a new attendance record"""
        args = attendance_parser.parse_args()

        try:
            record_date = date.fromisoformat(args['date']) 
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        new_record = AttendanceRecord(
            employee_id=args['employee_id'],
            date=record_date,
            status=args['status'],
            check_in_time=args['check_in_time'],
            check_out_time=args['check_out_time']
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record.to_dict(), 201

class AttendanceResource(Resource):
    def get(self, attendance_id):
        """Get a single attendance record by its ID"""
        record = AttendanceRecord.query.get(attendance_id)
        if record:
            return record.to_dict(), 200
        return {'message': 'Attendance record not found'}, 404

    def put(self, attendance_id):
        """Update an existing attendance record by its ID"""
        args = attendance_parser.parse_args()
        record = AttendanceRecord.query.get(attendance_id)
        if not record:
            return {'message': 'Attendance record not found'}, 404

        try:
            record.date = date.fromisoformat(args['date'])
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        record.employee_id = args['employee_id']
        record.status = args['status']
        record.check_in_time = args['check_in_time']
        record.check_out_time = args['check_out_time']

        db.session.commit()
        return record.to_dict(), 200

    def delete(self, attendance_id):
        """Delete an attendance record by its ID"""
        record = AttendanceRecord.query.get(attendance_id)
        if not record:
            return {'message': 'Attendance record not found'}, 404

        db.session.delete(record)
        db.session.commit()
        return {'message': 'Attendance record deleted'}, 204