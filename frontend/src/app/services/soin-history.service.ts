import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SoinHistoryService {
  private readonly API_URL = 'http://localhost:8000/soinHistory';
  
  constructor(private http: HttpClient) {}

  getSoinHistory(nss : number): Observable<any> {
    return this.http.get<any>(`${this.API_URL}?nss=${nss}`).pipe(
      catchError(this.handleError)
    );
  }

  //get a specific Soin by ID
  getSoinById(id: string): Observable<any> {
    return this.http.get<any>(`${this.API_URL}/${id}`).pipe(
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