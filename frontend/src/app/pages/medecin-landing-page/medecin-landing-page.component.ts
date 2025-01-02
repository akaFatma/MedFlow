import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { SideBarComponent } from '../../components/side-bar/side-bar.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from '../../components/search-bar/search-bar.component';
import { MedecinTableComponent } from '../../components/medecin-table/medecin-table.component';
import { SearchService } from '../../services/search.services';
import { PatientService } from '../../services/patient.services';
import { Patient } from '../../models/patient.models';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { QrScannerComponent } from '../../components/qr-scanner/qr-scanner.component';


@Component({
  selector: 'app-medecin-landing-page',
  imports: [
    CommonModule,
    SideBarComponent,
    BienvenuComponentComponent,
    SearchBarComponent,
    MedecinTableComponent,
    QrScannerComponent
  ],
  templateUrl: './medecin-landing-page.component.html',
  styleUrl: './medecin-landing-page.component.scss'
})
export class MedecinLandingPageComponent implements OnInit {
  
  results: Patient[] = [];
  userName: string = '';
  isQrScannerVisible: boolean = false; 
 
  constructor(
    private searchService: SearchService,
    private patientService : PatientService,
    private authService : AuthService,
    private router : Router
  
  ) {}

  ngOnInit(): void {
    // Load all patients when component initializes
    this.loadAllPatients();
    // Get the username dynamically
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
      this.loadAllPatients(); //if search is cleared load patients again
      return;
    }
    this.searchService.searchByNSS(nss).subscribe({
      next: (data: Patient) => {
        this.results = Array.isArray(data) ? data : [data];
      },
      error: (error) => {
        console.error('Error fetching data:', error);
        this.results = []; 
      }
    });

}

onScanQR() {
  this.isQrScannerVisible = true;
}
onCloseScanner() {
  this.isQrScannerVisible = false;
}

onConsulter(patient: Patient): void { 
  this.router.navigate(['/dossier-patient', patient.nss]);
}
}