from flask import Blueprint, json

from app.models import Suite, SuiteSchema

# Define the blueprint: 'suites', set its url prefix: app.url/suites
suites = Blueprint('suites', __name__, url_prefix='/suites')


@suites.route('/')
def get_all_suites():
    suites = Suite.query.all()
    suites_schema = SuiteSchema(many=True)
    return json.dumps(suites_schema.dump(suites))


@suites.route('/<int:id>')
def get_suite(id):
    suite = Suite.query.get(id)
    suite_schema = SuiteSchema()
    return suite_schema.dump(suite)