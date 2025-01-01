import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { InfermierTableComponent } from '../../components/infermier-table/infermier-table.component';
import { SoinsComponent } from '../../components/soins/soins.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from "../../components/search-bar/search-bar.component";
import { SearchService } from '../../services/search.services';
import { PatientService } from '../../services/patient.services';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

interface Patient {
  nom: string;
  prenom: string;
  nss: number;
}

@Component({
  selector: 'app-infermier-landing-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InfermierTableComponent,
    SoinsComponent,
    BienvenuComponentComponent,
    SearchBarComponent
  ],
  templateUrl: './infermier-landing-page.component.html',
  styleUrls: ['./infermier-landing-page.component.scss']
})
export class InfermierLandingPageComponent implements OnInit {
  showPopup: boolean = false;
  selectedPatient: Patient | null = null;
  results: Patient[] = [];
  userName: string = '';

  constructor(
    private searchService: SearchService,
    private patientService: PatientService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadAllPatients();
    this.userName = this.authService.getUserName();
  }

  loadAllPatients(): void {
    this.patientService.getConsultationHistory().subscribe({
      next: (data) => {
        this.results = data;
      },
      error: (error) => {
        console.error('Error fetching patients:', error);
        this.results = [];
      }
    });
  }

  onSearch(nss: number): void {
    if (!nss) {
      this.loadAllPatients();
      return;
    }

    this.searchService.searchByNSS(nss).subscribe({
      next: (data: Patient | Patient[]) => {
        this.results = Array.isArray(data) ? data : [data];
      },
      error: (error) => {
        console.error('Error fetching data:', error);
        this.results = [];
      }
    });
  }

  onConsulter(patient: Patient): void {
    this.router.navigate(['/dossier-patient', patient.nss]);
  }

  openPopup(patient: Patient): void {
    this.selectedPatient = patient;
    this.showPopup = true;
  }

  closePopup(): void {
    this.showPopup = false;
  }
}







  




 











