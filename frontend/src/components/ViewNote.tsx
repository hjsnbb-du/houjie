import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card } from "@/components/ui/card";
import MarkdownPreview from '@uiw/react-markdown-preview';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function ViewNote() {
  const { shareId } = useParams();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNote = async () => {
      try {
        const response = await fetch(`${API_URL}/api/notes/${shareId}`);
        if (!response.ok) {
          throw new Error('Note not found');
        }
        const note = await response.json();
        setContent(note.content);
        setLoading(false);
      } catch (error) {
        setError('Failed to load note');
        setLoading(false);
      }
    };

    fetchNote();
  }, [shareId]);

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <Card className="p-6">
        <MarkdownPreview source={content} />
      </Card>
    </div>
  );
}
