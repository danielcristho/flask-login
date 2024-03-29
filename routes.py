from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required, logout_user

#Blueprint configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder = 'templates',
    static_folder = 'static'
)

@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.jinja',
        title = 'Flask-Login',
        template = 'dashboard-template',
        current_user = current_user,
        body = "You are now logged in"
    )

@main_bp.route("/logout")
@login_required
def logaout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


