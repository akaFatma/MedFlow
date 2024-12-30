import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { InfermierTableComponent } from '../../components/infermier-table/infermier-table.component';
import { SoinsComponent } from '../../components/soins/soins.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from "../../components/search-bar/search-bar.component";
import { SearchService   } from '../../services/search.services';
import { PatientService } from '../../services/patient.services';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';


interface patient {
  nom : string ; 
  prenom : string;
  nss : number ;
}
@Component({
  selector: 'app-infermier-landing-page',
  imports: [CommonModule, InfermierTableComponent, SoinsComponent, BienvenuComponentComponent, SearchBarComponent],
  templateUrl: './infermier-landing-page.component.html',
  styleUrl: './infermier-landing-page.component.scss'
})
export class InfermierLandingPageComponent  implements OnInit{

    showPopup: boolean = false;
    selectedPatient: any = null; //data to pass to the soins component if needed
    results: patient[] = [];
    userName: string = '';
   
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
        next: (data: patient) => {
          this.results = Array.isArray(data) ? data : [data];
        },
        error: (error) => {
          console.error('Error fetching data:', error);
          this.results = []; 
        }
      });
  
  }

  onConsulter(patient: patient): void { 
    this.router.navigate(['/dossier-patient', patient.nss]);
  }


   //to trigger the popup display
   openPopup(patient: any): void {
    this.selectedPatient = patient;
    this.showPopup = true;
  }
  //close the popup
  closePopup(): void {
    this.showPopup = false;
  }

 
  }






  




 











