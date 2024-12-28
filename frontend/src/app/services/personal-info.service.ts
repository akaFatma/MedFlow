import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';
  

export interface user {
  'patient': {
    'nom': string,
    'prenom': string, 
    'nss': string, 
    'adresse': string, 
    'date_de_naissance': string, 
    'telephone': string, 
    'mutuelle': string, 
    'personne_a_contacter': {
      'nom': string, 
      'prenom': string, 
      'telephone': string
    }, 
    'medecins': [{
      'nom': string, 
      'prenom': string, 
      'specialite': string, 
    }]
  }, 
  'antecedants_medicaux': string,
  'etat': 'ouvert'
}
@Injectable({
    providedIn: 'root'
})

  export class UserInfoService {
    private baseUrl = 'http://127.0.0.1:8000/dpi/patients';  
    nss= 123456789;
    constructor(private http: HttpClient) {}
    
    getUserInfo(): Observable<user> {
      const params = new HttpParams().set('nss', this.nss.toString());
      return this.http.get<any>(`${this.baseUrl}/nss`, { params })
    }
  }
  