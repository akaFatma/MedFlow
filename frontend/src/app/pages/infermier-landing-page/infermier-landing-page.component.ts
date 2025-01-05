import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import {
  FormsModule,
  ReactiveFormsModule,
  Validators,
  FormBuilder,
  FormGroup,
} from '@angular/forms';
import { InfermierTableComponent } from '../../components/infermier-table/infermier-table.component';
import { SoinsComponent } from '../../components/soins/soins.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from '../../components/search-bar/search-bar.component';
import { SearchService } from '../../services/search.services';
import { PatientService } from '../../services/patient.services';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { InfermierService } from '../../services/infermier.service';

interface patient {
  nom: string;
  prenom: string;
  nss: number;
}
@Component({
  selector: 'app-infermier-landing-page',
  imports: [
    CommonModule,
    BienvenuComponentComponent,
    FormsModule,
    ReactiveFormsModule,
  ],
  templateUrl: './infermier-landing-page.component.html',
  styleUrl: './infermier-landing-page.component.scss',
})
export class InfermierLandingPageComponent implements OnInit {
  patientCareForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private infermierService: InfermierService,
    private router: Router
  ) {}
  goToHomePage() {
    this.router.navigate(['/HomePage']);
  }
  ngOnInit() {
    console.log('Initialisation du composant');
    this.patientCareForm = this.fb.group({
      nss: ['', Validators.required],
      etatPatient: ['', Validators.required],
      medicaments: ['', Validators.required],
      autres: [''],
    });
    console.log('Formulaire initialisé:', this.patientCareForm);
  }

  onSubmit() {
    console.log('Soumission du formulaire déclenchée');
    if (this.patientCareForm.valid) {
      console.log('Soumission du formulaire déclenchée');
      const formData = this.patientCareForm.getRawValue();
      console.log('Données du formulaire récupérées:', formData);
      const formattedData = {
        nss: formData.nss,
        etatPatient: formData.etatPatient,
        medicaments: formData.medicaments,
        etat: formData.etatPatient,
        medicament: formData.medicaments,
        autre: formData.autres,
      };
      console.log("Données formatées pour l'API:", formattedData);
      this.infermierService.submitSoins(formattedData).subscribe({
        next: (response) => {
          console.log('Soins enregistrés', response);
          this.patientCareForm.reset();
        },
        error: (error) => {
          console.error("Erreur d'enregistrement", error);
        },
      });
    }
  }
}
