import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';

interface Patient {
  nom: string;
  prenom: string;
  nss: number;
  etat: 'ouvert' | 'fermé';
}

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private baseUrl = 'https/api'; 

  constructor(private http: HttpClient) { }

  searchByNSS(nss: number): Observable<Patient> {
    const params = new HttpParams().set('nss', nss.toString());
    return this.http.get<Patient>(`${this.baseUrl}/search`, { params })
  }
  scanQR(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/scanQR`);
  }
}