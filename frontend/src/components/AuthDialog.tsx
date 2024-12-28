import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useToast } from './ui/use-toast';
import { LogIn, UserPlus } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface AuthDialogProps {
  onAuthSuccess: (token: string) => void;
}

export function AuthDialog({ onAuthSuccess }: AuthDialogProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_URL}/api/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          credentials: 'include',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Login failed');
        }

        const data = await response.json();
        onAuthSuccess(data.access_token);
        setIsOpen(false);
        toast({
          title: 'Success',
          description: 'Logged in successfully',
        });
      } else {
        const response = await fetch(`${API_URL}/api/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            username,
            password,
            email,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Registration failed');
        }

        // Auto-login after registration
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const loginResponse = await fetch(`${API_URL}/api/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          credentials: 'include',
          body: formData,
        });

        if (!loginResponse.ok) {
          const errorData = await loginResponse.json();
          throw new Error(errorData.detail || 'Auto-login failed');
        }

        const data = await loginResponse.json();
        onAuthSuccess(data.access_token);
        setIsOpen(false);
        toast({
          title: 'Success',
          description: 'Registered and logged in successfully',
        });
      }
    } catch (error) {
      let errorMessage = isLogin ? 'Login failed' : 'Registration failed';
      
      if (error instanceof Error && 'response' in error) {
        const response = (error as any).response;
        if (response instanceof Response) {
          const errorData = await response.json().catch(() => null);
          if (errorData?.detail) {
            errorMessage = errorData.detail;
          }
        }
      }
      
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="gap-2">
          {isLogin ? <LogIn className="w-4 h-4" /> : <UserPlus className="w-4 h-4" />}
          {isLogin ? 'Login' : 'Register'}
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{isLogin ? 'Login' : 'Register'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Input
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value.toLowerCase())}
            />
            {!isLogin && (
              <p className="text-sm text-gray-500">
                Username must contain only lowercase letters, numbers, and hyphens, and must start and end with a letter or number.
              </p>
            )}
          </div>
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {!isLogin && (
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          )}
          <div className="flex justify-between">
            <Button type="button" variant="ghost" onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? 'Need an account?' : 'Already have an account?'}
            </Button>
            <Button type="submit">{isLogin ? 'Login' : 'Register'}</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
