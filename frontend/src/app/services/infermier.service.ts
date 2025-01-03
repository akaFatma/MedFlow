import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Soins } from '../models/soins.models';
export type { Soins } from '../models/soins.models'


@Injectable({
  providedIn: 'root'
})
export class InfermierService {

  private apiUrl = 'http://127.0.0.1:8000/soin';

  constructor(private http: HttpClient) {}

  submitSoins(data: Soins ): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}