# in flask there  is an orm(object related mapping) where developers can interact with the db's
# in an most effective way such that they don't need to write the sql queries
# in programming only as previous we convert rows into dictionares
# like that we can convert the databses to objects and then we can onnect with the db's
# by creating an instance for each and every object that has been using in an classes
# python program-> classes-> objects->instantiate objects in class
# sql table-> rows, columns-> rows get instatntiated by using the obejcts
# this is called object relation mapping
# so to perform this operations one end point should be there 
# that is api's -> this api's will provide the crud operations


from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# for sessions kind of thing secret key is very importnat or else runtime error will be thr
app.config['SECRET_KEY'] = 'revathi'  # Change this to a strong, random value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlit3'

# here we are creating the object of sqlalcemy class
# and taking te object as an paramter
db = SQLAlchemy(app)
class students(db.Model):
    id = db.Column('student_id', db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin  = pin

# db.create_all()


@app.route('/')
def show_all():
    return render_template('show_all.html',students = students.query.all())

@app.route('/new', methods= ['GET','POST'])
def new():
    if request.method == 'POST':
        print(request.form)  # Debugging step

        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash("please enter all fields revathi...", 'error')
        else:
            # here when the fields are all filled in the form
            # and then for students class->student object is being created
            # suppose in form i entered revathi
            # request.form['name'] = "name" =>revathi it will get cause i submitted there and then
            # obviously studnets is an table then in that db object row will be inserted
            # and yes the order should be correct or else error will raises
            student = students(request.form['name'],request.form["city"], request.form['addr'], request.form['pin'],)
# default sqlaclchemy method to add the student into db
            db.session.add(student)
            db.session.commit()
# andflash message will be displays that the data is inserted successfully
            flash("record successfully entered")
            return redirect(url_for('show_all'))
    return render_template('new.html')

@app.route('/delete/<int:id>')
def delete(id):
    student = students.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for("show_all"))

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    # students->query->getting the id of an person to edit the route
    student =  students.query.get(id)
    if not student:
        flash("student not found")
        return redirect(url_for("show_all"))
    if request.method == 'POST':
        # getting all the submitted forms resuts into student
        student.name= request.form["name"]
        student.city = request.form["city"]
        student.addr = request.form["addr"]
        student.pin = request.form["pin"]
# commiting the results for it
        db.session.commit()
        flash("record updated revathi")
        return redirect(url_for("show_all"))
    
    return render_template('edit.html', student=student)

if __name__== '__main__':
    with app.app_context():  # <-- This is the fix
        db.create_all()
    app.run(debug=True)

