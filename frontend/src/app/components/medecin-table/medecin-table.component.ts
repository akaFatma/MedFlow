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
export class MedecinTableComponent implements OnInit {
  patients: Patient[] = [];  
  errorMessage: string = '';

  constructor(private patientservice: PatientService) {}

  ngOnInit(): void {
    this.loadPatients();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['searchResults']) {
      const currentValue = changes['searchResults'].currentValue;
      if (currentValue && currentValue.length > 0) {
        this.displayedPatients = currentValue;
      } else {
        // Only load all patients if we don't have search results
        this.loadPatients();
      }
    }
  }

  loadPatients(): void {
    this.patientservice.getConsultationHistory().subscribe({
      next: (data) => {
        this.displayedPatients = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching patients:', error);
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
