import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() {}

  setSession(email: string, role: string): void {
    localStorage.setItem('user_email', email);
    localStorage.setItem('user_role', role);
    localStorage.setItem('token', 'mock-jwt-token-123456');
  }

  getUserEmail(): string | null {
    return localStorage.getItem('user_email');
  }

  getUserRole(): string | null {
    return localStorage.getItem('user_role');
  }

  isAuthenticated(): boolean {
    return localStorage.getItem('token') !== null;
  }

  logout(): void {
    localStorage.clear();
  }
}
