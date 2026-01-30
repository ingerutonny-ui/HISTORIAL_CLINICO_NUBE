const { useState } = React;

function App() {
    const [formData, setFormData] = useState({ nombres: '', apellidos: '', documento_identidad: '' });
    const [pacienteCreado, setPacienteCreado] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setPacienteCreado(null);
        setError(null);

        try {
            // URL EXACTA DE TU RENDER
            const url = 'https://historial-clinico-936s.onrender.com/pacientes/';
            const response = await axios.post(url, formData);
            setPacienteCreado(response.data);
        } catch (err) {
            console.error(err);
            setError("Error de conexión. Revisa que Render esté activo.");
        }
    };

    return (
        <div className="bg-white p-10 rounded-3xl shadow-2xl w-[450px]">
            <h1 className="text-3xl font-extrabold text-center text-slate-800 mb-6">REGISTRO DE PACIENTE</h1>
            <form onSubmit={handleSubmit} className="space-y-5">
                <input type="text" placeholder="Nombres" required className="w-full p-4 border rounded-xl bg-blue-50"
                    onChange={(e) => setFormData({...formData, nombres: e.target.value})} />
                <input type="text" placeholder="Apellidos" required className="w-full p-4 border rounded-xl"
                    onChange={(e) => setFormData({...formData, apellidos: e.target.value})} />
                <input type="text" placeholder="Documento de Identidad" required className="w-full p-4 border rounded-xl"
                    onChange={(e) => setFormData({...formData, documento_identidad: e.target.value})} />
                
                {pacienteCreado && (
                    <div className="p-4 border-2 border-dashed border-blue-400 rounded-xl text-center bg-blue-50">
                        <span className="text-blue-700 font-bold text-xl">CÓDIGO: {pacienteCreado.codigo_paciente}</span>
                    </div>
                )}
                {error && <p className="text-red-500 text-center font-bold">{error}</p>}

                <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700">
                    REGISTRAR PACIENTE
                </button>
            </form>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
