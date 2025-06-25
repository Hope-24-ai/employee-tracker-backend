# resources/leave_request_resource.py
from flask_restful import Resource
from models import db, LeaveRequest
from flask import request

class LeaveRequestListResource(Resource):
    def get(self):
        leaves = LeaveRequest.query.all()
        return [
            {
                "id": l.id,
                "employeeId": l.employeeId,
                "type": l.type,
                "startDate": l.startDate,
                "endDate": l.endDate,
                "reason": l.reason,
                "status": l.status
            }
            for l in leaves
        ], 200

    def post(self):
        data = request.get_json()
        leave = LeaveRequest(
            employeeId=data["employeeId"],
            type=data["type"],
            startDate=data["startDate"],
            endDate=data["endDate"],
            reason=data.get("reason", ""),
            status=data.get("status", "Pending")
        )
        db.session.add(leave)
        db.session.commit()
        return {"message": "Leave request created"}, 201

class LeaveRequestResource(Resource):
    def get(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        return {
            "id": leave.id,
            "employeeId": leave.employeeId,
            "type": leave.type,
            "startDate": leave.startDate,
            "endDate": leave.endDate,
            "reason": leave.reason,
            "status": leave.status
        }, 200

    def put(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        data = request.get_json()
        leave.type = data.get("type", leave.type)
        leave.startDate = data.get("startDate", leave.startDate)
        leave.endDate = data.get("endDate", leave.endDate)
        leave.reason = data.get("reason", leave.reason)
        leave.status = data.get("status", leave.status)
        db.session.commit()
        return {"message": "Leave request updated"}, 200

    def delete(self, leave_id):
        leave = LeaveRequest.query.get_or_404(leave_id)
        db.session.delete(leave)
        db.session.commit()
        return {"message": "Leave request deleted"}, 200
