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
  private loginUrl = 'http://127.0.0.1:8000/auth/login'; // Backend login endpoint
  private tokenKey = 'auth_token'; // Key to store the token in localStorage
  private userNameKey = 'user_name'; // Key to store the username in localStorage
  private roleKey = 'user_role'; // Key to store the role in localStorage

  constructor(private http: HttpClient, private router: Router) {}

  /**
   * Perform login by sending username and password to the server.
   * @param username User's username
   * @param password User's password
   * @returns Observable of the login response
   */
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
            this.saveToken(response.token);
            this.saveUserName(response.user.username);
            this.saveUserRole(response.user.role);

            // Redirect user based on their role
            const redirectUrl = this.getRedirectUrl(response.user.role, response.user.nss);
            this.router.navigate([redirectUrl]);
          }
        }),
        catchError((error) => {
          console.error('Login failed:', error);
          throw error;
        })
      );
  }

  /**
   * Check if the user is authenticated by verifying the presence of a token.
   * @returns true if authenticated, false otherwise
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Save the authentication token in localStorage.
   * @param token Authentication token
   */
  private saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  /**
   * Retrieve the authentication token from localStorage.
   * @returns The token if present, otherwise null
   */
  private getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Save the user's username in localStorage.
   * @param username User's username
   */
  private saveUserName(username: string): void {
    localStorage.setItem(this.userNameKey, username);
  }

  /**
   * Retrieve the user's username from localStorage.
   * @returns The username if present, otherwise 'Guest'
   */
  getUserName(): string {
    return localStorage.getItem(this.userNameKey) || 'Guest';
  }

  /**
   * Save the user's role in localStorage.
   * @param role User's role
   */
  private saveUserRole(role: string): void {
    localStorage.setItem(this.roleKey, role);
  }

  /**
   * Retrieve the user's role from localStorage.
   * @returns The role if present, otherwise an empty string
   */
  getUserRole(): string {
    return localStorage.getItem(this.roleKey) || '';
  }

  /**
   * Determine the appropriate redirect URL based on the user's role.
   * @param role User's role
   * @param nss (Optional) Patient's NSS for redirection to their dossier
   * @returns Redirect URL as a string
   */
  getRedirectUrl(role: string, nss?: string): string {
    switch (role) {
      case 'Médecin':
        return '/medecin-landing';
      case 'Administratif':
        return '/add-dpi';
      case 'Patient':
        return nss ? `/dossier-patient/${nss}` : '/dossier-patient';
      case 'Infirmier':
        return '/soins';
      default:
        return '/';
    }
  }

  /**
   * Sanitize user input to prevent injection attacks.
   * @param input Input string to sanitize
   * @returns Sanitized string
   */
  private sanitizeInput(input: string): string {
    return DOMPurify.sanitize(input.trim());
  }

  /**
   * Log the user out by removing all authentication-related data from localStorage.
   */
  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userNameKey);
    localStorage.removeItem(this.roleKey);
    this.router.navigate(['/login']);
  }
}
