import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';
import { useToast } from './ui/use-toast';

interface Note {
  id: number;
  title: string;
  content: string;
  share_id: string;
  created_at: string;
  is_public: boolean;
  share_url: string | null;
}

export function UserNotesList() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/notes`, {
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch notes');
        }
        const data = await response.json();
        setNotes(data);
      } catch (err) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load your notes. Please try again later."
        });
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, [toast]);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Notes</h1>
        <Button asChild>
          <Link to="/">Create New Note</Link>
        </Button>
      </div>
      <ScrollArea className="h-[calc(100vh-200px)]">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {notes.map((note) => (
            <Card key={note.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{note.title}</CardTitle>
                <div className="text-sm text-gray-500">
                  {new Date(note.created_at).toLocaleDateString()}
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 line-clamp-3">{note.content}</p>
                <div className="mt-4 space-y-2">
                  <Button asChild className="w-full">
                    <Link to={`/note/${note.share_id}`}>View Note</Link>
                  </Button>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>Status: {note.is_public ? 'Public' : 'Private'}</span>
                    {note.share_url && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          navigator.clipboard.writeText(note.share_url!);
                          toast({
                            title: "Link Copied",
                            description: "Share link has been copied to clipboard"
                          });
                        }}
                      >
                        Copy Link
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
          {notes.length === 0 && (
            <div className="text-center text-gray-500 py-8 col-span-full">
              You haven't created any notes yet. Click "Create New Note" to get started!
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
