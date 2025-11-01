from database import db

# Tabla intermedia para relación muchos a muchos
ninja_jutsu = db.Table('ninja_jutsu',
    db.Column('ninja_id', db.Integer, db.ForeignKey('ninja.id'), primary_key=True),
    db.Column('jutsu_id', db.Integer, db.ForeignKey('jutsu.id'), primary_key=True)
)

class Aldea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

class Jutsu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))

class Ninja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rango = db.Column(db.String(20), nullable=False)  
    ataque = db.Column(db.Integer, default=0)
    defensa = db.Column(db.Integer, default=0)
    chakra = db.Column(db.Integer, default=0)
    aldea_id = db.Column(db.Integer, db.ForeignKey('aldea.id'), nullable=False)
    aldea = db.relationship('Aldea', backref=db.backref('ninjas', lazy=True))
    jutsus = db.relationship('Jutsu', secondary=ninja_jutsu, lazy='subquery',
                             backref=db.backref('ninjas', lazy=True))

# Método para el patrón Visitor
    def accept(self, visitor):
        visitor.visit_ninja(self)

class Mision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rango = db.Column(db.String(10), nullable=False)  
    recompensa = db.Column(db.Float, nullable=False)
    rango_minimo = db.Column(db.String(20), nullable=False)  

# Método para el patrón Visitor
    def accept(self, visitor):
        visitor.visit_mision(self)

class AsignacionMision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ninja_id = db.Column(db.Integer, db.ForeignKey('ninja.id'), nullable=False)
    mision_id = db.Column(db.Integer, db.ForeignKey('mision.id'), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    ninja = db.relationship('Ninja', backref='asignaciones')
    mision = db.relationship('Mision', backref='asignaciones')
