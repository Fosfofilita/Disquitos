from flask import Flask, jsonify, request, session
from flasgger import Swagger
from productos import producto

app = Flask (__name__)
app.secret_key = "123"

app.config['SWAGGER'] = {
    'openapi': '3.0.3'
}
swagger = Swagger (app, template_file='disquitos.yaml')

@app.route('/')
def inicio():
    return ("Bienvenido a disquitos")

@app.route('/productos')
def get_productos():
    return jsonify({"Discos Disponibles": producto}) 

@app.route('/productos/<string:nombre>')
def get_producto(nombre):
    producto_encontrado = [p for p in producto if p ['nombre']  == nombre]
    if (len(producto_encontrado)>0):
        return jsonify({"disco": producto_encontrado[0]})
    else:
        return ("Producto no encontrado"),404

@app.route('/carrito', methods=['GET', 'POST'])
def agregar_carrito():
    if 'carrito'not in session:
        session['carrito']= []

    if request.method == 'GET':
        return jsonify({"Carrito": session['carrito']})

    if request.method == 'POST':
        data = request.get_json(force=True)
        nombre = data.get('nombre')
        cantidad= data.get('cantidad', 1)

        if not nombre:
            return ("Falta el nombre del producto"),400
            
        producto_encontrado= next((p for p in producto if p ['nombre']== nombre), None)
        if not producto_encontrado:
            return ("Producto no encontrado"),404


        carrito= session ['carrito'] 
        produ_encontrado = next(( p for p in carrito if p ['nombre']== nombre), None)

        if produ_encontrado:
            produ_encontrado['cantidad'] += cantidad
        else:
            carrito.append({
                "nombre": producto_encontrado['nombre'],
                "precio": producto_encontrado['precio'],
                "cantidad": cantidad }) 
        
        session.modified = True

        return jsonify({"Producto agregado": nombre, "carrito": carrito})

@app.route('/carrito/<string:nombre>', methods=['DELETE'])
def eliminar_carrito(nombre):

    if 'carrito' not in session:
        return "Carrito vacio"
    
    carrito= session ['carrito'] 
    producto_encontrado = next((p for p in carrito if p['nombre'] == nombre), None)
    
    if not producto_encontrado:
        return ("Producto no encontrado en el carrito"),404
    
    carrito.remove(producto_encontrado)
    session.modified = True
    return jsonify({ "Producto eliminado": producto_encontrado, "carrito": carrito}),200

@app.route('/carrito/total', methods=['GET'])
def total_carrito():

    carrito = session.get('carrito', [])
    total = sum(p['precio'] * p['cantidad'] for p in carrito)

    return jsonify({"Total de Compra": total})


if __name__ == '__main__':
    app.run(debug=True)



