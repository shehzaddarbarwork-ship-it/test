"""Main view routes for the CRM application."""

from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page route."""
    return render_template('home.html')


@main_bp.route('/login')
def login():
    """Login page route."""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    return render_template('login.html')


@main_bp.route('/signup')
def signup():
    """Signup page route."""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    return render_template('signup.html')


@main_bp.route('/logout')
def logout():
    """Logout route."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))


@main_bp.route('/send-mail')
def send_mail():
    """Send mail page route."""
    return render_template('send_mail.html')


@main_bp.route('/learn-python')
def learn_python():
    """Learn Python page route."""
    return render_template('learn_python.html')


@main_bp.route('/see-interaction')
def see_interaction():
    """See interactions page route."""
    return render_template('see_interaction.html')