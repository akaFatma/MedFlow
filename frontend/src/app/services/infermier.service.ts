import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Patient } from '../models/patient.models';

@Injectable({
  providedIn: 'root'
})
export class InfermierService {
  private readonly API_URL = 'http://127.0.0.1:8000/';
  
  constructor(private http: HttpClient) {}

  getTable(): Observable<Patient[]> {
    return this.http.get<Patient[]>(this.API_URL).pipe(
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