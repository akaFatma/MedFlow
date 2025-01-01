import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router'; // Import Router for navigation

interface Patient {
  nom: string;
  prenom: string;
  nss: string;
  etat: 'ouvert' | 'ferme';
}

@Component({
  selector: 'app-patient-table',
  standalone: true, // Declare it as standalone
  imports: [CommonModule], // Import CommonModule to use directives like *ngFor and [ngClass]
  templateUrl: './patient-table.component.html',
  styleUrls: ['./patient-table.component.scss'],
})
export class PatientTableComponent {
  constructor(private router: Router) {}

  patients: Patient[] = [
    { nom: 'Salhi', prenom: 'Fatma', nss: '110720004', etat: 'ouvert' },
    { nom: 'Salhi', prenom: 'Fatma', nss: '110720004', etat: 'ferme' },
    { nom: 'Salhi', prenom: 'Fatma', nss: '110720004', etat: 'ferme' },
    { nom: 'Salhi', prenom: 'Fatma', nss: '110720004', etat: 'ouvert' },
    { nom: 'Salhi', prenom: 'Fatma', nss: '110720004', etat: 'ferme' },
  ];

  handleEtatClick(patient: Patient) {
    if (patient.etat === 'ouvert') {
      console.log(`Opening DPI for patient: ${patient.nom} ${patient.prenom}`);
      // TODO: Implement logic to open DPI
    } else if (patient.etat === 'ferme') {
      console.log(`Closing DPI for patient: ${patient.nom} ${patient.prenom}`);
      // TODO: Implement logic to close DPI
    }
  }

  consulter(patient: Patient) {
    console.log(`Consulting patient: ${patient.nom} ${patient.prenom}`);
    // Directly navigate to the patient dossier page with NSS as parameter
    this.router.navigate(['/dossier-patient', patient.nss]);
  }
}
