import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Consultation } from '../models/consultation.models';

@Injectable({
  providedIn: 'root'
})
export class ConsultationHistoryService {
  private readonly API_URL = 'http://localhost:3000/consultationHistory';
  
  constructor(private http: HttpClient) {}

  getConsultationHistory(): Observable<Consultation[]> {
    return this.http.get<Consultation[]>(this.API_URL).pipe(
      catchError(this.handleError)
    );
  }

  //get a specific consultation by ID
  getConsultationById(id: string): Observable<Consultation> {
    return this.http.get<Consultation>(`${this.API_URL}/${id}`).pipe(
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