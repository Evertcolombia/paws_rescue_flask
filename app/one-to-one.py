class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    department_name = db.Column(db.String, db.ForeignKey('department.name'), nullable = False)
    is_head_of = db.Column(db.String, db.ForeignKey('department.name'), nullable=True)
        
class Department(db.Model):
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    employees = db.relationship('Employee', backref='department')
    head = db.relationship('Employee', backref='head_of_department', uselist=False)
    
class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False) 