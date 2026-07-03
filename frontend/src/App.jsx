import { useState } from 'react';
import axios from 'axios';
//import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Ajoute le message utilisateur
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    try {
      // Appel au backend FastAPI
      const response = await axios.get('http://localhost:8000/api/chat', {
        params: { message: input }
      });
      
      // Ajoute la réponse de l'IA
      setMessages([...newMessages, { role: 'ai', content: response.data.response }]);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role}>{msg.content}</div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Envoyer</button>
    </div>
  );
}

export default App;