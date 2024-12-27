import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { tap, catchError } from 'rxjs/operators';
import DOMPurify from 'dompurify';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private loginUrl = 'http://127.0.0.1:8000/users/login';
  private tokenKey = 'auth_token';
  private userNameKey = 'user_name';
  private roleKey = 'user_role';

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<any> {
    const sanitizedUsername = this.sanitizeInput(username);
    const sanitizedPassword = this.sanitizeInput(password);

    return this.http
      .post<any>(this.loginUrl, {
        username: sanitizedUsername,
        password: sanitizedPassword,
      })
      .pipe(
        tap((response) => {
          if (response && response.token) {
            // Store the authentication data
            this.saveToken(response.token);
            this.saveUserName(response.user.username);
            this.saveUserRole(response.user.role);

            // Get the redirect URL
            const redirectUrl = this.getRedirectUrl(response.user.role);
            console.log('Role:', response.user.role);
            console.log('Redirect URL:', redirectUrl);

            // Use setTimeout to ensure the storage is complete before navigation
            setTimeout(() => {
              this.router.navigate([redirectUrl]).then(
                (success) => {
                  if (success) {
                    console.log('Navigation successful');
                  } else {
                    console.error('Navigation failed');
                    console.log('Current route:', this.router.url);
                  }
                },
                (error) => {
                  console.error('Navigation error:', error);
                }
              );
            }, 10000);
          }
        }),
        catchError((error) => {
          console.error('Login failed:', error);
          throw error;
        })
      );
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    return !!token;
  }

  private saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private saveUserName(username: string): void {
    localStorage.setItem(this.userNameKey, username);
  }

  getUserName(): string {
    return localStorage.getItem(this.userNameKey) || 'Guest';
  }

  private saveUserRole(role: string): void {
    // Normalize the role before saving
    const normalizedRole = this.normalizeRole(role);
    localStorage.setItem(this.roleKey, normalizedRole);
  }

  getUserRole(): string {
    const role = localStorage.getItem(this.roleKey) || '';
    return this.normalizeRole(role);
  }

  private normalizeRole(role: string): string {
    // Normalize the role to handle different encodings of 'é'
    return role.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  getRedirectUrl(role: string): string {
    const normalizedRole = this.normalizeRole(role);
    if (normalizedRole === this.normalizeRole('Médecin')) {
      return '/medecin-landing';
    } else if (normalizedRole === 'Administratif') {
      return '/admin-dashboard';
    } else {
      return '/user-landing';
    }
  }

  private sanitizeInput(input: string): string {
    return DOMPurify.sanitize(input.trim());
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userNameKey);
    localStorage.removeItem(this.roleKey);
    this.router.navigate(['/login']);
  }
}
