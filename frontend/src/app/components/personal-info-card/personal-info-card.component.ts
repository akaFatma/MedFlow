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
    nom: 'John',
    prenom: 'Doe',
    securityNumber: 123456789,
    address: '1234 Elm St',
    phone: 1234567890,
    mutuelle : 'test ',
    insurance: 'Blue Cross',
    contactName: 'Jane',
    contactPrenom: 'Doe',
    contactPhone: 1234567890,
    doctors: 'Dr. Smith, Dr. Johnson',
    qrCode: '1234567890',
    medicalHistory: 'ffffffffffffffjfkdjfkd this dude is dying type shit'
  };

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
