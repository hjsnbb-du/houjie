import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { MarkdownEditor } from "./components/MarkdownEditor";
import { ViewNote } from "./components/ViewNote";
import { BlogView } from "./components/BlogView";
import { UserNotesList } from "./components/UserNotesList";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MarkdownEditor />} />
        <Route path="/note/:shareId" element={<ViewNote />} />
        <Route path="/blog/:username" element={<BlogView />} />
        <Route path="/my/notes" element={<UserNotesList />} />
      </Routes>
      <Toaster />
    </Router>
  );
}

export default App
