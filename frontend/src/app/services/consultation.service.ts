// 
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface ConsultationData {
  ordonnance: {
    date: string;
    lastName: string;
    firstName: string;
    age: number;
    medications: Array<{
      medication: string;
      dose: string;
      instructions: string;
    }>;
  };
  bilan: string[];
  resume: string;
}

@Injectable({
  providedIn: 'root'
})
export class ConsultationService {
  private apiUrl = 'http://localhost:4200/'; // Change to the actual URL

  constructor(private http: HttpClient) {}

  submitData(data: ConsultationData): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}
