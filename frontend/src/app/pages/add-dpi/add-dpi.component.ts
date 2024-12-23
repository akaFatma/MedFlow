import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

@Component({
  selector: 'app-add-dpi',
  templateUrl: './add-dpi.component.html',
  styleUrls: ['./add-dpi.component.scss'],
  standalone: true,
  imports: [CommonModule, SidebarComponent, ReactiveFormsModule],
})
export class AddDPIComponent {
  currentStep: number = 1;
  patientForm: FormGroup;

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

  // Check if current step is complete
  isStepComplete(): boolean {
    if (this.currentStep === 1) {
      return this.patientForm.get('step1')?.valid || false;
    } else if (this.currentStep === 2) {
      return this.patientForm.get('step2')?.valid || false;
    } else if (this.currentStep === 3) {
      // Always enable the button in step 3
      return true;
    }
    return false;
  }

  // Method to move to the next step
  goToNextStep(): void {
    if (this.currentStep < 3 && this.isStepComplete()) {
      this.currentStep++;
    }
  }

  // Method to move to the previous step
  goToPreviousStep(): void {
    if (this.currentStep > 1) {
      this.currentStep--;
    }
  }

  // Get button text based on current step
  getButtonText(): string {
    if (this.currentStep === 2 && this.isStepComplete()) {
      return 'Suivant';
    } else if (this.currentStep === 3) {
      return 'Valider';
    }
    return 'Suivant';
  }

  // Get form data for summary
  getFormData() {
    return {
      ...this.patientForm.get('step1')?.value,
      ...this.patientForm.get('step2')?.value,
    };
  }
}
