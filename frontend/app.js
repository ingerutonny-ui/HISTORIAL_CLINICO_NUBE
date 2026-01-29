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
        try {
            // Usamos tu URL real de Render que aparece en tus capturas
            const response = await axios.post('https://historial-clinico-936s.onrender.com/pacientes/', formData);
            setPacienteCreado(response.data);
            alert("¡Paciente registrado exitosamente en HISTORIAL_CLINICO_NUBE!");
        } catch (error) {
            console.error("Error al registrar:", error);
            alert("Hubo un problema al conectar con el servidor en la nube.");
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="bg-white p-10 rounded-3xl shadow-2xl w-[450px] border border-gray-100">
            <h1 className="text-3xl font-extrabold text-center text-slate-800 tracking-tight mb-1">REGISTRO DE PACIENTE</h1>
            <p className="text-center text-sm text-gray-500 mb-8">Proyecto: <span className="font-semibold text-black">HISTORIAL_CLINICO_NUBE</span></p>
            
            <div className="bg-amber-50 text-amber-700 text-center py-2 rounded-lg mb-6 text-sm border border-amber-100">
                Fecha de Ingreso: {new Date().toLocaleDateString()}
            </div>

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
                    <div className="mt-6 p-4 border-2 border-dashed border-blue-300 rounded-xl text-center">
                        <span className="text-blue-500 font-mono font-bold">CÓDIGO GENERADO: {pacienteCreado.codigo_paciente}</span>
                    </div>
                )}

                <button 
                    type="submit" 
                    disabled={cargando}
                    className={`w-full ${cargando ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'} text-white py-4 rounded-xl font-bold text-lg shadow-lg shadow-blue-200 transition-all uppercase tracking-wider`}
                >
                    {cargando ? 'Registrando...' : 'Registrar Paciente'}
                </button>
            </form>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
