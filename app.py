import os
from flask import Flask, request, jsonify, render_template
from database import db
from models import Ninja, Mision, Aldea, Jutsu, AsignacionMision
from exporters import CSVExportVisitor, JSONExportVisitor

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'naruto.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Mapeo de rangos para comparación
RANGO_ORDEN = {'Genin': 1, 'Chūnin': 2, 'Jōnin': 3}
MISION_RANGO_NINJA = {'D': 'Genin', 'C': 'Genin', 'B': 'Chūnin', 'A': 'Jōnin', 'S': 'Jōnin'}

# === CLIENTE WEB ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reportes')
def reportes():
    ninjas = Ninja.query.all()
    misiones = Mision.query.all()
    return render_template('reportes.html', ninjas=ninjas, misiones=misiones)

# === API ENDPOINTS ===
@app.route('/api/ninjas', methods=['POST'])
def crear_ninja():
    data = request.json
    aldea = Aldea.query.filter_by(nombre=data['aldea']).first()
    if not aldea:
        aldea = Aldea(nombre=data['aldea'])
        db.session.add(aldea)
        db.session.commit()
    ninja = Ninja(
        nombre=data['nombre'],
        rango=data['rango'],
        ataque=data.get('ataque', 0),
        defensa=data.get('defensa', 0),
        chakra=data.get('chakra', 0),
        aldea_id=aldea.id
    )
    db.session.add(ninja)
    db.session.commit()
    return jsonify({"id": ninja.id}), 201

@app.route('/api/ninjas', methods=['GET'])
def listar_ninjas():
    ninjas = Ninja.query.all()
    return jsonify([{
        'id': n.id,
        'nombre': n.nombre,
        'rango': n.rango,
        'ataque': n.ataque,
        'defensa': n.defensa,
        'chakra': n.chakra,
        'aldea': n.aldea.nombre
    } for n in ninjas])

@app.route('/api/misiones', methods=['POST'])
def crear_mision():
    data = request.json
    mision = Mision(
        nombre=data['nombre'],
        rango=data['rango'],
        recompensa=data['recompensa'],
        rango_minimo=MISION_RANGO_NINJA.get(data['rango'], 'Jōnin')
    )
    db.session.add(mision)
    db.session.commit()
    return jsonify({"id": mision.id}), 201

@app.route('/api/misiones', methods=['GET'])
def listar_misiones():
    misiones = Mision.query.all()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'rango': m.rango,
        'recompensa': m.recompensa,
        'rango_minimo': m.rango_minimo
    } for m in misiones])

@app.route('/api/asignar', methods=['POST'])
def asignar_mision():
    data = request.json
    ninja = Ninja.query.get(data['ninja_id'])
    mision = Mision.query.get(data['mision_id'])
    if not ninja or not mision:
        return jsonify({"error": "Ninja o misión no encontrados"}), 404

    # Validar rango
    if RANGO_ORDEN.get(ninja.rango, 0) < RANGO_ORDEN.get(mision.rango_minimo, 999):
        return jsonify({"error": "El ninja no tiene el rango suficiente"}), 400

    asignacion = AsignacionMision(ninja_id=ninja.id, mision_id=mision.id, completada=False)
    db.session.add(asignacion)
    db.session.commit()
    return jsonify({"mensaje": "Misión asignada"}), 201

@app.route('/api/completar', methods=['POST'])
def completar_mision():
    data = request.json
    asignacion = AsignacionMision.query.get(data['asignacion_id'])
    if asignacion:
        asignacion.completada = True
        db.session.commit()
        return jsonify({"mensaje": "Misión completada"})
    return jsonify({"error": "Asignación no encontrada"}), 404


@app.route('/api/export/<formato>')
def exportar(formato):
    ninjas = Ninja.query.all()
    misiones = Mision.query.all()

    if formato == 'csv':
        visitor = CSVExportVisitor()
        for n in ninjas:
            n.accept(visitor)
        for m in misiones:
            m.accept(visitor)
        return visitor.get_result(), 200, {'Content-Type': 'text/csv'}

    elif formato == 'json':
        visitor = JSONExportVisitor()
        for n in ninjas:
            n.accept(visitor)
        for m in misiones:
            m.accept(visitor)
        return visitor.get_result(), 200, {'Content-Type': 'application/json'}

    else:
        return jsonify({"error": "Formato no soportado. Use 'csv' o 'json'."}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=5000, debug=True)
