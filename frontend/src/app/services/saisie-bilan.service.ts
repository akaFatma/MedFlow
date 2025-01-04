import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SaisieBilanService {
  private readonly API_URL = 'http://localhost:8000/bio-pres';
  private readonly API_URL2 = 'http://localhost:8000/saisie-bilan';

  
  constructor(private http: HttpClient) {}

  getPrescription(id: number): Observable<any> {
    return this.http.get<any>(`${this.API_URL}?id=${id}`).pipe(
      catchError(this.handleError)
    );
  }  
  postResults(id: number, measures: string): Observable<any> {
    return this.http.post<any>(`${this.API_URL2}?id=${id}`, { measures }).pipe(
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