import { useState } from 'react';
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Card } from "./ui/card";
import { Share2 } from "lucide-react";
import { useToast } from "./ui/use-toast";
import { Toaster } from "./ui/toaster";
import MarkdownPreview from '@uiw/react-markdown-preview';
import { AuthDialog } from './AuthDialog';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function MarkdownEditor() {
  const [content, setContent] = useState('');
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('authToken'));
  const { toast } = useToast();

  const handleSetToken = (newToken: string | null) => {
    if (newToken) {
      localStorage.setItem('authToken', newToken);
    } else {
      localStorage.removeItem('authToken');
    }
    setToken(newToken);
  };

  const handleShare = async () => {
    try {
      console.log('Sharing note with content:', content);
      const response = await fetch(`${API_URL}/api/notes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify({
          content,
          title: content.split('\n')[0].replace(/^#\s*/, ''), // Extract title from first line
        }),
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        throw new Error('Failed to share note');
      }

      const note = await response.json();
      console.log('Received note:', note);
      const shareUrl = `${window.location.origin}/note/${note.share_id}`;
      console.log('Generated share URL:', shareUrl);

      // Copy to clipboard
      await navigator.clipboard.writeText(shareUrl);
      console.log('URL copied to clipboard');

      toast({
        title: "Note shared successfully!",
        description: "Share link has been copied to your clipboard.",
      });
      console.log('Toast notification shown');

      // Navigate to the shared note
      window.location.href = shareUrl;
    } catch (error) {
      console.error('Error sharing note:', error);
      toast({
        title: "Error sharing note",
        description: "Please try again later.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold">Editor</h2>
            <div className="flex gap-2">
              <AuthDialog onAuthSuccess={handleSetToken} />
              <Button onClick={handleShare} className="gap-2" disabled={!token}>
                <Share2 className="w-4 h-4" />
                Share
              </Button>
            </div>
          </div>
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your Markdown here..."
            className="min-h-[500px] font-mono"
          />
        </div>
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Preview</h2>
          <Card className="p-4 min-h-[500px] overflow-auto">
            <MarkdownPreview source={content} />
          </Card>
        </div>
      </div>
      <Toaster />
    </div>
  );
}
