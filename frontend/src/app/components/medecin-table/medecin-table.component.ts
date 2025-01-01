import { CommonModule } from '@angular/common';
import { Component, OnChanges, OnInit } from '@angular/core';
import { PatientService } from '../../services/patient.services'
import { Input,Output } from '@angular/core';
import { SimpleChanges } from '@angular/core';

import { Router } from '@angular/router';

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
 
  errorMessage: string = '';
  @Input() searchResults: Patient[] = [];
  displayedPatients: Patient[] = [];
  

  constructor(private patientservice: PatientService , private router : Router) {}

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

  consulterPatient(nss: number): void {
    this.router.navigate(['/dossier-patient', nss]); 
  }
  
  
}

