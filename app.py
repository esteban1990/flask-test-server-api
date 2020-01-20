import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from  flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Contact, Todo


BASE_DIR = os.path.abspath(os.path.dirname( __file__))  #guarda la ruta del directorio de mi aplicacion// donde estoy ubicado

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db') #cual va ser la base de datos que voi a utilizar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # EVITA QUE MI BASE DE DATOS GUARDE CAMBIOS INNECESARIOS CADA VEZ QUE HAGO UNA MODIFICACION A NIVEL DE TABLAS

db.init_app(app)
migrate = Migrate(app, db)#genera los comandos para crear la migracion.

manager = Manager(app)
manager.add_command('db', MigrateCommand)#ejecuta mis migraciones por consola
CORS(app) #evite que tenga problemas con el navegador,para que pueda utilizarse en manera de desarollo


@app.route('/') #se crea una ruta principal
def home():
    return render_template('index.htm', name = "home")
@app.route("/api/contacts", methods=['GET', 'POST']) 
@app.route("/api/contacts/<int:id>", methods= ['GET','PUT','DELETE'])
def contacts(id = None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(contact.serialize()),200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200

    if request.method=="POST":
        if not request.json.get("name"):
            return jsonify({ "name": "is required"}), 422
        if not request.json.get("phone") :
            return jsonify({"phone": "is required"}), 422   
        
        contact = Contact()
        contact.name = request.json.get("name")
        contact.phone = request.json.get("phone")

        db.session.add(contact)
        db.session.commit()

        return jsonify(contact.serialize()), 201

    if request.method=="PUT":
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"contact": "Not Found" }), 404
        if not request.json.get("name"):
            return jsonify({ "name": "is required"}), 422
        if not request.json.get("phone") :
            return jsonify({"phone": "is required"}), 422  

        contact.name = request.json.get("name")
        contact.phone =request.json.get("phone")
            
        db.session.commit()
        
        return jsonify(contact.serialize()), 201

        
    if request.method=="DELETE":
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"msge": "Not Found" }), 404

        db.session.delete(contact)
        return jsonify({"msge": "Contact Delete" }), 200
        


#@app.route("/api/user/<username>/todos", methods=['GET', 'POST']) 
#@app.route("/api/user/<username>/todos/<int:id>", methods= ['GET','PUT','DELETE'])
# def todos(username, id)        
@app.route("/api/todos", methods=['GET', 'POST']) 
@app.route("/api/todos/<int:id>", methods= ['GET','PUT','DELETE'])
def todos(id = None):
    if request.method == 'GET':
        if id is not None:
            todo = Todo.query.get(id)
            if contact:
                return jsonify(todo.serialize()),200
            else:
                return jsonify({"msg": "Not Found"}), 404
        else:
            todos = Todo.query.all()
            todos = list(map(lambda todo: todo.serialize(), todos))
            return jsonify(todos), 200

    if request.method=="POST":
        if not request.json.get("label"):
            return jsonify({ "label": "is required"}), 422
        #if not request.json.get("done") :
        #    return jsonify({"done": "is required"}), 422   
        
        todo = Todo()
        todo.label = request.json.get("label")
        todo.done = request.json.get("done")

        db.session.add(todo)
        db.session.commit()

        return jsonify(todo.serialize()), 201

    if request.method=="PUT":
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"todo": "Not Found" }), 404
        if not request.json.get("label"):
            return jsonify({ "label": "is required"}), 422
        #if not request.json.get("done") :
        #    return jsonify({"done": "is required"}), 422  

        todo.label = request.json.get("label")
        todo.done = request.json.get("done")
            
        db.session.commit()
        
        return jsonify(todo.serialize()), 201

        
    if request.method=="DELETE":
        todo = Todo.query.get(id)
        if not todo:
            return jsonify({"msge": "Not Found" }), 404

        db.session.delete(todo)
        return jsonify({"msge": "Todo Delete" }), 200
        




if __name__ == "__main__":
    manager.run() # inicializa mi aplicacion


