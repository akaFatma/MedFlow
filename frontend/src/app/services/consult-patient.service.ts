// 
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConsultationPatientService {
  private apiUrl = 'http://127.0.0.1:8000/consultationContent';

  constructor(private http: HttpClient) {}

  getConsultation(id: number): Observable<any> {
    return this.http.post(this.apiUrl, id);
  }
}

