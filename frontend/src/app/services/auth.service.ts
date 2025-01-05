import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { tap, catchError } from 'rxjs/operators';
import DOMPurify from 'dompurify';
import { ɵnormalizeQueryParams } from '@angular/common';
import { query } from 'express';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private loginUrl = 'http://127.0.0.1:8000/auth/login';
  private baseUrl: string = 'http://127.0.0.1:8000/getnss';
  private tokenKey = 'auth_token'; // to store in local storage
  private userNameKey = 'user_name'; // store the current username in local storage
  private roleKey = 'user_role'; // Store the role in localStorage

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<any> {
    const sanitizedUsername = this.sanitizeInput(username);
    const sanitizedPassword = this.sanitizeInput(password);

    return this.http
      .post<any>(this.loginUrl, {
        username: sanitizedUsername, //sanitize inputs to prevent injection attacks
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
            this.router.navigate([this.getRedirectUrl(response.user.role)]); // redirect based on the role
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
    return !!token; // true if token exists, false otherwise
  }

  // Save token in localStorage
  private saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  // Get token from local storage
  private getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private saveUserName(username: string): void {
    localStorage.setItem(this.userNameKey, username);
  }

  // Get username from localStorage
  getUserName(): string {
    return localStorage.getItem(this.userNameKey) || 'Guest'; // return 'Guest' if no username is found
  }

  // Save role in localStorage
  private saveUserRole(role: string): void {
    localStorage.setItem(this.roleKey, role);
  }

  // Get the role from localStorage
  getUserRole(): string {
    return localStorage.getItem(this.roleKey) || ''; // Default to an empty string if no role is found
  }

  envoyerusername(username : string): Observable<any> {
    const params = new HttpParams().set('username', username);

    return this.http.get(this.baseUrl, { params });
  }

  getRedirectUrl(role: string): string {
    if (role === 'Médecin') {
      return '/medecin-landing'; // Redirect to medecin landing page
    } else if (role === 'Administratif') {
      return '/add-dpi'; // Redirect to admin dashboard
    } else if (role === 'Patient') {
      const username = localStorage.getItem("user_name");
      if (username) {
        this.envoyerusername(username).subscribe({
          next: (response) => {
            // Logique de traitement de la réponse, si nécessaire
            console.log('Response:', response);
            // Redirection vers la page du patient avec nss dynamique
            console.log('NSS:', response.nss);
            this.router.navigate(['/dossier-patient', response.nss]); // Ex : /dossier-patient/12345
          },
          error: (error) => {
            // Gérer l'erreur si la requête échoue
            console.error('Erreur lors de l\'envoi du token:', error);
            // Optionnel : vous pouvez rediriger vers une autre page ou afficher un message d'erreur
          }
        });
      }
      // Vous pouvez ajouter un fallback en cas de problème ici
      return '/'; // Retour par défaut en cas d'absence de token ou d'erreur
    } else if (role === 'Infirmier') {
      return '/soins'; // Default landing page for other users
    } else if (role === 'Laborantin') {
      return '/laborantin'; // Default landing page for other users
    }else if (role === 'Radiologue') {
      return '/radiologue'; // Default landing page for other users
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