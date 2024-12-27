import { CommonModule } from '@angular/common';
import { Component, OnChanges, OnInit } from '@angular/core';
import { PatientService } from '../../services/patient.services'
import { Input } from '@angular/core';
import { SimpleChanges } from '@angular/core';

interface Patient {
  nom: string;
  prenom: string;
  nss: number;
  etat: 'ouvert' | 'fermé';
}

@Component({
  selector: 'app-medecin-table',
  imports: [CommonModule],
  templateUrl: './medecin-table.component.html',
  styleUrls: ['./medecin-table.component.scss']  
})
export class MedecinTableComponent implements OnInit , OnChanges {
  patients: Patient[] = [];  
  errorMessage: string = '';
 
  @Input() searchResults: Patient[] = [];
  displayedPatients: Patient[] = [];
 

  constructor(private patientservice: PatientService) {}

  ngOnInit(): void {
    this.loadPatients();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['searchResults'] && changes['searchResults'].currentValue) {
      this.displayedPatients = changes['searchResults'].currentValue;
    }
  }

 /* loadPatients(): void {
    this.patientservice.getConsultationHistory().subscribe({
      next: (data) => {
        this.patients = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }*/

  loadPatients(): void {
    this.patientservice.getConsultationHistory().subscribe({
      next: (data) => {
        this.displayedPatients = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }
}
