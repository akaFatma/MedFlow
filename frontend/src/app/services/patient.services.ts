import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Patient } from '../models/patient.models';

@Injectable({
  providedIn: 'root'
})
export class PatientService {

  private readonly API_URL = 'http://localhost:8000/patients'; // Base URL for patient API
  
  constructor(private http: HttpClient) {}

  // Fetch the list of consultation history
  getConsultationHistory(): Observable<Patient[]> {
    return this.http.get<Patient[]>(this.API_URL).pipe(
      catchError(this.handleError)
    );
  }

  // Fetch patient by their unique ID
  getPatientById(id: string): Observable<Patient> {
    return this.http.get<Patient>(`${this.API_URL}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  // Fetch patient data by their NSS number (updated endpoint)
  getPatientByNSS(nss: number): Observable<any> {
    // Updated the endpoint to remove the extra 'patients' segment
    return this.http.get(`${this.API_URL}/${nss}`).pipe(
      catchError(this.handleError)  // Error handling
    );
  }

  // Handle API errors
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Client error: ${error.error.message}`;
    } else {
      errorMessage = `Server error: ${error.status} - ${error.message}`;
    }

    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));  // Throw error to be caught by subscribers
  }
}
