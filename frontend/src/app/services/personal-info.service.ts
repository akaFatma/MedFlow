import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
  

interface user {
    nom: string;
    prenom : string;
    securityNumber: number;
    address: string;
    phone: number;
    insurance: string;
    contactName: string;
    mutuelle : string;
    contactPrenom: string;
    contactPhone: number;
    doctors : string;
    qrCode: string;
    medicalHistory: string;
  }
@Injectable({
    providedIn: 'root'
})

  export class UserInfoService {
    private apiUrl = 'https://example.com/api/user';  //replace
  
    constructor(private http: HttpClient) {}
    
    getUserInfo(): Observable<user> {
      return this.http.get<any>(this.apiUrl);
    }
  }
  