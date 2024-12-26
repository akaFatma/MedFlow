import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

interface patient {
  nom: string;
  prenom: string;
  nss: number;
}

@Injectable({
  providedIn: 'root'
})
export class InfermierService {
  private readonly API_URL = 'http://localhost:3000/infermier';
  
  constructor(private http: HttpClient) {}

  getTable(): Observable<patient[]> {
    return this.http.get<patient[]>(this.API_URL).pipe(
      catchError(this.handleError)
    );
  }

  

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client error: ${error.error.message}`;
    } else {
      errorMessage = `Server error: ${error.status} - ${error.message}`;
    }

    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}