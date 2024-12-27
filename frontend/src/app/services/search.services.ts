import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private baseUrl = 'http://127.0.0.1:8000/dpi/patients'; 

  constructor(private http: HttpClient) { }

  searchByNSS(nss: number): Observable<any> {
    const params = new HttpParams().set('nss', nss.toString());
    return this.http.get<any>(`${this.baseUrl}/search`, { params })
    // return this.http.get<any>(`${this.baseUrl}/search?nss=${nss}`);
  }
  scanQR(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/scanQR`);
  }
}