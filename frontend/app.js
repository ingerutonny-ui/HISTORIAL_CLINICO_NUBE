const { useState } = React;

function App() {
    const [formData, setFormData] = useState({
        nombres: '',
        apellidos: '',
        documento_identidad: ''
    });
    const [pacienteCreado, setPacienteCreado] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Enviando datos a Render...", formData);
        
        try {
            const response = await axios.post('https://historial-clinico-936s.onrender.com/pacientes/', formData);
            
            console.log("Respuesta del servidor:", response.data);
            setPacienteCreado(response.data);
            
            // Esta alerta nos confirmará que el código LLEGÓ del servidor
            alert("CONECTADO: El código generado es " + response.data.codigo_paciente);
            
        } catch (error) {
            console.error("Error detallado:", error);
            alert("ERROR DE CONEXIÓN: Verifica que el Backend en Render esté activo.");
        }
    };

    return (
        <div className="bg-white p-10 rounded-3xl shadow-2xl w-[450px] border border-gray-100">
            <h1 className="text-3xl font-extrabold text-center text-slate-800 mb-1">REGISTRO DE PACIENTE</h1>
            <p className="text-center text-sm text-gray-500 mb-8">Proyecto: <strong>HISTORIAL_CLINICO_NUBE</strong></p>
            
            <form onSubmit={handleSubmit} className="space-y-5">
                <input 
                    type="text" 
                    placeholder="Nombres" 
                    className="w-full p-4 border border-gray-200 rounded-xl bg-blue-50"
                    onChange={(e) => setFormData({...formData, nombres: e.target.value})}
                    required
                />
                <input 
                    type="text" 
                    placeholder="Apellidos" 
                    className="w-full p-4 border border-gray-200 rounded-xl"
                    onChange={(e) => setFormData({...formData, apellidos: e.target.value})}
                    required
                />
                <input 
                    type="text" 
                    placeholder="Documento de Identidad" 
                    className="w-full p-4 border border-gray-200 rounded-xl"
                    onChange={(e) => setFormData({...formData, documento_identidad: e.target.value})}
                    required
                />
                
                {pacienteCreado && (
                    <div className="mt-6 p-4 border-2 border-dashed border-blue-400 rounded-xl text-center bg-blue-50">
                        <span className="text-blue-600 font-mono font-bold text-xl">
                            CÓDIGO: {pacienteCreado.codigo_paciente}
                        </span>
                    </div>
                )}

                <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-all">
                    REGISTRAR PACIENTE
                </button>
            </form>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
