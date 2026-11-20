import { useState } from 'react'
const API = 'http://127.0.0.1:8000'
export default function App() {
  const [file, setFile] = useState(null), [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([]), [status, setStatus] = useState(''), [busy, setBusy] = useState(false)
  async function upload() {
    if (!file || busy) return
    setBusy(true); setStatus('Uploading and indexing...')
    const form = new FormData(); form.append('file', file)
    try {
      const r = await fetch(`${API}/upload`, { method: 'POST', body: form }), d = await r.json()
      if (!r.ok) throw new Error(d.detail || 'Upload failed')
      setStatus(`${d.message}: ${d.filename} (${d.chunks_added} chunks)`); setFile(null)
    } catch (e) { setStatus(e.message) } finally { setBusy(false) }
  }
  async function ask(e) {
    e.preventDefault(); const q = question.trim()
    if (!q || busy) return
    setMessages(m => [...m, { role: 'user', content: q }]); setQuestion(''); setBusy(true)
    try {
      const r = await fetch(`${API}/ask`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({question:q}) })
      const d = await r.json(); if (!r.ok) throw new Error(d.detail || 'Request failed')
      setMessages(m => [...m, { role: 'assistant', ...d }])
    } catch (e) { setMessages(m => [...m, { role:'assistant', answer:e.message }]) }
    finally { setBusy(false) }
  }
  return <main className="page">
    <header><p className="eyebrow">AGENTIC AI SYSTEM</p><h1>Agentic RAG</h1><p className="subtitle">Ask complex questions. The agent plans, selects tools, and combines evidence.</p></header>
    <section className="panel"><h2>Knowledge base</h2><p>Upload PDF, DOCX, or TXT documents.</p>
      <div className="row"><input type="file" accept=".pdf,.docx,.txt" onChange={e=>setFile(e.target.files?.[0]||null)}/><button disabled={!file||busy} onClick={upload}>Upload document</button></div>{status&&<p className="status">{status}</p>}
    </section>
    <section className="panel"><h2>Ask your agent</h2><div className="conversation">
      {!messages.length&&<p className="empty">Your questions, answers, agent activity, and sources will appear here.</p>}
      {messages.map((m,i)=><article className={`message ${m.role}`} key={i}><b>{m.role==='user'?'You':'Agent'}</b><p>{m.content||m.answer}</p>
        {m.tools_used?.length>0&&<p className="meta"><b>Tools:</b> {m.tools_used.join(', ')}</p>}
        {m.activity?.length>0&&<details><summary>Agent activity</summary><ul>{m.activity.map((x,j)=><li key={j}>{x}</li>)}</ul></details>}
        {m.sources?.length>0&&<details open><summary>Sources</summary><ul>{m.sources.map((s,j)=><li key={j}>{s.url?<a href={s.url} target="_blank" rel="noreferrer">{s.name}</a>:s.name}</li>)}</ul></details>}
      </article>)}{busy&&<p className="status">The agent is working...</p>}
    </div><form className="row ask" onSubmit={ask}><input value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask a question..."/><button disabled={!question.trim()||busy}>Send</button></form></section>
    <footer>Runs locally with Ollama · LangGraph · ChromaDB</footer>
  </main>
}
