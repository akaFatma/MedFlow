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
      }
    }, 
    'antecedants_medicaux': "Asthme",
    'etat': 'ouvert'
  }

  errorMessage = '';
  decodedQRCode: string = '';

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


  // decodeQRCode(base64String: string): void {
  //   try {
  //     const base64Data = base64String.replace(/^data:image\/(png|jpg|jpeg|gif);base64,/, '');
  //     this.decodedQRCode = atob(base64Data);
  //     this.user.qrCode = `data:image/png;base64,${base64Data}`;
  //   } catch (error) {
  //     console.error('Error decoding QR code:', error);
  //     this.errorMessage = 'Error decoding QR code';
  //     this.decodedQRCode = '';
  //     this.user.qrCode = '';
  //   }
  // }

  // getQRCodeSrc(): string {
  //   return this.user.qrCode ? `data:image/png;base64,${this.user.qrCode}` : '';
  // }
  
  // getQRCodeSrc(): string {
  //   return this.user.qrCode ? `data:image/png;base64,${this.user.qrCode}` : '';
  // }







}
