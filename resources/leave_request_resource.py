

from flask_restful import Resource, reqparse
from models import db, LeaveRequest 
from datetime import date 

leave_parser = reqparse.RequestParser()
leave_parser.add_argument('employee_id', type=int, required=True, help='Employee ID is required', location='json')
leave_parser.add_argument('leave_type', type=str, required=True, help='Leave type is required', location='json')
leave_parser.add_argument('start_date', type=str, required=True, help='Start date is required (YYYY-MM-DD)', location='json')
leave_parser.add_argument('end_date', type=str, required=True, help='End date is required (YYYY-MM-DD)', location='json')
leave_parser.add_argument('status', type=str, location='json')

class LeaveRequestListResource(Resource):
    def get(self):
        """Get all leave requests"""
        leave_requests = LeaveRequest.query.all()
        return [req.to_dict() for req in leave_requests], 200

    def post(self):
        """Create a new leave request"""
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
            status=args['status']
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request.to_dict(), 201

class LeaveRequestResource(Resource):
    def get(self, leave_id):
        """Get a single leave request by its ID"""
        request = LeaveRequest.query.get(leave_id)
        if request:
            return request.to_dict(), 200
        return {'message': 'Leave request not found'}, 404

    def put(self, leave_id):
        """Update an existing leave request by its ID"""
        args = leave_parser.parse_args()
        request = LeaveRequest.query.get(leave_id)
        if not request:
            return {'message': 'Leave request not found'}, 404

        try:
            request.start_date = date.fromisoformat(args['start_date'])
            request.end_date = date.fromisoformat(args['end_date'])
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        request.employee_id = args['employee_id']
        request.leave_type = args['leave_type']
        request.status = args['status']

        db.session.commit()
        return request.to_dict(), 200

    def delete(self, leave_id):
        """Delete a leave request by its ID"""
        request = LeaveRequest.query.get(leave_id)
        if not request:
            return {'message': 'Leave request not found'}, 404

        db.session.delete(request)
        db.session.commit()
        return {'message': 'Leave request deleted'}, 204