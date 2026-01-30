const { useState } = React;

function App() {
    const [formData, setFormData] = useState({
        nombres: '',
        apellidos: '',
        documento_identidad: ''
    });
    const [pacienteCreado, setPacienteCreado] = useState(null);
    const [cargando, setCargando] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setCargando(true);
        setPacienteCreado(null); // Limpiamos resultado anterior

        try {
            // URL verificada de tu servidor Render
            const response = await axios.post('https://historial-clinico-936s.onrender.com/pacientes/', formData);
            
            setPacienteCreado(response.data);
            alert("¡PACIENTE REGISTRADO EXITOSAMENTE!");
        } catch (error) {
            console.error("Error:", error);
            alert("ERROR: No se pudo conectar con el servidor. Asegúrate de que Render esté activo.");
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="bg-white p-10 rounded-3xl shadow-2xl w-[450px] border border-gray-100">
            <h1 className="text-3xl font-extrabold text-center text-slate-800 mb-1 tracking-tight">REGISTRO DE PACIENTE</h1>
            <p className="text-center text-sm text-gray-500 mb-8 uppercase tracking-widest">PROYECTO: <strong>HISTORIAL_CLINICO_NUBE</strong></p>
            
            <form onSubmit={handleSubmit} className="space-y-5">
                <input 
                    type="text" 
                    placeholder="Nombres" 
                    required
                    className="w-full p-4 border border-gray-200 rounded-xl bg-blue-50 focus:ring-2 focus:ring-blue-400 outline-none transition-all"
                    onChange={(e) => setFormData({...formData, nombres: e.target.value})}
                />
                <input 
                    type="text" 
                    placeholder="Apellidos" 
                    required
                    className="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-400 outline-none transition-all"
                    onChange={(e) => setFormData({...formData, apellidos: e.target.value})}
                />
                <input 
                    type="text" 
                    placeholder="Documento de Identidad" 
                    required
                    className="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-400 outline-none transition-all"
                    onChange={(e) => setFormData({...formData, documento_identidad: e.target.value})}
                />
                
                {pacienteCreado && (
                    <div className="mt-6 p-4 border-2 border-dashed border-blue-400 rounded-xl text-center bg-blue-50 animate-pulse">
                        <span className="text-blue-700 font-mono font-bold text-xl uppercase">
                            CÓDIGO GENERADO: {pacienteCreado.codigo_paciente}
                        </span>
                    </div>
                )}

                <button 
                    type="submit" 
                    disabled={cargando}
                    className={`w-full ${cargando ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'} text-white py-4 rounded-xl font-bold text-lg shadow-lg transition-all uppercase`}
                >
                    {cargando ? 'PROCESANDO...' : 'REGISTRAR PACIENTE'}
                </button>
            </form>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
