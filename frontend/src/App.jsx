import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="*"
          element={<p style={{ padding: '2rem' }}>OP-TRACK scaffold ready for Phase 3 (Frontend).</p>}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
