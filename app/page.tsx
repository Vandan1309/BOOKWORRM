'use client'

import { FormEvent, KeyboardEvent, useMemo, useState } from 'react'
import {
  ArrowLeft,
  ArrowUpRight,
  BookOpen,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Feather,
  Menu,
  MessageCircle,
  Send,
  Sparkles,
  X,
} from 'lucide-react'

const FEEDBACK_EMAIL = 'FEEDBACK_EMAIL'

type Book = {
  id: string
  title: string
  author: string
  description: string
  cover: string
  pageCount?: number
  questions: string[]
}

type Citation = { page: number; excerpt: string }
type ChatMessage = { role: 'user' | 'assistant'; content: string; citations?: Citation[]; prototype?: boolean }
type View = 'welcome' | 'library' | 'chat' | 'reader' | 'about' | 'feedback'

const books: Book[] = [
  { id: 'jungle_book', title: 'The Jungle Book', author: 'Rudyard Kipling', description: 'A collection of unforgettable tales about belonging, courage, and the laws of the wild.', cover: 'jungle', questions: ['What does the jungle law teach Mowgli?', 'Why is Mowgli caught between two worlds?', 'What themes of belonging run through the stories?'] },
  { id: 'alice_in_wonderland', title: "Alice's Adventures in Wonderland", author: 'Lewis Carroll', description: 'A curious fall into a world where language, logic, and identity are wonderfully unstable.', cover: 'alice', questions: ['What does the changing size of Alice represent?', 'How does the book play with logic?', 'Who is Alice becoming in Wonderland?'] },
  { id: 'around_the_world', title: 'Around the World in Eighty Days', author: 'Jules Verne', description: 'A race against time, across continents, where precision meets chance and adventure.', cover: 'world', questions: ['What drives Phileas Fogg?', 'How does the journey change Passepartout?', 'Explain the importance of the final wager.'] },
  { id: 'wuthering_heights', title: 'Wuthering Heights', author: 'Emily Brontë', description: 'A storm-lit story of desire, revenge, and the haunting force of memory across generations.', cover: 'heights', questions: ['Why is Heathcliff so consumed by revenge?', 'How does the landscape reflect the characters?', 'What makes the novel feel like a ghost story?'] },
]

const mockAnswers: Record<string, string> = {
  jungle_book: 'Mowgli’s choices are shaped by a tension between two kinds of belonging: the freedom of the jungle and the pull of human society. His education in the law of the pack gives him confidence, but it also makes clear that every home has boundaries.',
  alice_in_wonderland: 'Alice’s changing size turns a simple bodily experience into a question of identity. Wonderland keeps asking who she is, and her answer shifts as quickly as the rules around her do.',
  around_the_world: 'Fogg’s calm is less a lack of feeling than a way of making the world measurable. The wager gives every delay a cost, while the journey gradually reveals that his companions matter as much as the timetable.',
  wuthering_heights: 'Heathcliff’s revenge grows from grief that has been denied a humane outlet. The novel makes his fixation feel both self-chosen and inherited, as if the landscape itself keeps the old wound alive.',
}

function getBook(id: string) { return books.find((book) => book.id === id) ?? books[0] }

function Wordmark({ dark = false }: { dark?: boolean }) {
  return <div className={`wordmark ${dark ? 'wordmark-dark' : ''}`}><span>BOOKWO</span><span className="brand-r">R</span><span>RM</span></div>
}

function WelcomeScreen({ onEnter, onAbout }: { onEnter: () => void; onAbout: () => void }) {
  return <main className="welcome-screen">
    <div className="welcome-art" aria-hidden="true" />
    <div className="welcome-noise" aria-hidden="true" />
    <header className="welcome-header"><Wordmark dark /><span className="welcome-descriptor">Your AI-Assisted Bookmark</span><button className="text-link light-link" onClick={onAbout}>About BOOKWORRM <ArrowUpRight data-icon="inline-end" /></button></header>
    <section className="welcome-content">
      <p className="eyebrow light-eyebrow"><Feather data-icon="inline-start" /> A Rewamp Digital project</p>
      <h1>Every book holds<br /><em>a world.</em></h1>
      <p className="welcome-subtitle">Every question opens another door.</p>
      <button className="button button-gold" onClick={onEnter}>Enter the Wonderful World of Books <ArrowUpRight data-icon="inline-end" /></button>
    </section>
    <div className="welcome-foot"><span>Read deeply</span><span className="foot-line" /><span>Ask freely</span><span className="foot-line" /><span>Stay curious</span></div>
  </main>
}

function Navbar({ view, onNavigate }: { view: View; onNavigate: (view: View) => void }) {
  const [open, setOpen] = useState(false)
  const navigate = (next: View) => { setOpen(false); onNavigate(next) }
  return <header className="navbar"><button className="logo-button" onClick={() => navigate('library')} aria-label="Return to library"><Wordmark /></button><nav className="desktop-nav" aria-label="Main navigation">{[['library', 'Library'], ['about', 'About'], ['feedback', 'Feedback']].map(([id, label]) => <button key={id} className={`nav-link ${view === id ? 'active' : ''}`} onClick={() => navigate(id as View)}>{label}</button>)}</nav><button className="menu-button" onClick={() => setOpen(!open)} aria-expanded={open} aria-label={open ? 'Close navigation' : 'Open navigation'}>{open ? <X /> : <Menu />}</button>{open && <div className="mobile-nav">{[['library', 'Library'], ['about', 'About'], ['feedback', 'Feedback']].map(([id, label]) => <button key={id} className={view === id ? 'active' : ''} onClick={() => navigate(id as View)}>{label}</button>)}</div>}</header>
}

function BookCover({ book, small = false }: { book: Book; small?: boolean }) { return <div className={`book-cover ${book.cover} ${small ? 'book-cover-small' : ''}`}><div className="cover-frame"><span className="cover-kicker">A CLASSIC</span><strong>{book.title}</strong><span className="cover-author">{book.author}</span><span className="cover-mark">BOOKWORRM</span></div></div> }

function BookCard({ book, onAsk, onRead }: { book: Book; onAsk: () => void; onRead: () => void }) { return <article className="book-card"><BookCover book={book} /><div className="book-card-body"><div><h3>{book.title}</h3><p className="book-author">{book.author}</p></div><p className="book-description">{book.description}</p><div className="book-meta"><span><BookOpen data-icon="inline-start" /> Page count unavailable</span></div><div className="book-actions"><button className="button button-primary" onClick={onAsk}>Ask BOOKWORRM <MessageCircle data-icon="inline-end" /></button><button className="button button-ghost" onClick={onRead}>Read Book <ArrowUpRight data-icon="inline-end" /></button></div></div></article> }

function Footer({ onNavigate }: { onNavigate: (view: View) => void }) { return <footer className="footer"><div className="footer-brand"><Wordmark /><p>Your AI-Assisted Bookmark</p><em>Stay curious. Go beyond the page.</em></div><div className="footer-links"><span className="footer-label">Explore</span><button onClick={() => onNavigate('library')}>Library</button><button onClick={() => onNavigate('about')}>About</button><button onClick={() => onNavigate('feedback')}>Feedback</button></div><div className="footer-credit"><p>An AI reading companion by Rewamp Digital.</p><p>© 2026 BOOKWORRM · By Rewamp Digital</p></div></footer> }

function Library({ onAsk, onRead, onNavigate }: { onAsk: (id: string) => void; onRead: (id: string) => void; onNavigate: (view: View) => void }) { return <><Navbar view="library" onNavigate={onNavigate} /><main className="library-page"><section className="library-intro"><div><p className="eyebrow"><Sparkles data-icon="inline-start" /> The reading room</p><h1>Find your next <em>question.</em></h1><p>Explore a story, revisit a moment, or ask what lies between the lines.</p></div><div className="library-count"><span>04</span><small>preloaded<br />classics</small></div></section><section className="book-grid" aria-label="Available books">{books.map((book) => <BookCard key={book.id} book={book} onAsk={() => onAsk(book.id)} onRead={() => onRead(book.id)} />)}</section></main><Footer onNavigate={onNavigate} /></> }

function Citation({ citation }: { citation: Citation }) { const [expanded, setExpanded] = useState(false); return <div className="citation-wrap"><button className="citation" onClick={() => setExpanded(!expanded)} aria-expanded={expanded}><span className="citation-number">{citation.page}</span><span><b>Source · PDF page {citation.page}</b><small>Open passage</small></span><ChevronDown className={expanded ? 'rotated' : ''} /></button>{expanded && <div className="citation-popover">“{citation.excerpt}”<span>Mock citation for UI prototyping — verification will come from the Python RAG backend.</span></div>}</div> }

function ChatView({ book, onBack, onRead }: { book: Book; onBack: () => void; onRead: () => void }) { const [messages, setMessages] = useState<ChatMessage[]>([{ role: 'assistant', content: `Welcome to the pages of ${book.title}. Ask me about a character, a moment, or an idea you want to see more clearly.`, prototype: true }]); const [input, setInput] = useState(''); const [loading, setLoading] = useState(false); const [error, setError] = useState('');
  const submit = async (event?: FormEvent) => { event?.preventDefault(); if (!input.trim() || loading) return; const question = input.trim(); setInput(''); setError(''); setMessages((prev) => [...prev, { role: 'user', content: question }]); setLoading(true); await new Promise((resolve) => setTimeout(resolve, 650)); setMessages((prev) => [...prev, { role: 'assistant', content: mockAnswers[book.id], prototype: true, citations: [{ page: book.id === 'wuthering_heights' ? 42 : 18, excerpt: 'This source excerpt will be supplied by the connected retrieval pipeline.' }] }]); setLoading(false) }
  const onKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => { if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing && event.keyCode !== 229) { event.preventDefault(); void submit() } }
  return <div className="app-shell"><Navbar view="library" onNavigate={onBack} /><main className="chat-page"><button className="back-link" onClick={onBack}><ArrowLeft data-icon="inline-start" /> Back to library</button><div className="chat-layout"><aside className="chat-context"><BookCover book={book} small /><p className="eyebrow">Currently exploring</p><h1>{book.title}</h1><p>{book.author}</p><button className="button button-ghost full-width" onClick={onRead}><BookOpen data-icon="inline-start" /> Read this book</button><div className="context-note"><span className="status-dot" /> Prototype mode<br /><small>Answers will connect to your book-specific RAG API.</small></div></aside><section className="chat-panel"><div className="chat-heading"><div><p className="eyebrow">Ask the margins</p><h2>What are you curious about?</h2></div><span className="prototype-pill">UI prototype</span></div><div className="messages" aria-live="polite">{messages.map((message, index) => <div key={index} className={`message-row ${message.role}`}><div className={`message ${message.role}`}>{message.role === 'assistant' && <span className="message-icon"><Sparkles /></span>}<p>{message.content}</p>{message.prototype && <span className="prototype-note">Prototype response — not verified against the book.</span>}{message.citations?.map((citation, citationIndex) => <Citation citation={citation} key={citationIndex} />)}</div></div>)}{loading && <div className="message-row assistant"><div className="message assistant loading-message"><span className="message-icon"><Sparkles /></span><span className="typing"><i /><i /><i /></span></div></div>}{error && <div className="chat-error">{error}</div>}</div><div className="suggestions"><span>Try asking</span>{book.questions.map((question) => <button key={question} onClick={() => setInput(question)}>{question}</button>)}</div><form className="composer" onSubmit={submit}><textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={onKeyDown} placeholder="Ask about this book..." rows={2} aria-label="Ask about this book" /><button className="send-button" type="submit" disabled={!input.trim() || loading} aria-label="Send question"><Send /></button><small>Enter to send · Shift + Enter for a new line</small></form></section></div></main></div> }

function ReadingView({ book, onBack, onAsk }: { book: Book; onBack: () => void; onAsk: () => void }) { const [page, setPage] = useState(1); return <div className="app-shell"><Navbar view="library" onNavigate={onBack} /><main className="reader-page"><div className="reader-top"><button className="back-link" onClick={onBack}><ArrowLeft data-icon="inline-start" /> Back to library</button><div className="reader-title"><p className="eyebrow">Reading room</p><h1>{book.title}</h1><p>{book.author}</p></div><button className="button button-primary" onClick={onAsk}><MessageCircle data-icon="inline-start" /> Ask BOOKWORRM</button></div><section className="pdf-stage"><div className="pdf-placeholder"><BookOpen /><p>PDF integration point</p><h2>Your selected book will appear here.</h2><span>The Python API can provide a secure PDF URL for <strong>{book.id}</strong>. No local file or placeholder document is being presented.</span></div></section><div className="reader-controls"><button onClick={() => setPage(Math.max(1, page - 1))} disabled={page === 1} aria-label="Previous page"><ChevronLeft /></button><span>Page {page} <small>of —</small></span><button onClick={() => setPage(page + 1)} aria-label="Next page"><ChevronRight /></button></div></main></div> }

function AboutSection({ onNavigate }: { onNavigate: (view: View) => void }) { return <><Navbar view="about" onNavigate={onNavigate} /><main className="simple-page about-page"><div className="simple-mark"><Feather /></div><p className="eyebrow">The idea behind the bookmark</p><h1>About <em>BOOKWORRM</em></h1><p className="lead">BOOKWORRM is an AI-assisted reading companion by Rewamp Digital. It helps readers explore characters, understand motivations, revisit important moments, and discover the ideas hidden between the pages of a book.</p><div className="about-rule" /><p className="pull-quote">Stay curious.<br /><em>Go beyond the page.</em></p><button className="button button-primary" onClick={() => onNavigate('library')}>Return to the library <ArrowUpRight data-icon="inline-end" /></button></main><Footer onNavigate={onNavigate} /></> }

function FeedbackForm() { const [message, setMessage] = useState(''); const [email, setEmail] = useState(''); const [notice, setNotice] = useState(''); const [fallback, setFallback] = useState(''); const handleSubmit = (event: FormEvent) => { event.preventDefault(); if (!message.trim()) return; const subject = encodeURIComponent('BOOKWORRM Feedback'); const body = encodeURIComponent(`${message.trim()}${email.trim() ? `\\n\\nReply email: ${email.trim()}` : ''}`); const mailto = `mailto:${FEEDBACK_EMAIL}?subject=${subject}&body=${body}`; window.location.href = mailto; setNotice('Your email app should open with your feedback ready to send. Please review it and press Send.'); setFallback(`To: ${FEEDBACK_EMAIL}\\nSubject: BOOKWORRM Feedback\\n\\n${message.trim()}`) }; return <form className="feedback-form" onSubmit={handleSubmit}><label htmlFor="feedback">Your feedback <span>*</span></label><textarea id="feedback" required value={message} onChange={(e) => setMessage(e.target.value)} placeholder="What is on your mind?" rows={7} /><label htmlFor="reply-email">Email for a reply <small>optional</small></label><input id="reply-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" /><button type="submit" className="button button-primary">Send Feedback <ArrowUpRight data-icon="inline-end" /></button>{notice && <p className="form-notice">{notice}</p>}{fallback && <details className="fallback"><summary>Email draft details</summary><pre>{fallback}</pre></details>}</form> }

function FeedbackSection({ onNavigate }: { onNavigate: (view: View) => void }) { return <><Navbar view="feedback" onNavigate={onNavigate} /><main className="simple-page feedback-page"><div className="feedback-copy"><p className="eyebrow">A note in the margin</p><h1>Help us make BOOKWORRM <em>better.</em></h1><p className="lead">Share a suggestion, report a problem, or tell us what you&apos;d love to see next.</p><p className="quiet-note">Your message will open in your email app as a draft. Nothing is sent without your review.</p></div><FeedbackForm /></main><Footer onNavigate={onNavigate} /></> }

export default function Page() { const [view, setView] = useState<View>('welcome'); const [selectedId, setSelectedId] = useState(books[0].id); const selectedBook = useMemo(() => getBook(selectedId), [selectedId]); const enter = () => setView('library'); const navigate = (next: View) => setView(next); if (view === 'welcome') return <WelcomeScreen onEnter={enter} onAbout={() => setView('about')} />; if (view === 'chat') return <ChatView book={selectedBook} onBack={() => setView('library')} onRead={() => setView('reader')} />; if (view === 'reader') return <ReadingView book={selectedBook} onBack={() => setView('library')} onAsk={() => setView('chat')} />; if (view === 'about') return <AboutSection onNavigate={navigate} />; if (view === 'feedback') return <FeedbackSection onNavigate={navigate} />; return <Library onAsk={(id) => { setSelectedId(id); setView('chat') }} onRead={(id) => { setSelectedId(id); setView('reader') }} onNavigate={navigate} /> }
