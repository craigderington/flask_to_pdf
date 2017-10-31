from flask import Flask, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from pdfs import create_pdf
from datetime import datetime
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    MAIL_DEFAULT_SENDER='Defalt Sender <some_user@gmail.com>'
))
mail = Mail(app)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    today = datetime.now().strftime('%c')
    return render_template(
        'index.html',
        foo=today,
    )


@app.route('/invoice/<int:invoice_id>', methods=['GET'])
def view_invoice(invoice_id):
    invoice_id = invoice_id
    subject = "Bellcurve Report PDF"
    receiver = "craig@craigderington.me"
    msg = Message(subject=subject, recipients=[receiver])
    msg.body = "This email contains a PDF."
    pdf = create_pdf(render_template('invoice.html', invoice_id=invoice_id))
    msg.attach("invoice.pdf", "application/pdf", pdf.getvalue())
    mail.send(msg)
    flash('OK, invoice has been emailed...', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5555,
        debug=True,
    )
