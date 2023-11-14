
from flask import render_template, Blueprint, render_template

error_blueprint = Blueprint('error_blueprint', __name__, template_folder="templates")

@error_blueprint.app_errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400

@error_blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@error_blueprint.app_errorhandler(405)
def method_not_allowded(error):
    return render_template('405.html'), 405

@error_blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@error_blueprint.app_errorhandler(503)
def server_down(error):
    return render_template('503.html'), 503
