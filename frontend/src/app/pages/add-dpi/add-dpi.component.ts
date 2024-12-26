import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';

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
  currentStep: number = 1;
  patientForm: FormGroup;
  isSuccessPopupVisible: boolean = false;

  constructor(private fb: FormBuilder) {
    this.patientForm = this.fb.group({
      step1: this.fb.group({
        prenom: ['', Validators.required],
        nom: ['', Validators.required],
        dateNaissance: ['', Validators.required],
        telephone: ['', Validators.required],
      }),
      step2: this.fb.group({
        securiteSociale: ['', Validators.required],
        mutuelle: ['', Validators.required],
        medecin: ['', Validators.required],
        personneContact: ['', Validators.required],
        profession: ['', Validators.required],
        assurance: ['', Validators.required],
      }),
    });
  }

  isStepComplete(): boolean {
    if (this.currentStep === 1) {
      return this.patientForm.get('step1')?.valid || false;
    } else if (this.currentStep === 2) {
      return this.patientForm.get('step2')?.valid || false;
    }
    return true;
  }

  goToNextStep(): void {
    if (this.currentStep < 3 && this.isStepComplete()) {
      this.currentStep++;
    }
  }

  goToPreviousStep(): void {
    if (this.currentStep > 1) {
      this.currentStep--;
    }
  }

  getButtonText(): string {
    return this.currentStep === 3 ? 'Valider' : 'Suivant';
  }

  getFormData() {
    return {
      ...this.patientForm.get('step1')?.value,
      ...this.patientForm.get('step2')?.value,
    };
  }

  onValidate(): void {
    if (this.currentStep === 3) {
      this.isSuccessPopupVisible = true;
      setTimeout(() => {
        this.isSuccessPopupVisible = false;
      }, 3000);
    }
  }

  closeSuccessPopup(): void {
    this.isSuccessPopupVisible = false;
  }
}
