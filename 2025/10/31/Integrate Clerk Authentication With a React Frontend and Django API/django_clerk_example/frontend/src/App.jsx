import { useState } from 'react'
import './App.css'
import { SignedIn, SignedOut, SignInButton, UserButton, useAuth } from '@clerk/clerk-react'

function App() {
  const [videos, setVideos] = useState([])
  const { getToken } = useAuth();

  const fetchVideos = async () => {
    const token = await getToken();
    const response = await fetch('/api/videos/', {
      headers: {
        Authorization: `Bearer ${token}`,
      }
    })
    const data = await response.json()
    setVideos(data)
  }

  return (
    <>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <h1>YouTube Videos</h1>
        <div className="card">
          <button onClick={fetchVideos}>Fetch Videos</button>
        </div>
        <ul>
          {videos.map(video => (
            <li key={video.id}>{video.title}</li>
          ))}
        </ul>
      </SignedIn>
    </>
  )
}

export default App
