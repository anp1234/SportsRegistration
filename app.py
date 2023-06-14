from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy




app= Flask(__name__)
REGISTRANT={}
SPORTS=['Basketball',
        'Football',
        'Cricket',
        'Chess',
        'Badminton',
        'Tennis',
        'Hockey',
        'Swimming',
        'Volleyball']

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.sqlite3'
db=SQLAlchemy(app)

class Registration(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column("Name",db.String(255), nullable=False)
    sport=db.Column("Sport",db.String(255), nullable=False)

    def __init__(self,name,sport):
        self.name = name
        self.sport = sport

@app.route('/')
def index():
    return render_template('index.html',sports=SPORTS)


@app.route('/register', methods=['POST','GET'])
def register():
    name=request.form.get('name')
    sport=request.form.get('sport')
    REGISTRANT[name]=sport
    
    if name=='' or sport not in SPORTS:
        return render_template('failure.html')
    else:
        new_register=Registration(name,sport)
        db.session.add(new_register)
        db.session.commit()
        return render_template('register.html')



@app.route('/registrant', methods=['POST','GET'])
def registrant():
        all_registrant=Registration.query.order_by(Registration.id).all()
        return render_template('registrant.html',registrants=all_registrant)
    
    
@app.route('/delete/<int:id>')
def delete(id):
    register_to_delete=Registration.query.get_or_404(id)
    db.session.delete(register_to_delete)
    db.session.commit()
    return redirect('/registrant')


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    register_to_update=Registration.query.get_or_404(id)
    if request.method=='POST':
        register_to_update.name=request.form.get('name')
        register_to_update.sport=request.form.get('sport')
        db.session.commit()
        return redirect('/registrant')
    
    else:
        return render_template('update.html',sports=SPORTS,registrant=register_to_update)
    
    
    
    






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
