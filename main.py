import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


class Bike(BaseModel):
     bicicleta: str
     precio: str
     especificaciones: str
     categoria: str

app = FastAPI()

@app.get('/')
async def root():
    html_content = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API PYTHON BICICLETAS</title>

       <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        #bicycle-list {
            margin-bottom: 20px;
        }

        button {
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            background-color: #007bff;
            color: #fff;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }
    </style>
    
</head>
<body>
    <h1>Lista de Bicicletas</h1>
    <button id="toggleButton">Mostrar/Ocultar Lista</button>
    <div id="bikes-list" style="display: none;"></div>

    <hr>
    
    <h2>Buscar por ID</h2>
    <form id="searchByIdForm">
        <label for="bikeId">ID de Bicicleta:</label>
        <input type="text" id="bikeId" name="bikeId">
        <button type="submit">Buscar</button>
    </form>
    <div id="bikeDetails"></div>

    <hr>

    <h2>Buscar por Nombre</h2>
    <form id="searchByNameForm">
        <label for="bikeName">Nombre de Bicicleta:</label>
        <input type="text" id="bikeName" name="bikeName">
        <button type="submit">Buscar</button>
    </form>
    <div id="bikeDetailsByName"></div>

    <hr>

    <h2>Dar de Alta una Bicicleta</h2>
    <form id="addBikeForm">
        <label for="newBike">Nombre de Bicicleta:</label>
        <input type="text" id="newBike" name="newBike"><br>
        <label for="newPrice">Precio:</label>
        <input type="text" id="newPrice" name="newPrice"><br>
        <label for="newSpecs">Especificaciones:</label>
        <input type="text" id="newSpecs" name="newSpecs"><br>
        <label for="newCategory">Categoría:</label>
        <input type="text" id="newCategory" name="newCategory"><br>
        <button type="submit">Dar de Alta</button>
    </form>
    <div id="addBikeResponse"></div>

    <hr>

    <h2>Editar una Bicicleta</h2>
    <form id="editBikeForm">
        <label for="editBikeId">ID de Bicicleta:</label>
        <input type="text" id="editBikeId" name="editBikeId"><br>
        <label for="editBikeName">Nombre de Bicicleta:</label>
        <input type="text" id="editBikeName" name="editBikeName"><br>
        <label for="editPrice">Precio:</label>
        <input type="text" id="editPrice" name="editPrice"><br>
        <label for="editSpecs">Especificaciones:</label>
        <input type="text" id="editSpecs" name="editSpecs"><br>
        <label for="editCategory">Categoría:</label>
        <input type="text" id="editCategory" name="editCategory"><br>
        <button type="submit">Editar</button>
    </form>
    <div id="editBikeResponse"></div>

    <hr>

    <h2>Eliminar una Bicicleta por ID</h2>
    <form id="deleteBikeForm">
        <label for="deleteBikeId">ID de Bicicleta:</label>
        <input type="text" id="deleteBikeId" name="deleteBikeId"><br>
        <button type="submit">Eliminar</button>
    </form>
    <div id="deleteBikeResponse"></div>

    <script>
        // Hacer la solicitud GET a la API y mostrar la lista de bicicletas
        fetch('http://127.0.0.1:8000/search_bikes/')
            .then(response => response.json())
            .then(data => {
                const bikesList = document.getElementById('bikes-list');
                data.forEach(bike => {
                    const bikeInfo = document.createElement('div');
                    bikeInfo.innerHTML = `
                        <h2>${bike['Bicicleta ']}</h2>
                        <p><strong>ID:</strong> ${bike['id ']}</p>
                        <p><strong>Precio:</strong> ${bike['Precio ']}</p>
                        <p><strong>Especificaciones:</strong> ${bike['especificaciones ']}</p>
                        <p><strong>Categoría:</strong> ${bike['categoria ']}</p>
                        <hr>
                    `;
                    bikesList.appendChild(bikeInfo);
                });
            })
            .catch(error => console.error('Error:', error));

        // Obtener el botón y la lista de bicicletas
        const toggleButton = document.getElementById('toggleButton');
        const bikesList = document.getElementById('bikes-list');

        // Agregar un event listener para el botón
        toggleButton.addEventListener('click', function() {
            if (bikesList.style.display === 'none') {
                bikesList.style.display = 'block';
            } else {
                bikesList.style.display = 'none';
            }
        });

        // Obtener el formulario y el contenedor de detalles de bicicletas por ID
        const searchByIdForm = document.getElementById('searchByIdForm');
        const bikeDetails = document.getElementById('bikeDetails');

        // Agregar un event listener para el formulario de búsqueda por ID
        searchByIdForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario se envíe por defecto

            const bikeId = document.getElementById('bikeId').value;

            // Hacer la solicitud GET a la API con el ID de la bicicleta
            fetch(`http://127.0.0.1:8000/search_bike/${bikeId}/`)
                .then(response => response.json())
                .then(data => {
                    // Mostrar los detalles de la bicicleta encontrada por ID
                    const bikeDetailsInfo = document.createElement('div');
                    bikeDetailsInfo.innerHTML = `
                        <h2>Detalles de la Bicicleta</h2>
                        <p><strong>ID:</strong> ${data['id ']}</p>
                        <p><strong>Bicicleta:</strong> ${data['Bicicleta ']}</p>
                        <p><strong>Precio:</strong> ${data['Precio ']}</p>
                        <p><strong>Especificaciones:</strong> ${data['especificaciones ']}</p>
                        <p><strong>Categoría:</strong> ${data['categoria ']}</p>
                    `;
                    bikeDetails.innerHTML = ''; // Limpiar los detalles anteriores
                    bikeDetails.appendChild(bikeDetailsInfo);
                })
                .catch(error => {
                    // Manejar el error si la bicicleta no se encuentra
                    bikeDetails.innerHTML = '<p>Bicicleta no encontrada</p>';
                    console.error('Error:', error);
                });
        });

        // Obtener el formulario y el contenedor de detalles de bicicletas por nombre
        const searchByNameForm = document.getElementById('searchByNameForm');
        const bikeDetailsByName = document.getElementById('bikeDetailsByName');

        // Agregar un event listener para el formulario de búsqueda por nombre
        searchByNameForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario se envíe por defecto

            const bikeName = document.getElementById('bikeName').value;

            // Hacer la solicitud GET a la API con el nombre de la bicicleta
            fetch(`http://127.0.0.1:8000/search_bike_name/${bikeName}/`)
                .then(response => response.json())
                .then(data => {
                    // Mostrar los detalles de la bicicleta encontrada por nombre
                    const bikeDetailsByNameInfo = document.createElement('div');
                    bikeDetailsByNameInfo.innerHTML = `
                        <h2>Detalles de la Bicicleta</h2>
                        <p><strong>ID:</strong> ${data['id ']}</p>
                        <p><strong>Bicicleta:</strong> ${data['Bicicleta ']}</p>
                        <p><strong>Precio:</strong> ${data['Precio ']}</p>
                        <p><strong>Especificaciones:</strong> ${data['especificaciones ']}</p>
                        <p><strong>Categoría:</strong> ${data['categoria ']}</p>
                    `;
                    bikeDetailsByName.innerHTML = ''; // Limpiar los detalles anteriores
                    bikeDetailsByName.appendChild(bikeDetailsByNameInfo);
                })
                .catch(error => {
                    // Manejar el error si la bicicleta no se encuentra
                    bikeDetailsByName.innerHTML = '<p>Bicicleta no encontrada</p>';
                    console.error('Error:', error);
                });
        });

        // Obtener el formulario y el contenedor de respuesta de dar de alta una bicicleta
        const addBikeForm = document.getElementById('addBikeForm');
        const addBikeResponse = document.getElementById('addBikeResponse');

        // Agregar un event listener para el formulario de dar de alta una bicicleta
        addBikeForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario se envíe por defecto

            // Obtener los valores del formulario
            const newBike = document.getElementById('newBike').value;
            const newPrice = document.getElementById('newPrice').value;
            const newSpecs = document.getElementById('newSpecs').value;
            const newCategory = document.getElementById('newCategory').value;

            // Construir el objeto con los datos de la nueva bicicleta
            const newBikeData = {
                bicicleta: newBike,
                precio: newPrice,
                especificaciones: newSpecs,
                categoria: newCategory
            };

            // Hacer la solicitud POST a la API para dar de alta la bicicleta
            fetch('http://127.0.0.1:8000/add_bike', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newBikeData)
            })
                .then(response => response.json())
                .then(data => {
                    // Mostrar la respuesta de dar de alta la bicicleta
                    addBikeResponse.innerHTML = `<p>Bicicleta dada de alta</p>`;
                })
                .catch(error => {
                    // Manejar el error si ocurre algún problema
                    addBikeResponse.innerHTML = '<p>Error al dar de alta la bicicleta</p>';
                    console.error('Error:', error);
                });
        });

        // Obtener el formulario y el contenedor de respuesta de editar una bicicleta
        const editBikeForm = document.getElementById('editBikeForm');
        const editBikeResponse = document.getElementById('editBikeResponse');

        // Agregar un event listener para el formulario de editar una bicicleta
        editBikeForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario se envíe por defecto

            // Obtener los valores del formulario
            const editBikeId = document.getElementById('editBikeId').value;
            const editBikeName = document.getElementById('editBikeName').value;
            const editPrice = document.getElementById('editPrice').value;
            const editSpecs = document.getElementById('editSpecs').value;
            const editCategory = document.getElementById('editCategory').value;

            // Construir el objeto con los datos para editar la bicicleta
            const editBikeData = {
                bicicleta: editBikeName,
                precio: editPrice,
                especificaciones: editSpecs,
                categoria: editCategory
            };

            // Hacer la solicitud PUT a la API para editar la bicicleta
            fetch(`http://127.0.0.1:8000/change_bike/${editBikeId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(editBikeData)
            })
                .then(response => response.json())
                .then(data => {
                    // Mostrar la respuesta de editar la bicicleta
                    editBikeResponse.innerHTML = `<p>Bicicleta editada</p>`;
                })
                .catch(error => {
                    // Manejar el error si ocurre algún problema
                    editBikeResponse.innerHTML = '<p>Error al editar la bicicleta</p>';
                    console.error('Error:', error);
                });
        });

        // Obtener el formulario y el contenedor de respuesta de eliminar una bicicleta
        const deleteBikeForm = document.getElementById('deleteBikeForm');
        const deleteBikeResponse = document.getElementById('deleteBikeResponse');

        // Agregar un event listener para el formulario de eliminar una bicicleta
        deleteBikeForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario se envíe por defecto

            // Obtener el ID de la bicicleta a eliminar
            const bikeId = document.getElementById('deleteBikeId').value;

            // Hacer la solicitud DELETE a la API para eliminar la bicicleta
            fetch(`http://127.0.0.1:8000/delete_bike/${bikeId}/`, {
                method: 'DELETE'
            })
                .then(response => response.json())
                .then(data => {
                    // Mostrar la respuesta de eliminar la bicicleta
                    deleteBikeResponse.innerHTML = `<p>Bicicleta eliminado</p>`;
                })
                .catch(error => {
                    // Manejar el error si ocurre algún problema
                    deleteBikeResponse.innerHTML = '<p>Error al eliminar la bicicleta</p>';
                    console.error('Error:', error);
                });
        });
    </script>
</body>
</html>


    """
    return HTMLResponse(content=html_content, status_code=200)


#RUTA PARA DEVOLVER TODAS LAS BICICLETAS
@app.get("/search_bikes")
async def read_bikes():
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("SELECT id, bicicleta, precio, especificaciones, categoria FROM bikes")
 resultados = cursor.fetchall()
 conn.close()
 if resultados:
    return [{"id ":resultado[0] ,"Bicicleta ": resultado[1], "Precio ": resultado[2], "especificaciones ": resultado[3] , "categoria ": resultado[4]} for resultado in resultados]
 else:
    return {"mensaje": "No hay datos en la base de datos"}
 

#RUTA PARA BUSCAR UNA BICICLETA EN ESPECIFICO POR ID
@app.get("/search_bike/{id}/")
async def search_bike(id: int):
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("SELECT id, bicicleta, precio, especificaciones, categoria FROM bikes WHERE id=?", (id,))
 resultado = cursor.fetchone()
 conn.close()
 if resultado is not None:
    return {"id ":resultado[0] ,"Bicicleta ": resultado[1], "Precio ": resultado[2], "especificaciones ": resultado[3] , "categoria ": resultado[4]}
 else:
    return {"mensaje": "Datos no encontrados"}

#RUTA PARA BUSCAR UNA BICICLETA EN ESPECIFICO POR NOMBRE
@app.get("/search_bike_name/{bike}/")
async def search_bike_name(bike: str):
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("SELECT id, bicicleta, precio, especificaciones, categoria FROM bikes WHERE bicicleta=?", (bike,))
 resultado = cursor.fetchone()
 conn.close()
 if resultado is not None:
    return {"id ":resultado[0] ,"Bicicleta ": resultado[1], "Precio ": resultado[2], "especificaciones ": resultado[3] , "categoria ": resultado[4]}
 else:
    return {"mensaje": "Datos no encontrados"}


#RUTA PARA DAR DE ALTA BICICLETA
@app.post("/add_bike/")
async def add_bike(item: Bike):
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("INSERT INTO bikes (bicicleta, precio, especificaciones, categoria) VALUES (?, ?, ?, ?)", (item.bicicleta, item.precio, item.especificaciones, item.categoria))
 conn.commit()
 conn.close()
 return {"mensaje": "Datos agregados exitosamente"}

#RUTA PAR MODIFICAR UNA BICICLETA
@app.put("/change_bike/{id}/")
async def change_bike(id: int, item: Bike):
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("UPDATE bikes SET bicicleta=?, precio=?, especificaciones=? , categoria=?  WHERE id=?", (item.bicicleta, item.precio, item.especificaciones, item.categoria, id))
 conn.commit()
 conn.close()
 return {"mensaje": "Datos actualizados exitosamente"}

#RUTA PARA ELIMINAR BICICLETA
@app.delete("/delete_bike/{id}/")
async def delete_bike(id: int):
 conn = sqlite3.connect("hot100.db")
 cursor = conn.cursor()
 cursor.execute("DELETE FROM bikes WHERE id=?", (id,))
 conn.commit()
 conn.close()
 return {"mensaje": "Datos eliminados exitosamente"}