import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { trigger, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-add-dpi',
  templateUrl: './add-dpi.component.html',
  styleUrls: ['./add-dpi.component.scss'],
  standalone: true,
  imports: [CommonModule, SidebarComponent, ReactiveFormsModule],
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
export class AddDPIComponent {
  patientForm: FormGroup;
  currentStep: number = 1;
  isSuccessPopupVisible: boolean = false;

  constructor(private fb: FormBuilder, private http: HttpClient) {
    // Initialisation du formulaire avec les champs requis
    this.patientForm = this.fb.group({
      step1: this.fb.group({
        prenom: ['', Validators.required],
        nom: ['', Validators.required],
        dateNaissance: ['', Validators.required],
        telephone: ['', [Validators.required, Validators.pattern('^[0-9]+$')]],
      }),
      step2: this.fb.group({
        securiteSociale: ['', Validators.required],
        mutuelle: ['', Validators.required],
        medecin: ['', Validators.required],
        personneContact: ['', Validators.required],
        profession: ['', Validators.required],
        assurance: ['', [Validators.required, Validators.pattern('^[0-9]+$')]],
      }),
    });
  }

  // Récupère toutes les données du formulaire
  getFormData() {
    return {
      nom: this.patientForm.value.step1.nom,
      prenom: this.patientForm.value.step1.prenom,
      dateNaissance: this.patientForm.value.step1.dateNaissance,
      telephone: this.patientForm.value.step1.telephone,
      securiteSociale: this.patientForm.value.step2.securiteSociale,
      mutuelle: this.patientForm.value.step2.mutuelle,
      medecin: this.patientForm.value.step2.medecin,
      personneContact: this.patientForm.value.step2.personneContact,
      profession: this.patientForm.value.step2.profession,
      assurance: this.patientForm.value.step2.assurance,
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
    const backendUrl = 'http://127.0.0.1:8000/creerrdpi/';

    this.http.post(backendUrl, transformedData, { headers }).subscribe(
      (response) => {
        console.log('Données envoyées avec succès au backend', response);
      },
      (error) => {
        console.error('Erreur lors de l\'envoi des données au backend', error);
      }
    );
  }
}
