import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConsultationService {
  private apiUrl = 'http://127.0.0.1:8000/users/login';  //enter your url here rayane

  constructor(private http: HttpClient) {}

  submitData(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return this.http.post(this.apiUrl, data, { headers });
  }
}
