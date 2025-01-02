import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import  { user }  from '../models/user.models';

@Injectable({
    providedIn: 'root'
})
  export class UserInfoService {
    private baseUrl = 'http://127.0.0.1:8000/patients/nss';  
    constructor(private http: HttpClient) {}
    user: user | undefined;
    getUserInfo(nss : number): Observable<user> {
      console.log('fouffouuuuu ', nss);
      const params = new HttpParams().set('nss', nss.toString());
      return this.http.get<any>(`${this.baseUrl}`, { params })
    }
  }
  