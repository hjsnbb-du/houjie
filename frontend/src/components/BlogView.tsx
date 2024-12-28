import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

interface Note {
  id: number;
  title: string;
  content: string;
  share_id: string;
  created_at: string;
  is_public: boolean;
  share_url: string | null;
}

export function BlogView() {
  const { username } = useParams<{ username: string }>();
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/blog/${username}/notes`);
        if (!response.ok) {
          throw new Error('Failed to fetch notes');
        }
        const data = await response.json();
        setNotes(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (username) {
      fetchNotes();
    }
  }, [username]);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center p-4">{error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">{username}'s Notes</h1>
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
                <div className="mt-4">
                  <Button asChild>
                    <Link to={`/note/${note.share_id}`}>Read More</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
          {notes.length === 0 && (
            <div className="text-center text-gray-500 py-8 col-span-full">
              No public notes available
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
