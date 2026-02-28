from flask import Flask, request, render_template_string, redirect
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/v1/usuarios"

HTML = """
<h2>Usuarios</h2>

<form method="post" action="/crear">
    <input type="number" name="id" placeholder="ID" required>
    <input type="text" name="nombre" placeholder="Nombre" required>
    <input type="number" name="edad" placeholder="Edad" required>
    <button type="submit">Agregar</button>
</form>

<hr>

<ul>
{% for u in usuarios %}
    <li>
        {{u["id"]}} - {{u["nombre"]}} - {{u["edad"]}}
        <a href="/eliminar/{{u['id']}}">Eliminar</a>
    </li>
{% endfor %}
</ul>
"""

@app.route("/")
def index():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if isinstance(data, list):
            usuarios = data
        elif "data" in data:
            usuarios = data["data"]
        elif "usuarios" in data:
            usuarios = data["usuarios"]
        else:
            usuarios = []

        return render_template_string(HTML, usuarios=usuarios)

    except Exception as e:
        return f"Error conectando con FastAPI: {e}"


@app.route("/crear", methods=["POST"])
def crear():
    datos = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }

    requests.post(API_URL, json=datos)
    return redirect("/")


@app.route("/eliminar/<int:id>")
def eliminar(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5010, debug=True)
