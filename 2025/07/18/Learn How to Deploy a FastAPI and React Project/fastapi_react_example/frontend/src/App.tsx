import { useState } from 'react'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useMutation, useQuery } from '@tanstack/react-query'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

type Task = {
  task_id: string;
}

type Comment = {
  id: string;
  category: string;
  text: string;
}

type TaskStatus = {
  task_id: string;
  status: string;
  data: {[key: string]: Comment[]};
}

async function analyzeVideo(url: string): Promise<Task> {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({url: url})
  })
  if (!response.ok) {
    throw new Error('Network response was not ok')
  }
  return response.json()
}

async function getStatus(taskId: string): Promise<TaskStatus> {
  const response = await fetch(`${API_BASE_URL}/status/${taskId}`)
  if (!response.ok) {
    throw new Error('Network response was not ok')
  }
  return response.json()
}

function App() {
  const [url, setUrl] = useState('')
  const [taskId, setTaskId] = useState('')

  const mutation = useMutation({
    mutationFn: analyzeVideo,
    onSuccess: (data: Task) => {
      setTaskId(data.task_id)
    }
  })

  const { data } = useQuery<TaskStatus>({
    queryKey: ['status', taskId],
    queryFn: () => getStatus(taskId),
    enabled: !!taskId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === "completed" ? false : 2000;
    }
  })

  return (
    <>
    <header>
      <h1>YouTube Comments Analyzer</h1>
    </header>
    <input type="text" placeholder="Enter YouTube video URL" onChange={(e) => setUrl(e.target.value)} />
    <button onClick={() => mutation.mutate(url)} disabled={mutation.isPending || !url.trim()}>{taskId ? 'Analyzing...' : 'Analyze'}</button>

    {data?.status === "completed" && (
      <div>
        <h2>Analysis Results</h2>
        <div>
          {Object.keys(data.data).map((key) => (
            <div key={key}>
              <h3>{key}</h3>
              <div>
                {data.data[key].map((item) => 
                <div key={item.id}>
                  <p>{item.text}</p>
                </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    )}
    <ReactQueryDevtools />
    </>
  )
}

export default App
