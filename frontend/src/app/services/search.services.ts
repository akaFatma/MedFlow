import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private baseUrl = 'https/api'; 

  constructor(private http: HttpClient) { }

  searchByNSS(nss: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/search?nss=${nss}`);
  }

  scanQR(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/scanQR`);
  }
}