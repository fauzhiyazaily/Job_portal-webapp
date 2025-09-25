from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Job, Application, Category
from app.forms import LoginForm, RegistrationForm, JobForm, ApplicationForm

# Create blueprint
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    return render_template('index.html', jobs=jobs, categories=categories)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Log the user in
            login_user(user, remember=form.remember_me.data)

            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', form=form)

        # Check if username already exists
        existing_username = User.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already taken. Please choose a different username.', 'danger')
            return render_template('register.html', form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)

        # Add to database
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'employer':
        # Show employer's posted jobs
        jobs = Job.query.filter_by(employer_id=current_user.id).all()
        return render_template('dashboard.html', jobs=jobs, user_type='employer')
    else:
        # Show job seeker's applications
        applications = Application.query.filter_by(job_seeker_id=current_user.id).all()
        return render_template('dashboard.html', applications=applications, user_type='job_seeker')


@bp.route('/jobs')
def jobs():
    # Get all active jobs (simple list without pagination for now)
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)


@bp.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    form = ApplicationForm()
    return render_template('job_detail.html', job=job, form=form)


@bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.user_type != 'job_seeker':
        flash('Only job seekers can apply for jobs.', 'warning')
        return redirect(url_for('main.job_detail', job_id=job_id))

    job = Job.query.get_or_404(job_id)
    form = ApplicationForm()

    if form.validate_on_submit():
        # Check if already applied
        existing_application = Application.query.filter_by(
            job_seeker_id=current_user.id, job_id=job_id
        ).first()

        if existing_application:
            flash('You have already applied for this job.', 'warning')
        else:
            application = Application(
                cover_letter=form.cover_letter.data,
                job_seeker_id=current_user.id,
                job_id=job_id
            )
            db.session.add(application)
            db.session.commit()
            flash('Your application has been submitted successfully!', 'success')

    return redirect(url_for('main.job_detail', job_id=job_id))


@bp.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.user_type != 'employer':
        flash('Only employers can post jobs.', 'warning')
        return redirect(url_for('main.dashboard'))

    form = JobForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            description=form.description.data,
            requirements=form.requirements.data,
            location=form.location.data,
            salary=form.salary.data,
            job_type=form.job_type.data,
            category_id=form.category_id.data,
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Your job has been posted successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('post_job.html', form=form)

from flask import jsonify, request
from app.models import Job, User


# API Routes
@bp.route('/api/jobs', methods=['GET'])
def api_get_jobs():
    jobs = Job.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'company': job.employer.username,
        'location': job.location,
        'salary': job.salary,
        'type': job.job_type
    } for job in jobs])


@bp.route('/api/jobs/<int:job_id>', methods=['GET'])
def api_get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'requirements': job.requirements,
        'location': job.location,
        'salary': job.salary,
        'type': job.job_type,
        'company': job.employer.username
    })


@bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()

    # Validation
    if not data or not all(k in data for k in ['username', 'email', 'password', 'user_type']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        user_type=data['user_type']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201