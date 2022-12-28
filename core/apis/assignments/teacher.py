from flask import Blueprint
from core.models.assignments import Assignment
from core.apis.responses import APIResponse
from core.apis import decorators
from core.models.assignments import GradeEnum
from core import db
from .schema import AssignmentSchema, AssignmentSubmitSchema

teacher_assignments_resources = Blueprint("teacher_assignments_resources", __name__)


@teacher_assignments_resources.route("/assignments", methods=['GET'], strict_slashes = False)
@decorators.auth_principal
def list_assignments_by_teacher(p):
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many = True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route("/assignments/grade",methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def update_grade(p, incoming_payload):
    print(incoming_payload['id'])
    updated_assignment = Assignment.update(incoming_payload['id'],incoming_payload['grade'],principal=p)
    db.session.commit()
    updated_assignment_dump = AssignmentSchema().dump(updated_assignment)
    return APIResponse.respond(data=updated_assignment_dump)