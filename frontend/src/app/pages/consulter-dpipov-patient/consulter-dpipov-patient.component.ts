import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { PatientService } from '../../services/patient.services';
import { ActivatedRoute } from '@angular/router';
import { MedicalHistoryComponent } from '../../components/medical-history/medical-history.component';
import { PersonalInfoCardComponent } from '../../components/personal-info-card/personal-info-card.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-consulter-dpipov-patient',
  imports: [CommonModule,MedicalHistoryComponent, PersonalInfoCardComponent, BienvenuComponentComponent],
  templateUrl: './consulter-dpipov-patient.component.html',
  styleUrl: './consulter-dpipov-patient.component.scss'
})
export class ConsulterDPIPovPatientComponent  implements OnInit{

  patientData: any;
  isDoctor: boolean = false;
  patientNSS : number | null = null; 

  constructor (
    private authService: AuthService,
    private patientService: PatientService,
    private route: ActivatedRoute
  ) {}
 ngOnInit(): void {

  const userRole = this.authService.getUserRole();
  console.log('User Role:', userRole); 
  this.isDoctor = userRole === 'Médecin'; 
  this.patientNSS = +this.route.snapshot.paramMap.get('nss')!;//get the parameter from the route 
  this.loadPatientData();
     
 }
 private loadPatientData() {
  if (this.patientNSS) {
    this.patientService.getPatientByNSS(this.patientNSS).subscribe({
    next: (data) => {
      this.patientData = data;
    },
    error: (error) => {
      console.error('Error loading patient data:', error);
    }
    
    });
  } else {
    console.error('Patient NSS is null');
  }
  };
}



