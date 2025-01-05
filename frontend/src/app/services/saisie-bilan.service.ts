import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SaisieBilanService {
  private readonly API_URL = 'http://localhost:8000/bio-pres';
  private readonly API_URL2 = 'http://localhost:8000/saisie-bilan-bio';
  private readonly API_URL3 = 'http://localhost:8000/radio-pres';
  private readonly API_URL4 = 'http://localhost:8000/saisie-bilan-radio';

  
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
  getPrescriptionRadio(id: number): Observable<any> {
    return this.http.get<any>(`${this.API_URL3}?id=${id}`).pipe(
      catchError(this.handleError)
    );
  }  
  postCompteRendu(id: number, formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.API_URL4}?id=${id}`, formData).pipe(
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