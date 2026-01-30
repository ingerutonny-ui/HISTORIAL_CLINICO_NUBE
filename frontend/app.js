const { useState, useEffect } = React;

function App() {
    const [formData, setFormData] = useState({ nombres: '', apellidos: '', documento_identidad: '' });
    const [codigoPrevio, setCodigoPrevio] = useState('');
    const [resultadoFinal, setResultadoFinal] = useState(null);

    // Lógica para generar el código apenas escribes (Como en la versión corta)
    useEffect(() => {
        if (formData.nombres && formData.apellidos) {
            const iniciales = (formData.nombres[0] + formData.apellidos[0]).toUpperCase();
            const numAleatorio = Math.floor(1000 + Math.random() * 9000);
            setCodigoPrevio(`${iniciales}${numAleatorio}`);
        } else {
            setCodigoPrevio('');
        }
    }, [formData.nombres, formData.apellidos]);

    const registrar = async (e) => {
        e.preventDefault();
        try {
            const datosAEnviar = { ...formData, codigo_paciente: codigoPrevio };
            const res = await axios.post('https://historial-clinico-936s.onrender.com/pacientes/', datosAEnviar);
            setResultadoFinal(res.data);
            alert("¡GUARDADO EN LA NUBE!");
        } catch (err) {
            alert("Error al conectar con Render. Revisa que el servidor esté activo.");
        }
    };

    return (
        <div className="bg-white p-10 rounded-3xl shadow-2xl w-[450px]">
            <h1 className="text-3xl font-extrabold text-center text-slate-800 mb-6">REGISTRO DE PACIENTE</h1>
            <form onSubmit={registrar} className="space-y-5">
                <input type="text" placeholder="Nombres" required className="w-full p-4 border rounded-xl bg-blue-50"
                    onChange={e => setFormData({...formData, nombres: e.target.value})} />
                
                <input type="text" placeholder="Apellidos" required className="w-full p-4 border rounded-xl"
                    onChange={e => setFormData({...formData, apellidos: e.target.value})} />
                
                <input type="text" placeholder="Documento de Identidad" required className="w-full p-4 border rounded-xl"
                    onChange={e => setFormData({...formData, documento_identidad: e.target.value})} />
                
                {codigoPrevio && (
                    <div className="p-4 border-2 border-dashed border-blue-400 rounded-xl text-center bg-blue-50">
                        <span className="text-blue-700 font-bold text-xl uppercase italic">
                            CÓDIGO SUGERIDO: {codigoPrevio}
                        </span>
                    </div>
                )}

                <button type="submit" className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700">
                    REGISTRAR PACIENTE
                </button>
            </form>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
