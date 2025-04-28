import { useState } from 'react'
import axios from 'axios'

function App() {
  const [inputText, setInputText] = useState('')
  const [correctedText, setCorrectedText] = useState('')

  const handleCorrect = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/correct', { text: inputText })
      setCorrectedText(response.data.corrected_text)
    } catch (error) {
      console.error('Error correcting speech:', error)
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Speech Correction App</h1>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Type your speech here..."
        rows={5}
        cols={50}
      />
      <br />
      <button onClick={handleCorrect} style={{ marginTop: '1rem' }}>Correct Speech</button>
      <h2>Corrected Text:</h2>
      <p>{correctedText}</p>
    </div>
  )
}

export default App
