from flask_restful import Resource


class HealthResource(Resource):

    def get(self):
        return {
            "status": "healthy",
            "service": "erp-backend"
        }, 200