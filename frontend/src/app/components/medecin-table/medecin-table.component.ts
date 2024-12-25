import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { PatientService } from '../../services/patient.services'

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
export class MedecinTableComponent implements OnInit {
  patients: Patient[] = [];  
  errorMessage: string = '';

  constructor(private patientservice: PatientService) {}

  ngOnInit(): void {
    this.loadPatients();
  }

  loadPatients(): void {
    this.patientservice.getConsultationHistory().subscribe({
      next: (data) => {
        this.patients = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }

  // Example patient data to display before fetching real data
  patientss: Patient[] = [
    { nom: 'Salhi', prenom: 'Fatma', nss: 110720004, etat: 'ouvert' },
    { nom: 'Salhi', prenom: 'Fatma', nss: 110720004, etat: 'ouvert' },
    { nom: 'Salhi', prenom: 'Fatma', nss: 110720004, etat: 'fermé' },
    { nom: 'Salhi', prenom: 'Fatma', nss: 110720004, etat: 'fermé' },
    { nom: 'Salhi', prenom: 'Fatma', nss: 110720004, etat: 'fermé' }
  ];
}
