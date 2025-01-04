import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { trigger, style, animate, transition } from '@angular/animations';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { AuthService } from '../../services/auth.service';
import { OnInit } from '@angular/core';
import { SuccessNotifComponent } from '../../components/success-notif/success-notif.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-dpi',
  templateUrl: './add-dpi.component.html',
  styleUrls: ['./add-dpi.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, SuccessNotifComponent],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('300ms ease-out', style({ opacity: 1 })),
      ]),
      transition(':leave', [animate('300ms ease-out', style({ opacity: 0 }))]),
    ]),
  ],
})
export class AddDPIComponent implements OnInit {
  userName: string = '';
  patientForm: FormGroup;
  currentStep: number = 1;
  isSuccessPopupVisible: boolean = false;
  successTitle: string = ''; // Title for success popup
  successDescription: string = ''; // Description for success popup

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private authService: AuthService,
    private router: Router
  ) {
    // Initialisation du formulaire avec les champs requis
    this.patientForm = this.fb.group({
      step1: this.fb.group({
        prenom: ['', Validators.required],
        nom: ['', Validators.required],
        date_naissance: ['', Validators.required],
        telephone: ['', [Validators.required, Validators.pattern('^[0-9]+$')]],
      }),
      step2: this.fb.group({
        nss: ['', Validators.required],
        mutuelle: ['', Validators.required],
        adr: ['', Validators.required],
        nom_personne: ['', Validators.required],
        prenom_personne: ['', Validators.required],
        telephone_personne: [
          '',
          [Validators.required, Validators.pattern('^[0-9]+$')],
        ],
      }),
    });
  }
  ngOnInit(): void {
    this.userName = this.authService.getUserName();
  }

  // Récupère toutes les données du formulaire
  getFormData() {
    return {
      nom: this.patientForm.value.step1.nom,
      prenom: this.patientForm.value.step1.prenom,
      date_naissance: this.patientForm.value.step1.date_naissance,
      telephone: this.patientForm.value.step1.telephone,
      nss: this.patientForm.value.step2.nss,
      mutuelle: this.patientForm.value.step2.mutuelle,
      adr: this.patientForm.value.step2.adr,
      nom_personne: this.patientForm.value.step2.nom_personne,
      prenom_personne: this.patientForm.value.step2.prenom_personne,
      telephone_personne: this.patientForm.value.step2.telephone_personne,
    };
  }

  // Vérifie si l'étape est complète
  isStepComplete(): boolean {
    if (this.currentStep === 1) {
      return this.patientForm.get('step1')?.valid ?? false;
    } else if (this.currentStep === 2) {
      return this.patientForm.get('step2')?.valid ?? false;
    }
    return true;
  }

  // Va à l'étape suivante
  goToNextStep(): void {
    if (this.currentStep < 3) {
      this.currentStep++;
    }
  }

  // Va à l'étape précédente
  goToPreviousStep(): void {
    if (this.currentStep > 1) {
      this.currentStep--;
    }
    if (this.currentStep === 1) {
      this.router.navigate(['/HomePage']);
    }
  }

  // Retourne le texte du bouton selon l'étape
  getButtonText(): string {
    if (this.currentStep === 3) {
      return 'Valider';
    } else {
      return 'Suivant';
    }
  }

  // Soumet le formulaire et envoie les données au backend
  onValidate(): void {
    if (this.patientForm.valid) {
      this.sendDataToBackend(); // Envoi final des données au backend
      this.successTitle = 'DPI créé avec succès';
      this.successDescription = 'Le dossier patient a été enregistré';
      this.isSuccessPopupVisible = true;
      setTimeout(() => {
        this.isSuccessPopupVisible = false;
      }, 3000);
    }
  }

  // Ferme le popup de succès
  closeSuccessPopup(): void {
    this.isSuccessPopupVisible = false;
  }

  // Envoie les données au backend
  sendDataToBackend(): void {
    const formData = this.getFormData();

    const transformedData = {
      data: formData,
    };

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // URL du backend
    const backendUrl = 'http://127.0.0.1:8000/creerdpi';

    this.http.post(backendUrl, transformedData, { headers }).subscribe(
      (response) => {
        console.log('Données envoyées avec succès au backend', response);
      },
      (error) => {
        console.error("Erreur lors de l'envoi des données au backend", error);
      }
    );
  }
}
