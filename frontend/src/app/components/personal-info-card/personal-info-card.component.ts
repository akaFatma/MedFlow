import { Component, OnInit } from '@angular/core';
import { UserInfoService } from '../../services/personal-info.service';
import { CommonModule } from '@angular/common';



@Component({
  selector: 'app-personal-info-card',
  imports: [CommonModule],
  templateUrl: './personal-info-card.component.html',
  styleUrl: './personal-info-card.component.scss'
})
export class PersonalInfoCardComponent implements OnInit {
  user = {
    'patient': {
      'nom': "Doe",
      'prenom': "John",
      'nss': "123456789", 
      'adresse': "123 rue de la rue", 
      'date_de_naissance':'1985-04-12', 
      'telephone': "0123456789", 
      'mutuelle': "MGEN", 
      'personne_a_contacter': {
        'nom': "Doe", 
        'prenom': "Jane", 
        'telephone': "0123456789"
      }, 
      'medecins': [{
        'nom': "Amiri", 
        'prenom': "Sara", 
        'specialite': "Cardiologue", 
      }]
    }, 
    'antecedants_medicaux': "Asthme",
    'etat': 'ouvert'
  }

  errorMessage = '';

  constructor(private userInfoService: UserInfoService) {}

  ngOnInit(): void {
    this.loadUserInfo();
  }

  loadUserInfo(): void {
    this.userInfoService.getUserInfo().subscribe({
      next: (data) => {
        this.user = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching user info:', error);
      }
    });
  }







}
