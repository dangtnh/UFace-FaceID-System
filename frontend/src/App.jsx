import React, { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [status, setStatus] = useState("Đang kết nối Backend...")

  useEffect(() => {
    // Gọi thử API của Python Backend xem sống hay chết
    axios.get(import.meta.env.VITE_API_URL || 'http://localhost:8000')
      .then(res => setStatus("✅ Kết nối thành công: " + res.data.message))
      .catch(err => setStatus("❌ Lỗi kết nối: " + err.message))
  }, [])

  return (
    <div style={{ fontFamily: 'sans-serif', textAlign: 'center', marginTop: '50px' }}>
      <h1>📸 Hệ thống FaceID</h1>
      <div style={{ padding: '20px', border: '2px solid #ddd', borderRadius: '10px', display: 'inline-block' }}>
        <h3>Trạng thái hệ thống:</h3>
        <p style={{ fontWeight: 'bold', color: status.includes('Lỗi') ? 'red' : 'green' }}>
          {status}
        </p>
      </div>
      <p style={{ marginTop: '20px', color: '#666' }}>
        Code React đang chạy trong Docker tại cổng 3000
      </p>
    </div>
  )
}
export default App
