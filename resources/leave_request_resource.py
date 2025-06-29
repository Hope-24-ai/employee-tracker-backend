from flask_restful import Resource, reqparse
from flask import request
from models import db, LeaveRequest 
from datetime import date 

leave_parser = reqparse.RequestParser()
leave_parser.add_argument('employee_id', type=int, required=True, help='Employee ID is required', location='json')
leave_parser.add_argument('leave_type', type=str, required=True, help='Leave type is required', location='json')
leave_parser.add_argument('start_date', type=str, required=True, help='Start date is required (YYYY-MM-DD)', location='json')
leave_parser.add_argument('end_date', type=str, required=True, help='End date is required (YYYY-MM-DD)', location='json')
leave_parser.add_argument('status', type=str, location='json')  # HR sets this

class LeaveRequestListResource(Resource):
    def get(self):
        """✅ HR Only: Get all leave requests"""
        role = request.headers.get('Role', '').strip().lower()
        if role != 'human resource manager':
            return {'message': 'Access denied: HR Manager role required'}, 403

        leave_requests = LeaveRequest.query.all()
        return [req.to_dict() for req in leave_requests], 200

    def post(self):
        """✅ Any Employee: Create a new leave request"""
        args = leave_parser.parse_args()

        try:
            start_date_obj = date.fromisoformat(args['start_date'])
            end_date_obj = date.fromisoformat(args['end_date'])
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        new_request = LeaveRequest(
            employee_id=args['employee_id'],
            leave_type=args['leave_type'],
            start_date=start_date_obj,
            end_date=end_date_obj,
            status=args.get('status', 'Pending')
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request.to_dict(), 201

class LeaveRequestResource(Resource):
    def get(self, leave_id):
        """✅ HR Only: View a single leave request"""
        role = request.headers.get('Role', '').strip().lower()
        if role != 'human resource manager':
            return {'message': 'Access denied: HR Manager role required'}, 403

        request_obj = LeaveRequest.query.get(leave_id)
        if request_obj:
            return request_obj.to_dict(), 200
        return {'message': 'Leave request not found'}, 404

    def put(self, leave_id):
        """✅ HR Only: Update leave request (e.g., approve/reject)"""
        role = request.headers.get('Role', '').strip().lower()
        if role != 'human resource manager':
            return {'message': 'Access denied: HR Manager role required'}, 403

        args = leave_parser.parse_args()
        request_obj = LeaveRequest.query.get(leave_id)
        if not request_obj:
            return {'message': 'Leave request not found'}, 404

        try:
            request_obj.start_date = date.fromisoformat(args['start_date'])
            request_obj.end_date = date.fromisoformat(args['end_date'])
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        request_obj.employee_id = args['employee_id']
        request_obj.leave_type = args['leave_type']
        request_obj.status = args['status'] or request_obj.status

        db.session.commit()
        return request_obj.to_dict(), 200

    def delete(self, leave_id):
        """✅ HR Only: Delete a leave request"""
        role = request.headers.get('Role', '').strip().lower()
        if role != 'human resource manager':
            return {'message': 'Access denied: HR Manager role required'}, 403

        request_obj = LeaveRequest.query.get(leave_id)
        if not request_obj:
            return {'message': 'Leave request not found'}, 404

        db.session.delete(request_obj)
        db.session.commit()
        return {'message': 'Leave request deleted'}, 204
