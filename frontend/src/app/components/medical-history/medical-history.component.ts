import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConsultationHistoryService } from '../../services/consultation-history';
import { Injectable } from '@angular/core';

interface Consultation {
  date: string;
  doctor: string;
  specialty: string;
}

@Component({
  selector: 'app-medical-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './medical-history.component.html',
  styleUrl: './medical-history.component.scss'
})

/*export class MedicalHistoryComponent implements OnInit {
  consultations: Consultation[] = [];
  errorMessage: string = '';

  constructor(private consultationService: ConsultationHistoryService) {}

  ngOnInit(): void {
    this.loadConsultations();
  }

  loadConsultations(): void {
    this.consultationService.getConsultationHistory().subscribe({
      next: (data) => {
        this.consultations = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }
}*/

export class MedicalHistoryComponent {
  consultations: Consultation[] = [
    { date: '2024-12-20', doctor: 'Dr. TOUAT', specialty: 'Cardiologue' },
    { date: '2024-12-10', doctor: 'Dr. SENNANE', specialty: 'Dermatologue' },
    { date: '2024-12-05', doctor: 'Dr. FELKIR', specialty: 'Neurologue' }
  ];
}







