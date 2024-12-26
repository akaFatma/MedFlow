import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';


interface Patient {
    nom: string;
    prenom: string;
    nss: number;
    etat: 'ouvert' | 'fermé';
  }

  @Injectable({
    providedIn: 'root'
  })
export class PatientService {

     private readonly API_URL = 'http://localhost:3000/cff';
      
      constructor(private http: HttpClient) {}
    
      getConsultationHistory(): Observable<Patient[]> {
        return this.http.get<Patient[]>(this.API_URL).pipe(
          catchError(this.handleError)
        );
      }
    
      getPatientById(id: string): Observable<Patient> {
        return this.http.get<Patient>(`${this.API_URL}/${id}`).pipe(
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