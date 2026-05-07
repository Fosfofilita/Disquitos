import pytest
from app import app

@pytest.fixture
def cliente():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test123'
    with app.test_client() as cliente:
        yield cliente

def test_inicio(cliente):
    respuesta = cliente.get('/')
    assert respuesta.status_code == 200

def test_get_productos(cliente):
    respuesta = cliente.get('/productos')
    assert respuesta.status_code == 200

def test_producto_existe(cliente):
    respuesta = cliente.get('/productos/Yes')
    assert respuesta.status_code == 200
    dato= respuesta.get_json()
    assert 'disco' in dato

def test_producto_no_existe(cliente):
    respuesta = cliente.get('/productos/Ten')
    assert respuesta.status_code == 404

def test_agregar_carrito(cliente):
    respuesta = cliente.post('/carrito', json={"nombre": "Gulp", "cantidad": 2})
    assert respuesta.status_code == 200
    dato = respuesta.get_json()
    assert dato['Producto agregado'] == 'Gulp'

def test_agregar_carrito_producto_no_existe(cliente):
    respuesta = cliente.post('/carrito', json={"nombre": "Ten", "cantidad": 1})
    assert respuesta.status_code == 404

def test_agregar_carrito_falta_nombre(cliente):
    respuesta = cliente.post('/carrito', json={"cantidad": 1})
    assert respuesta.status_code == 400

def test_eliminar_carrito(cliente):
    cliente.post('/carrito', json={"nombre": "Gulp", "cantidad": 2})
    respuesta = cliente.delete('/carrito/Gulp')
    assert respuesta.status_code == 200
    dato = respuesta.get_json()
    assert dato['Producto eliminado']['nombre'] == 'Gulp'

def test_total_carrito(cliente):
    cliente.post('/carrito', json={"nombre": "Gulp", "cantidad": 2})
    cliente.post('/carrito', json={"nombre": "Yes", "cantidad": 1})
    respuesta = cliente.get('/carrito/total')
    assert respuesta.status_code == 200
    dato = respuesta.get_json()
    assert dato['Total de Compra'] == 3000

