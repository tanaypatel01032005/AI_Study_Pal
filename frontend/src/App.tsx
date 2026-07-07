import { useState } from 'react'
import { BookOpen, GraduationCap, LayoutDashboard, Settings } from 'lucide-react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 flex font-sans selection:bg-blue-500/30">
      
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-900/50 backdrop-blur-xl p-4 flex flex-col gap-6">
        <div className="flex items-center gap-3 px-2 py-4 text-blue-400">
          <GraduationCap className="h-8 w-8" />
          <span className="text-xl font-bold tracking-tight text-slate-100">AI Study Pal</span>
        </div>

        <nav className="flex flex-col gap-2 flex-1">
          <Button 
            variant={activeTab === 'dashboard' ? 'secondary' : 'ghost'} 
            className="justify-start gap-3"
            onClick={() => setActiveTab('dashboard')}
          >
            <LayoutDashboard className="h-5 w-5" />
            Dashboard
          </Button>
          <Button 
            variant={activeTab === 'library' ? 'secondary' : 'ghost'} 
            className="justify-start gap-3"
            onClick={() => setActiveTab('library')}
          >
            <BookOpen className="h-5 w-5" />
            Library
          </Button>
          <Button 
            variant={activeTab === 'settings' ? 'secondary' : 'ghost'} 
            className="justify-start gap-3"
            onClick={() => setActiveTab('settings')}
          >
            <Settings className="h-5 w-5" />
            Settings
          </Button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950/0 to-slate-950/0 -z-10" />
        
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Welcome back, Student</h1>
            <p className="text-slate-400 mt-1">Here's your learning progress today.</p>
          </div>
          <Button className="bg-blue-600 hover:bg-blue-500 shadow-[0_0_20px_rgba(37,99,235,0.3)]">
            Upload Document
          </Button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-slate-400 text-sm font-medium">Study Streak</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">4 Days</div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-slate-400 text-sm font-medium">Quizzes Taken</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">12</div>
            </CardContent>
          </Card>
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-slate-400 text-sm font-medium">Concepts Mastered</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">28</div>
            </CardContent>
          </Card>
        </div>

        <h2 className="text-xl font-semibold mb-4">Recent Documents</h2>
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm p-8 text-center text-slate-400 border-dashed border-2">
          <BookOpen className="mx-auto h-12 w-12 opacity-20 mb-4" />
          <p>No documents uploaded yet.</p>
          <Button variant="link" className="text-blue-400">Upload your first PDF or DOCX</Button>
        </Card>
        
      </main>
    </div>
  )
}

export default App
