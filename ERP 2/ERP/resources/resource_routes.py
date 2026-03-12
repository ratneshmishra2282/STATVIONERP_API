from resources.auth_resource import LoginResource
from resources.organization_resource import OrganizationRegisterResource
from resources.student_resource import StudentListResource, StudentDetailResource
from resources.fee_resource import FeeResource


def register_resources(api):

    # Auth
    api.add_resource(LoginResource, "/api/login")

    # Organization
    api.add_resource(OrganizationRegisterResource, "/api/organizations")

    # Students
    api.add_resource(StudentListResource, "/api/students")
    api.add_resource(StudentDetailResource, "/api/students/<int:student_id>")

    # Fees
    api.add_resource(FeeResource, "/api/fees")