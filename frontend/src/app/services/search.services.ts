import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { Patient } from '../models/patient.models';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private baseUrl = 'https//localhost:42000/test';

  constructor(private http: HttpClient) { }

  searchByNSS(nss: number): Observable<Patient> {
    const params = new HttpParams().set('nss', nss.toString());
    return this.http.get<Patient>(`${this.baseUrl}/search`, { params })
  }
}