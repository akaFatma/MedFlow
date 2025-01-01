import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { Patient } from '../models/patient.models';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private baseUrl = 'http://127.0.0.1:8000/patients'; 

  constructor(private http: HttpClient) { }

  searchByNSS(nss: number): Observable<Patient> {
    const params = new HttpParams().set('nss', nss.toString());
    return this.http.get<Patient>(`${this.baseUrl}/search`, { params })
  }
  scanQR(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/scanQR`);
  }
}