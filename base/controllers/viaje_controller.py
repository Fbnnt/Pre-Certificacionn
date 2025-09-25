from flask import render_template, redirect, request, session, flash, url_for
from base.models.viaje_model import Viaje

# Panel principal
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    viajes_usuario = Viaje.viajes_usuario(session['usuario_id'])
    viajes_otros = Viaje.viajes_otros(session['usuario_id'])
    return render_template('dashboard.html', viajes_usuario=viajes_usuario, viajes_otros=viajes_otros)

# Ver detalles de un viaje
@app.route('/viaje/<int:viaje_id>')
def ver_viaje(viaje_id):
    if 'usuario_id' not in session:
        return redirect('/')
    viaje = Viaje.obtener_por_id(viaje_id)
    usuarios = Viaje.usuarios_unidos(viaje_id)
    return render_template('ver_viaje.html', viaje=viaje, usuarios=usuarios)

# Agregar viaje
@app.route('/viaje/nuevo', methods=['GET', 'POST'])
def agregar_viaje():
    if 'usuario_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        data = {
            'destino': request.form['destino'],
            'descripcion': request.form['descripcion'],
            'fecha_inicio': request.form['fecha_inicio'],
            'fecha_fin': request.form['fecha_fin'],
            'planificador_id': session['usuario_id']
        }
        if not Viaje.validar(data):
            return redirect('/viaje/nuevo')
        Viaje.crear(data)
        return redirect('/dashboard')
    return render_template('agregar_viaje.html')

# Unirse a un viaje
@app.route('/viaje/unirse/<int:viaje_id>')
def unirse_viaje(viaje_id):
    if 'usuario_id' not in session:
        return redirect('/')
    Viaje.unirse(session['usuario_id'], viaje_id)
    return redirect('/dashboard')

# Cancelar unión a un viaje
@app.route('/viaje/cancelar/<int:viaje_id>')
def cancelar_union(viaje_id):
    if 'usuario_id' not in session:
        return redirect('/')
    Viaje.cancelar_union(session['usuario_id'], viaje_id)
    return redirect('/dashboard')

# Eliminar viaje (solo si es el creador)
@app.route('/viaje/eliminar/<int:viaje_id>')
def eliminar_viaje(viaje_id):
    if 'usuario_id' not in session:
        return redirect('/')
    viaje = Viaje.obtener_por_id(viaje_id)
    if viaje and viaje.planificador_id == session['usuario_id']:
        Viaje.eliminar(viaje_id)
    return redirect('/dashboard')