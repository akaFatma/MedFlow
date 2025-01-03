import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ConsultationHistoryService } from '../../services/consultation-history';
import { Injectable } from '@angular/core';
import { Consultation } from '../../models/consultation.models';
import { ConsultationPatientService} from '../../services/consult-patient.service';

@Component({
  selector: 'app-medical-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './medical-history.component.html',
  styleUrl: './medical-history.component.scss'
})

export class MedicalHistoryComponent implements OnInit {
  consultations: Consultation[] = [];
  errorMessage: string = '';

  @Input() nss: any;
  constructor(private consultationService: ConsultationHistoryService, private router: Router, 
    private consultationPatientService: ConsultationPatientService
  ) {}

  ngOnInit(): void {
    this.loadConsultations();
  }

  loadConsultations(): void {
    this.consultationService.getConsultationHistory(this.nss).subscribe({
      next: (data) => {
        this.consultations = data;
        console.log('Consultations:', this.consultations);
        console.log('Data :', data);
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }
  onConsult(id: number): void {
    this.router.navigate(['/consult-patient'], { queryParams: { id } });
  }
}