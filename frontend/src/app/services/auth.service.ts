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
  private tokenKey = 'auth_token';// to store in local storage
  private userNameKey =  'user_name';; //store the current username in local storage
  private roleKey = 'user_role'; // Store the role in localStorage

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<any> {
    const satnitizedUsername = this.sanitizeInput(username);
    const sanitizedPassword = this.sanitizeInput(password);

    return this.http
      .post<any>(this.loginUrl, {
        username: satnitizedUsername, //sanitize inputs to prevent injection attacks
        password: sanitizedPassword,
      })
      .pipe(
        tap((response) => {
          if (response && response.token) {
            console.log('Full response:', response);
            console.log('User:', response.user);
            console.log('Role:', response.user.role);
            this.saveToken(response.token);
            this.saveUserName(response.user.username);
            this.saveUserRole(response.user.role);
            this.router.navigate([this.getRedirectUrl(response.user.role)]); //redirect based on the role
          }
        }),
        catchError((error) => {
          console.error('Login failed:', error);
          throw error;
        })
      );
  }
  isAuthentificated(): boolean {
    const token = this.getToken();
    return !!token; //true if token exists , false otherwise
  }
  // Save token in localStorage
  private saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }
  //get token from local storage
  private getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }
  private saveUserName(username: string): void {
    localStorage.setItem(this.userNameKey, username);
  }

  // Get username from localStorage
  getUserName(): string {
    return localStorage.getItem(this.userNameKey) || 'Guest' ; //return 'Guest' if no username is found
  }
  // Save role in localStorage
  private saveUserRole(role: string): void {
    localStorage.setItem(this.roleKey, role);
  }
  // Get the role from localStorage
  getUserRole(): string {
    return localStorage.getItem(this.roleKey) || ''; // Default to an empty string if no role is found
  }
   getRedirectUrl(role: string): string {
    if (role === 'Médecin') {
      return '/medecin-landing'; // Redirect to medecin landing page
    } else if (role === 'administratif') {
      return '/admin-dashboard'; // Redirect to admin dashboard
    } else if (role === 'Patient') {
      return '/dossier-patient'; // Default landing page for other users
    }
    return '/'; // Default return value if no role matches
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
