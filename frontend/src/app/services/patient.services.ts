import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse , HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Patient } from '../models/patient.models';

  @Injectable({
    providedIn: 'root'
  })
export class PatientService {

     private readonly API_URL = 'http://localhost:8000/patients';
      
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



      getPatientByNSS(nss: number): Observable<any> {
        return this.http.get(`${this.API_URL}/${nss}`);
      }

      // private handleError(error: HttpErrorResponse) {
      //   let errorMessage = 'An error occurred';
    
      //   if (error.error instanceof ErrorEvent) {
      //     errorMessage = `Client error: ${error.error.message}`;
      //   } else {
      //     errorMessage = `Server error: ${error.status} - ${error.message}`;
      //   }
    
      //   console.error(errorMessage);
      //   return throwError(() => new Error(errorMessage));
      // }

      private handleError(error: HttpErrorResponse) {
        let errorMessage = 'An error occurred';
    
        if (error.error instanceof ErrorEvent) {
          errorMessage = `Client error: ${error.error.message}`;
        } else {
          if (error.status === 401) {
            errorMessage = 'Authentication failed. Please log in again.';
          } else if (error.status === 403) {
            errorMessage = 'You do not have permission to access this resource.';
          } else {
            errorMessage = `Server error: ${error.status} - ${error.message}`;
          }
        }
    
        console.error(errorMessage);
        return throwError(() => new Error(errorMessage));
      }
    

     
    
     } 