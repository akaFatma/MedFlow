import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule, Validators, FormBuilder, FormGroup } from '@angular/forms';
import { InfermierTableComponent } from '../../components/infermier-table/infermier-table.component';
import { SoinsComponent } from '../../components/soins/soins.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from "../../components/search-bar/search-bar.component";
import { SearchService   } from '../../services/search.services';
import { PatientService } from '../../services/patient.services';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { InfermierService } from '../../services/infermier.service';


interface patient {
  nom : string ; 
  prenom : string;
  nss : number ;
}
@Component({
  selector: 'app-infermier-landing-page',
  imports: [CommonModule, BienvenuComponentComponent,FormsModule],
  templateUrl: './infermier-landing-page.component.html',
  styleUrl: './infermier-landing-page.component.scss'
})
export class InfermierLandingPageComponent  implements OnInit{

  patientCareForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private infermierService: InfermierService
  ) {}

  ngOnInit() {
    this.patientCareForm = this.fb.group({
      nss: ['', Validators.required],
      etatPatient: ['', Validators.required],
      medicaments: ['', Validators.required],
      autres: ['']
    });
  }

  onSubmit() {
    if (this.patientCareForm.valid) {
      this.infermierService.submitSoins(this.patientCareForm.value)
        .subscribe({
          next: (response) => {
            console.log('Soins enregistrés', response);
            this.patientCareForm.reset();
          },
          error: (error) => {
            console.error('Erreur d\'enregistrement', error);
          }
        });
    }
  }
}
  






  




 











