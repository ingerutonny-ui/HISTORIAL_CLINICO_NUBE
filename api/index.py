<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historial Clínico en la Nube</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        form {
            max-width: 400px;
            margin: auto;
        }
        input, button {
            display: block;
            width: 100%;
            margin-bottom: 10px;
            padding: 8px;
        }
        #fecha-actual {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Registro de Pacientes</h1>
    <form id="form-paciente">
        <input type="text" id="nombre" placeholder="Nombre" required>
        <input type="text" id="apellido" placeholder="Apellido" required>
        <input type="text" id="ci" placeholder="Cédula de Identidad (CI)" required>
        <p>Fecha de ingreso: <span id="fecha-actual"></span></p>
        <button type="submit">Registrar</button>
    </form>

    <script>
        // Mostrar fecha actual
        document.getElementById("fecha-actual").textContent = new Date().toLocaleDateString();

        // Generar código único
        function generarCodigo(nombre, apellido) {
            const fecha = new Date().getTime();
            return nombre.substring(0,2).toUpperCase() + apellido.substring(0,2).toUpperCase() + fecha;
        }

        // Manejar envío del formulario
        document.getElementById("form-paciente").addEventListener("submit", async function(e) {
            e.preventDefault();

            const nombre = document.getElementById("nombre").value.trim();
            const apellido = document.getElementById("apellido").value.trim();
            const ci = document.getElementById("ci").value.trim();
            const fechaIngreso = document.getElementById("fecha-actual").textContent;
            const codigo = generarCodigo(nombre, apellido);

            const paciente = { nombre, apellido, ci, fechaIngreso, codigo };

            try {
                const response = await fetch("/api/registrar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(paciente)
                });

                const data = await response.json();
                alert(data.mensaje || "Paciente registrado correctamente");
            } catch (error) {
                alert("Error al registrar paciente: " + error);
            }
        });
    </script>
</body>
</html>
