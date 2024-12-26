import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { tap, catchError } from 'rxjs/operators';
import DOMPurify from 'dompurify';




@Injectable({
  providedIn: 'root'
})
export class AuthService {
  

  private loginUrl = 'http://127.0.0.1:8000/users/login'; 
  private tokenKey = '' // to store in local storage

  constructor(private http: HttpClient , private router : Router) {}

  login(username: string, password: string): Observable<any> {
   
    const satnitizedUsername = this.sanitizeInput(username);
    const sanitizedPassword = this.sanitizeInput(password);
    
    return this.http.post<any>(this.loginUrl, { 
       
       username : satnitizedUsername, //sanitize inputs to prevent injection attacks 
       password  : sanitizedPassword,

      }).pipe(
      tap(response =>{
        
        if (response && response.token){
          this.saveToken(response.token);
          this.router.navigate(['/test']);
        }
      }),
      catchError((error) => {
        console.error('Login failed:', error);
        throw error;
      }  )
    );
  }
  isAuthentificated():boolean{
    const token= this.getToken();
    return !!token //true if token exists , false otherwise
  }
  // Save token in localStorage
 private saveToken(token: string): void {
  localStorage.setItem(this.tokenKey, token);
}
//get token from local storage 
private getToken(): string | null {
  return localStorage.getItem(this.tokenKey);
}
private sanitizeInput(input: string): string {
  return DOMPurify.sanitize(input.trim()); 
}
  
}


 

