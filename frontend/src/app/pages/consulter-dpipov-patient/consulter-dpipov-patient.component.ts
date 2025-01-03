import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { PatientService } from '../../services/patient.services';
import { MedicalHistoryComponent } from '../../components/medical-history/medical-history.component';
import { PersonalInfoCardComponent } from '../../components/personal-info-card/personal-info-card.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-consulter-dpipov-patient',
  template: `
  <app-medical-history [nss]="patientNSS"></app-medical-history>
`,
  imports: [CommonModule, MedicalHistoryComponent, PersonalInfoCardComponent, BienvenuComponentComponent],
  templateUrl: './consulter-dpipov-patient.component.html',
  styleUrls: ['./consulter-dpipov-patient.component.scss']
})
export class ConsulterDPIPovPatientComponent implements OnInit {

  isDoctor: boolean = false;
  patientNSS: number | null = null; // To store the patient's NSS from the route parameter

  constructor(
    private authService: AuthService,
    private patientService: PatientService,
    private route: ActivatedRoute,
    private router : Router
  ) {}

  ngOnInit(): void {
    // Check the role of the user and if the user is a doctor
    const userRole = this.authService.getUserRole();
    console.log('User Role:', userRole);
    this.isDoctor = userRole === 'Médecin'; // Set isDoctor to true if the role is 'Médecin'

    // Get the patient NSS from the route parameters
    this.patientNSS = +this.route.snapshot.paramMap.get('nss')!; // Get NSS from the route path
    console.log('Patient NSS:', this.patientNSS);
  }


  handleNewConsultation(): void {
    this.router.navigate(['/new-consultation'], { queryParams: {'nss' : this.patientNSS}});
  }
}

