import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class MedecinService {
  private apiUrl = 'http://127.0.0.1:8000/medecin'; // Replace with your API endpoint

  constructor(private http: HttpClient) {}

  getMedecinInfo(username: string): Observable<any> {
    const url = `${this.apiUrl}?username=${username}`;
    console.log(url)
    return this.http
      .get(url)
      .pipe(
        catchError((error) => {
          console.error('Error fetching Medecin:', error);
          return throwError(() => new Error('Failed to fetch Medecin info'));
        })
      );
  }
}
