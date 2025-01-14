from flask import Flask, request, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from tasks import send_email, send_sms

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    new_user = User(email=data['email'], phone=data['phone'],
                    notify_via_email=data.get('notify_via_email', True),
                    notify_via_sms=data.get('notify_via_sms', False))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successrender_templatefully!'}), 201

@app.route('/list', methods=['GET', 'POST'])
def list_users():

    return render_template('list_users.html', items=User.query.all())


@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user:
        if user.notify_via_email:
            send_email.delay(data['subject'], data['message'], user.email)

        if user.notify_via_sms:
            send_sms.delay(data['message'], user.phone)

        return jsonify({'message': 'Notification queued.'}), 200
    else:
        return jsonify({'message': 'User not found.'}), 404

# @app.route('/send_message', methods=['POST'])
# def send_messagesms():
#     data = request.json
#     user = User.query.filter_by(email=data['email']).first()

#     if user:('notify_via_sms', False)
#         return jsonify({'message': 'User not found.'}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_user', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # conn = get_db_connection()
        # conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        # conn.commit()
        # conn.close()


        new_user = User(email=title, phone=content, notify_via_email=True, notify_via_sms=False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_user.html')

@app.route('/new_sendMail', methods=['GET', 'POST'])
def new_sendMail():
    if request.method == 'POST':
        title = request.form['title']
        subject = request.form['subject']
        content = request.form['content']

        # conn = get_db_connection()
        # conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        # conn.commit()
        # conn.close()

        send_email.delay(subject, content, title)

        return redirect(url_for('index'))

    return render_template('send_mail.html')


if __name__ == '__main__':
    app.run(debug=True)

