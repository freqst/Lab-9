from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder= 'template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hardware.db'
db = SQLAlchemy(app)

class HardwarePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    parts = HardwarePart.query.all()
    total_cost = sum(part.price for part in parts)
    return render_template('index.html', parts=parts, total_cost=total_cost)

@app.route('/add', methods=['POST'])
def add_part():
    device = request.form['device']
    price = float(request.form['price'])

    new_part = HardwarePart(device=device, price=price)
    db.session.add(new_part)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_part(id):
    part = HardwarePart.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()

    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)